from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from .forms import ImageUploadForm, UserProfileEditForm
from .models import PredictionImage
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import numpy as np
import tensorflow as tf
from PIL import Image
from scipy import ndimage
import cv2
import pytesseract
import re
from django.db.models import Avg
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

# # Lazy loading of Keras model to handle import errors gracefully
kbe_keras_model = None

from keras.models import load_model

# then load your model
keras_model = load_model('CNN_Model.h5',
    custom_objects={'softmax_v2': tf.nn.softmax})
# Temporary in-memory user profile data used by profile-related views
# In a real application this would come from the database (e.g. a Profile model).
MOCK_USER_DATA = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
}

# --- BASIC VIEWS ---

def index_view(request):
    """Home page view."""
    return render(request, 'Home.html')

def contact_view(request):
    """Contact page view."""
    return render(request, 'Contact.html')

def about_view(request):
    """About page view."""
    return render(request, 'about.html')

# --- PREDICTION VIEW ---
# Keep startup fast/reliable for local development by default.
# These metrics can be wired to a background task later if needed.
overall_accuracy = None
precision = None
recall = None
f1 = None


def _prepare_binary_image(uploaded_file):
    """Convert uploaded image to a binary map where digit pixels are 1."""
    img = Image.open(uploaded_file).convert('L')
    arr = np.array(img).astype('float32') / 255.0

    # Auto-orient to MNIST style: foreground bright, background dark.
    if np.mean(arr) > 0.5:
        arr = 1.0 - arr

    # Binarize and denoise for stable connected-component extraction.
    # Use an adaptive threshold so faint strokes are not dropped.
    threshold = max(0.18, float(np.mean(arr) + 0.15 * np.std(arr)))
    binary = arr > threshold
    # Keep thin handwriting by avoiding aggressive opening.
    binary = ndimage.binary_closing(binary, structure=np.ones((2, 2)))
    binary = ndimage.binary_fill_holes(binary)
    return binary.astype(np.uint8)


def _split_component_by_projection(component):
    """
    Split a wide component into multiple digit chunks using vertical projection.
    Returns one or more components.
    """
    h, w = component.shape
    if w <= h * 1.15:
        return [component]

    col_sum = np.sum(component, axis=0)
    active = col_sum > max(1, int(h * 0.04))

    segments = []
    start = None
    for i, is_active in enumerate(active):
        if is_active and start is None:
            start = i
        elif not is_active and start is not None:
            if i - start >= 3:
                segments.append((start, i))
            start = None
    if start is not None and (w - start) >= 3:
        segments.append((start, w))

    if len(segments) <= 1:
        return [component]

    split_components = []
    for x0, x1 in segments:
        piece = component[:, x0:x1]
        rows = np.where(np.sum(piece, axis=1) > 0)[0]
        if rows.size == 0:
            continue
        y0, y1 = rows[0], rows[-1] + 1
        cropped = piece[y0:y1, :]
        if cropped.size > 0:
            split_components.append(cropped.astype('float32'))

    return split_components if split_components else [component]


def _extract_digit_crops(binary_image):
    """Find digit components and return left-to-right cropped images."""
    labeled, num_features = ndimage.label(binary_image)
    slices = ndimage.find_objects(labeled)
    components = []
    image_h, image_w = binary_image.shape

    for idx, slc in enumerate(slices, start=1):
        if slc is None:
            continue
        y_slice, x_slice = slc
        h = y_slice.stop - y_slice.start
        w = x_slice.stop - x_slice.start
        area = h * w

        # Skip obvious noise and tiny marks.
        if area < 80 or h < 8 or w < 3:
            continue

        component = (labeled[y_slice, x_slice] == idx).astype('float32')
        pixel_count = int(np.sum(component))
        fill_ratio = pixel_count / float(area)

        # Reject components that are too sparse or too dense to be a digit.
        if fill_ratio < 0.03 or fill_ratio > 0.97:
            continue

        # Reject components spanning almost the whole image (background artifacts).
        if h > int(image_h * 0.95) and w > int(image_w * 0.95):
            continue

        x_center = (x_slice.start + x_slice.stop) / 2.0
        components.append((x_center, area, component, h, w))

    if not components:
        return []

    # Keep only components close to the largest candidates (adaptive area filter).
    max_area = max(area for _, area, _, _, _ in components)
    min_keep_area = max(80, int(max_area * 0.06))
    filtered = [(x, a, c, h, w) for (x, a, c, h, w) in components if a >= min_keep_area]

    # Guardrail: if still too many pieces, keep the largest likely digits.
    if len(filtered) > 12:
        filtered = sorted(filtered, key=lambda item: item[1], reverse=True)[:12]

    # Split very wide components (e.g. connected "1234") using vertical projection.
    expanded = []
    for x, area, crop, h, w in filtered:
        splits = _split_component_by_projection(crop)
        if len(splits) == 1:
            expanded.append((x, splits[0]))
            continue

        # Recreate approximate x-order from split offsets.
        cursor = x - (w / 2.0)
        for split_crop in splits:
            split_w = split_crop.shape[1]
            split_center = cursor + (split_w / 2.0)
            expanded.append((split_center, split_crop))
            cursor += split_w

    expanded.sort(key=lambda item: item[0])
    return [crop for _, crop in expanded]


def _crop_to_model_input(digit_component):
    """Pad digit component to square, resize to 28x28, and shape for model."""
    h, w = digit_component.shape
    size = max(h, w) + 8
    canvas = np.zeros((size, size), dtype='float32')
    y_offset = (size - h) // 2
    x_offset = (size - w) // 2
    canvas[y_offset:y_offset + h, x_offset:x_offset + w] = digit_component

    pil = Image.fromarray((canvas * 255).astype(np.uint8))
    pil = pil.resize((28, 28), Image.Resampling.BILINEAR)
    arr28 = np.array(pil).astype('float32') / 255.0
    return arr28.reshape(1, 28, 28, 1)


def _ocr_digits_with_tesseract(uploaded_file):
    """
    OCR-first path for multi-digit strings.
    Returns (text, digits, confidence) or (None, None, None) if OCR fails.
    """
    try:
        pil_img = Image.open(uploaded_file).convert('L')
    except Exception:
        return None, None, None

    gray = np.array(pil_img)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Build multiple preprocessed variants and keep the best OCR result.
    variants = []
    thresh1 = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 12
    )
    variants.append(255 - thresh1)  # white digits on dark background

    _, thresh2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    variants.append(255 - thresh2)

    kernel = np.ones((2, 2), np.uint8)
    variants.append(cv2.morphologyEx(variants[0], cv2.MORPH_CLOSE, kernel))

    best_text = ""
    best_conf = 0.0
    psm_modes = [7, 6, 8, 13]  # line / block / word / raw line

    for candidate in variants:
        for psm in psm_modes:
            config = f"--oem 3 --psm {psm} -c tessedit_char_whitelist=0123456789"
            raw_text = pytesseract.image_to_string(candidate, config=config)
            digits_only = re.sub(r"\D", "", raw_text)
            if not digits_only:
                continue

            data = pytesseract.image_to_data(
                candidate, config=config, output_type=pytesseract.Output.DICT
            )
            conf_vals = []
            for conf in data.get("conf", []):
                try:
                    val = float(conf)
                    if val >= 0:
                        conf_vals.append(val)
                except Exception:
                    continue
            avg_conf = float(np.mean(conf_vals)) if conf_vals else 0.0

            # Prefer longer numeric strings, then higher confidence.
            better = (
                len(digits_only) > len(best_text)
                or (len(digits_only) == len(best_text) and avg_conf > best_conf)
            )
            if better:
                best_text = digits_only
                best_conf = avg_conf

    if not best_text:
        return None, None, None

    digits = [int(ch) for ch in best_text]
    return best_text, digits, best_conf

@login_required(login_url='/login/')
def prediction_view(request):
    context = {
        'form': ImageUploadForm(),
        'overall_accuracy': overall_accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
    }

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            prediction_image = form.save(commit=False)

            # 1) OCR-first: much better for multi-digit real-world images.
            predicted_text, predicted_digits, confidence = _ocr_digits_with_tesseract(
                prediction_image.image
            )

            # 2) CNN fallback (MNIST-style) if OCR cannot read any digits.
            if not predicted_text:
                binary = _prepare_binary_image(prediction_image.image)
                digit_crops = _extract_digit_crops(binary)
                if not digit_crops:
                    digit_crops = [binary.astype('float32')]

                predicted_digits = []
                confidences = []
                for crop in digit_crops:
                    model_input = _crop_to_model_input(crop)
                    probs = keras_model.predict(model_input, verbose=0)[0]
                    predicted_digits.append(int(np.argmax(probs)))
                    confidences.append(float(np.max(probs) * 100.0))

                predicted_text = ''.join(str(d) for d in predicted_digits)
                confidence = float(np.mean(confidences))

            predicted_digit = predicted_digits[0] if predicted_digits else None

            # 3) Save prediction in DB
            prediction_image.predicted_digit = predicted_digit
            prediction_image.prediction_accuracy = confidence
            prediction_image.save()

            # 4) Render prediction + metrics
            context.update({
                'predicted_digit': predicted_digit,
                'predicted_text': predicted_text,
                'predicted_digits': predicted_digits,
                'accuracy': confidence,
                'image': prediction_image,
                'form': form,
            })
            return render(request, 'prediction.html', context)
        context['form'] = form
    else:
        context['form'] = ImageUploadForm()

    return render(request, 'prediction.html', context)


def user_signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Account created for {user.username}! You can now log in.")
            return redirect("user_login")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})

def user_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("Home")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def user_logout_view(request):
    logout(request)
    return redirect("index")

# --- PROFILE LOGIC ---

@login_required(login_url='/login/')
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    context = {
        'profile': profile,
        'user': request.user,
    }

    return render(request, 'profile.html', context)

@login_required(login_url='/login/')
def profile_edit_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile   # 🔥 THIS IS THE FIX
        )
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile_edit.html', {'form': form})


def upload_image_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            return HttpResponse("Upload successful!")
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})

def HomePage(request):
    return render(request,"Home.html")


@login_required(login_url='/login/')
def dashboard(request):
    total_predictions = PredictionImage.objects.count()
    last_prediction = PredictionImage.objects.last()

    avg_accuracy = PredictionImage.objects.aggregate(
        avg=Avg('prediction_accuracy')
    )['avg']

    recent_predictions = PredictionImage.objects.order_by('-id')[:5]

    context = {
        'total_predictions': total_predictions,
        'last_prediction': last_prediction,
        'avg_accuracy': round(avg_accuracy, 2) if avg_accuracy else 0,
        'recent_predictions': recent_predictions
    }

    return render(request, 'Dashboard.html', context)
