# HandWritten Digit Recognition - Detailed Documentation (Roman Urdu)

Ye documentation puray project ka detailed explanation hai Roman Urdu mein. Har important file kya role play kar rahi hai, kese kaam kar rahi hai, aur sab files mil ke kese ek complete web application banati hain - sab kuch step by step samjhaya gaya hai.

---

## Table of Contents

1. [Project Ka Introduction](#1-project-ka-introduction)
2. [Tech Stack (Konsi Technologies Use Hui)](#2-tech-stack-konsi-technologies-use-hui)
3. [Project Ka Folder Structure](#3-project-ka-folder-structure)
4. [Important Files Ka Detailed Explanation](#4-important-files-ka-detailed-explanation)
   - [4.1 `manage.py`](#41-managepy)
   - [4.2 `handWrittenDigitRecognition/settings.py`](#42-handwrittendigitrecognitionsettingspy)
   - [4.3 `handWrittenDigitRecognition/urls.py`](#43-handwrittendigitrecognitionurlspy)
   - [4.4 `handWrittenDigitRecognition/wsgi.py` aur `asgi.py`](#44-handwrittendigitrecognitionwsgipy-aur-asgipy)
   - [4.5 `HandWrittenApp/apps.py`](#45-handwrittenappappspy)
   - [4.6 `HandWrittenApp/admin.py`](#46-handwrittenappadminpy)
   - [4.7 `HandWrittenApp/models.py`](#47-handwrittenappmodelspy)
   - [4.8 `HandWrittenApp/forms.py`](#48-handwrittenappformspy)
   - [4.9 `HandWrittenApp/urls.py`](#49-handwrittenappurlspy)
   - [4.10 `HandWrittenApp/views.py` (sab se important file)](#410-handwrittenappviewspy-sab-se-important-file)
   - [4.11 `HandWrittenApp/migrations/`](#411-handwrittenappmigrations)
   - [4.12 `HandWrittenApp/Templates/` (HTML pages)](#412-handwrittenapptemplates-html-pages)
   - [4.13 `HandWrittenApp/static/`](#413-handwrittenappstatic)
   - [4.14 `CNN_Model.h5`](#414-cnn_modelh5)
   - [4.15 `db.sqlite3`](#415-dbsqlite3)
   - [4.16 `media/` folder](#416-media-folder)
5. [Pura Application Ka Flow (End to End)](#5-pura-application-ka-flow-end-to-end)
6. [Application Ko Locally Kese Run Karna Hai](#6-application-ko-locally-kese-run-karna-hai)
7. [Documentation Ko GitHub Par Kese Push Karna Hai](#7-documentation-ko-github-par-kese-push-karna-hai)

---

## 1. Project Ka Introduction

Ye ek **web application** hai jo user ki upload ki hui **handwritten digit image (0 se 9)** ko padh kar batati hai ke us image mein konsa number likha hua hai. App single digit hi nahi balke **multi-digit numbers** (jaise `123`, `4567`) bhi recognize karti hai.

System do techniques use karta hai:
- **OCR (Tesseract)** - pehle koshish karta hai ke image se digits text ki form mein nikal le.
- **CNN Model (TensorFlow/Keras)** - agar OCR fail ho jaye, to ye trained model image preprocess kar ke digit predict karta hai.

Sath sath app mein **user signup/login, profile management, aur ek dashboard** bhi hai jo total predictions, average accuracy, aur recent predictions show karta hai.

---

## 2. Tech Stack (Konsi Technologies Use Hui)

| Layer | Technology | Kaam |
|---|---|---|
| Backend Language | Python 3 | Saari logic |
| Web Framework | Django 5.2 | Routing, views, forms, auth, ORM |
| Frontend | HTML + Bootstrap 5 + Font Awesome | UI / Design |
| JavaScript | Bootstrap bundle JS | Navbar collapse waghera |
| Machine Learning | TensorFlow / Keras | `CNN_Model.h5` se digit prediction |
| OCR | pytesseract (Tesseract) | Image se digits read karna |
| Image Processing | OpenCV, Pillow (PIL), NumPy, SciPy | Image clean, threshold, resize |
| Metrics | scikit-learn | Accuracy / precision / recall / F1 |
| Database | SQLite (Django default) | User aur prediction record save |
| Form helpers | django-widget-tweaks | Templates mein form fields style karne ke liye |

---

## 3. Project Ka Folder Structure

```text
handWrittenDigitRecognition/                <- root folder (project)
├── manage.py                               <- Django ka command-line entry point
├── CNN_Model.h5                            <- Trained CNN model (Keras format)
├── db.sqlite3                              <- SQLite database file
├── ROMAN_URDU_DOCUMENTATION.md             <- ye documentation file
├── FIX_LONG_PATH_ISSUE.md                  <- Windows long-path fix notes
├── enable_long_paths.ps1                   <- PowerShell helper (Windows)
├── .gitignore                              <- git ko btanay ke kon si files ignore karni
│
├── handWrittenDigitRecognition/            <- main Django project package
│   ├── __init__.py
│   ├── settings.py                         <- saari project settings
│   ├── urls.py                             <- top-level URL routing
│   ├── wsgi.py                             <- WSGI entrypoint (production)
│   └── asgi.py                             <- ASGI entrypoint (async)
│
├── HandWrittenApp/                         <- ye actual Django app hai
│   ├── __init__.py
│   ├── apps.py                             <- app config
│   ├── admin.py                            <- Django admin registration
│   ├── models.py                           <- database tables (Profile, PredictionImage)
│   ├── forms.py                            <- HTML forms (image upload, profile edit)
│   ├── urls.py                             <- app ki apni URLs
│   ├── views.py                            <- saari business logic + ML/OCR yahan hai
│   ├── tests.py                            <- empty test file
│   ├── migrations/                         <- DB schema changes (auto generated)
│   ├── Templates/                          <- HTML pages
│   └── static/                             <- CSS, images, JS
│
└── media/                                  <- user uploaded images (predictions/, profiles/)
```

---

## 4. Important Files Ka Detailed Explanation

### 4.1 `manage.py`

**Role:** Ye Django ka **command-line utility** hai. Jab bhi koi Django command run karni ho (jaise `runserver`, `migrate`, `createsuperuser`), wo isi file ke through chalti hai.

**Kese kaam karti hai:**
1. Sab se pehle environment variable `TF_ENABLE_ONEDNN_OPTS=0` set karti hai taa ke TensorFlow ki oneDNN warnings na aayen.
2. `DJANGO_SETTINGS_MODULE` ko `handWrittenDigitRecognition.settings` par set karti hai - is se Django ko pata chalta hai k konsi settings file load karni hai.
3. Django ka `execute_from_command_line` call karti hai jo command-line arguments (`runserver`, `makemigrations` waghera) ko handle karta hai.

```1:35:manage.py
#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
Customized for: Handwritten Digit Recognition Project
- Suppresses TensorFlow oneDNN warnings
- Handles Django management tasks
"""
import os
import sys

def main():
    """Run administrative tasks."""
    
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'handWrittenDigitRecognition.settings')
    # ...
```

---

### 4.2 `handWrittenDigitRecognition/settings.py`

**Role:** Pure Django project ki **central configuration file**. Database, installed apps, middleware, templates, static/media paths - sab kuch yahan define hota hai.

**Important parts:**

- `BASE_DIR` - project root ka absolute path. Iss se baaki saare paths bante hain.
- `SECRET_KEY` - cryptographic signing key. Environment variable `DJANGO_SECRET_KEY` se ati hai, warna fallback dev key.
- `DEBUG = True` - development mode on hai (production mein `False` hona chahiye).
- `INSTALLED_APPS` - Django ko btata hai konsi apps active hain:
  - Default Django apps (`admin`, `auth`, `sessions`, etc.)
  - `widget_tweaks` - form rendering helper
  - `HandWrittenApp` - hamari apni app
- `MIDDLEWARE` - har HTTP request ke liye chalne wale layers (security, sessions, CSRF, auth).
- `TEMPLATES` - `DIRS: [BASE_DIR / 'Templates']` aur `APP_DIRS: True` - dono jagahon se templates dhondega.
- `DATABASES` - SQLite use ho rahi hai, file `db.sqlite3`.
- `STATIC_URL = 'statics/'` aur `MEDIA_URL = '/media/'`, `MEDIA_ROOT = BASE_DIR / 'media'` - user-uploaded images yahan store hoti hain.

---

### 4.3 `handWrittenDigitRecognition/urls.py`

**Role:** Project ka **top-level URL router**. Ye decide karta hai k konsa URL kis app ke paas jaye ga.

```1:14:handWrittenDigitRecognition/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('HandWrittenApp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Kaam:**
- `/admin/` - Django built-in admin panel.
- `/` (root) aur baaki sab URLs - `HandWrittenApp/urls.py` ko forward kar dete hain.
- DEBUG mode mein media files (uploaded images) ko serve karne ke liye `static(...)` add hota hai.

---

### 4.4 `handWrittenDigitRecognition/wsgi.py` aur `asgi.py`

**Role:** Ye production servers (Gunicorn, uWSGI, Daphne, etc.) ke **entry points** hain.

- `wsgi.py` - synchronous WSGI servers ke liye (jaise Apache + mod_wsgi, Gunicorn).
- `asgi.py` - asynchronous ASGI servers ke liye (jaise Daphne, Uvicorn).

Local development mein `runserver` use hota hai is liye in dono ka direct kaam nahi parta, but deployment ke liye zaruri hain.

---

### 4.5 `HandWrittenApp/apps.py`

**Role:** App ki **configuration class**. Django ko btata hai k `HandWrittenApp` ek installed app hai, aur kuch app-level settings define karta hai.

```1:7:HandWrittenApp/apps.py
from django.apps import AppConfig


class HandwrittenappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HandWrittenApp'
```

Yahaan `default_auto_field` set hai taa ke primary keys `BigAutoField` (64-bit integer) ho jayen.

---

### 4.6 `HandWrittenApp/admin.py`

**Role:** Django admin panel mein **konse models register karne** hain wo yahan likha jata hai.

```1:5:HandWrittenApp/admin.py
from django.contrib import admin
from .models import PredictionImage

admin.site.register(PredictionImage)
```

Is se admin panel mein `PredictionImage` table ka CRUD interface mil jata hai (image, predicted_digit, accuracy, created_at).

---

### 4.7 `HandWrittenApp/models.py`

**Role:** **Database tables ka structure** define karta hai. Django ORM se ye Python classes SQLite tables mein convert ho jati hain.

**Tables (Models):**

1. **`PredictionImage`** - har prediction ka record:
   - `image` - upload ki hui image (folder: `media/predictions/`)
   - `predicted_digit` - jo number predict hua (integer)
   - `prediction_accuracy` - kitne percent confidence se predict hua (float)
   - `created_at` - kab create hua (timestamp, auto)

2. **`UploadedImage`** - simple upload table (currently extra/backup):
   - `image`, `uploaded_at`

3. **`Profile`** - har Django user ka extra profile data:
   - `user` - Django ke built-in `User` se OneToOne link
   - `full_name`, `job_title`, `bio`
   - `profile_picture` - profile pic (folder: `media/profiles/`)

```5:30:HandWrittenApp/models.py
class PredictionImage(models.Model):
    image = models.ImageField(upload_to='predictions/')
    predicted_digit = models.IntegerField(null=True, blank=True)
    prediction_accuracy = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # ...

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
```

---

### 4.8 `HandWrittenApp/forms.py`

**Role:** **HTML forms** ko Python classes mein represent karta hai. Form validation aur saving ka kaam asaan ho jata hai.

**Forms:**

1. **`ImageUploadForm`** - `PredictionImage` model par based hai, sirf `image` field. Prediction page par image upload ke liye use hota hai.
2. **`ProfileForm`** - `Profile` model par based. `full_name`, `job_title`, `bio`, `profile_picture` fields ko Bootstrap classes ke sath render karta hai.
3. **`UserProfileEditForm`** - ek simple non-model form (`first_name`, `last_name`, `email`) jo mock data ke sath use hota tha.

---

### 4.9 `HandWrittenApp/urls.py`

**Role:** App ke andar saare URLs ka **routing table**. Har URL ek view function se jurra hua hai.

```7:21:HandWrittenApp/urls.py
urlpatterns = [
    path('', views.index_view, name='index'), 
    path('contact/', views.contact_view, name='contact'),
    path('prediction/', views.prediction_view, name='prediction'),
    path('signup/', views.user_signup_view, name='user_signup'),
    path('login/', views.user_login_view, name='user_login'),
    path('logout/', views.user_logout_view, name='user_logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('about/',views.about_view,name='about'),
    path('Home/',views.HomePage,name='Home'),
    path('Dashboard/', views.dashboard, name='dashboard'),
]
```

| URL | View | Kaam |
|---|---|---|
| `/` | `index_view` | Home page |
| `/about/` | `about_view` | About page |
| `/contact/` | `contact_view` | Contact page |
| `/prediction/` | `prediction_view` | Image upload + digit prediction |
| `/signup/` | `user_signup_view` | Naya account banana |
| `/login/` | `user_login_view` | Login form |
| `/logout/` | `user_logout_view` | Logout |
| `/profile/` | `profile_view` | Current user ka profile |
| `/profile/edit/` | `profile_edit_view` | Profile update |
| `/Home/` | `HomePage` | Login ke baad ka home alias |
| `/Dashboard/` | `dashboard` | Stats + recent predictions |

---

### 4.10 `HandWrittenApp/views.py` (sab se important file)

**Role:** Project ka **dimagh (brain)**. Har request handle karne wala function yahan hai - chahe wo simple page rendering ho ya complex CNN/OCR prediction logic.

#### A) Top par imports aur model loading

```13:30:HandWrittenApp/views.py
import numpy as np
import tensorflow as tf
from PIL import Image
from scipy import ndimage
import cv2
import pytesseract
import re
from django.db.models import Avg
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

kbe_keras_model = None

from keras.models import load_model

keras_model = load_model('CNN_Model.h5',
    custom_objects={'softmax_v2': tf.nn.softmax})
```

**Yahan kya ho raha hai:**
- Image processing aur ML libraries import hoti hain.
- `keras_model = load_model('CNN_Model.h5', ...)` - server start hote hi trained CNN model RAM mein load ho jata hai. Iska faida ye hai k har request par dobara load nahi karna parta (fast prediction).
- `custom_objects={'softmax_v2': tf.nn.softmax}` - ye is liye dia gaya hai k model ki training mein softmax custom name se save hui thi.

#### B) Simple page views

- `index_view` - `Home.html` render karta hai.
- `about_view` - `about.html`.
- `contact_view` - `Contact.html`.
- `HomePage` - same as index, just legacy URL ke liye.

#### C) Image Preprocessing Helper Functions

##### `_prepare_binary_image(uploaded_file)`
Image ko load karta hai aur **binary map** (0/1 ka grid) bana deta hai jahan digit ke pixels `1` hote hain aur background `0`.

Steps:
1. PIL se grayscale (`'L' mode`) image load.
2. NumPy array banata hai aur 0-1 range mein normalize.
3. Agar image background bright hai (`mean > 0.5`), to invert kar deta hai - because MNIST style mein digit white aur background black hota hai.
4. Adaptive threshold lagata hai (mean + 0.15 * std).
5. `binary_closing` + `fill_holes` se chhote chhote holes band karta hai.

##### `_split_component_by_projection(component)`
Agar koi digit-component bohat **chaurra** (wide) hai (jaise `123` saath jurra hua), to is function ko use kar ke vertical projection (har column ka sum) nikal kar gaps dhondta hai aur digits ko alag pieces mein split karta hai.

##### `_extract_digit_crops(binary_image)`
Binary image se **individual digits ko alag** karta hai:
1. `scipy.ndimage.label` se connected components dhondta hai.
2. Noise filter karta hai (bohat chhote ya bohat sparse components reject).
3. Har component ka x-center nikalta hai taa ke baad mein left-to-right order kar sake.
4. Wide components ko `_split_component_by_projection` se split karta hai.
5. Final left-to-right order mein digit crops return karta hai.

##### `_crop_to_model_input(digit_component)`
Ek digit crop ko **CNN model ke liye ready** karta hai:
1. Square canvas mein center karta hai (padding ke sath).
2. PIL se 28x28 pixel par resize.
3. Float32 mein 0-1 normalize.
4. Shape `(1, 28, 28, 1)` mein reshape (model ki expected input shape).

##### `_ocr_digits_with_tesseract(uploaded_file)`
**OCR-based fast path**. Multi-digit real-world images mein zyada accurate hota hai.
1. Image ko grayscale + Gaussian blur karta hai.
2. **Multiple preprocessed variants** banata hai: adaptive threshold, Otsu, morphological closing.
3. **Multiple PSM modes** (`7, 6, 8, 13`) ke sath Tesseract chalata hai.
4. Sirf digits `0-9` whitelist karta hai (`tessedit_char_whitelist=0123456789`).
5. Sab combinations mein se **longest + highest confidence** wala result chunta hai.
6. Return: `(text, list_of_digits, confidence)` ya agar fail ho to `(None, None, None)`.

#### D) Main Prediction View

```269:328:HandWrittenApp/views.py
@login_required(login_url='/login/')
def prediction_view(request):
    # ...
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
                # ...
                for crop in digit_crops:
                    model_input = _crop_to_model_input(crop)
                    probs = keras_model.predict(model_input, verbose=0)[0]
                    predicted_digits.append(int(np.argmax(probs)))
                    confidences.append(float(np.max(probs) * 100.0))

                predicted_text = ''.join(str(d) for d in predicted_digits)
                confidence = float(np.mean(confidences))

            # 3) Save prediction in DB
            prediction_image.predicted_digit = predicted_digit
            prediction_image.prediction_accuracy = confidence
            prediction_image.save()
            # 4) Render prediction + metrics
            # ...
```

**Step by step flow:**
1. `@login_required` decorator: agar user logged-in nahi to `/login/` par redirect.
2. GET request par empty `ImageUploadForm` ke sath `prediction.html` render karta hai.
3. POST request par:
   - Form validate hoti hai.
   - `commit=False` se model object banata hai but DB mein save nahi karta abhi.
   - **Pehle OCR try karta hai** (`_ocr_digits_with_tesseract`).
   - Agar OCR fail kare to **CNN fallback** chalata hai: image → binary → split digits → har digit ko 28x28 mein resize → model ko de kar predict → average confidence calculate.
   - Predicted digit aur accuracy `PredictionImage` mein save karta hai.
   - Result `prediction.html` mein show karta hai.

#### E) Authentication Views

- **`user_signup_view`** - Django ke built-in `UserCreationForm` use kar ke naya user banata hai. Success message dikha kar login page par bhej deta hai.
- **`user_login_view`** - `AuthenticationForm` se username+password validate karta hai aur `login()` call kar ke session start karta hai. Success par `Home` page par.
- **`user_logout_view`** - `logout()` call kar ke session khatam, phir index page par.

#### F) Profile Views

- **`profile_view`** - logged-in user ka `Profile` object `get_or_create` se nikalta hai (agar nahi hai to ban jata hai), `profile.html` render karta hai.
- **`profile_edit_view`** - `ProfileForm` ko existing `Profile` instance ke sath bind kar ke render karta hai. POST par save kar ke profile page par redirect.

#### G) Dashboard View

```402:420:HandWrittenApp/views.py
@login_required(login_url='/login/')
def dashboard(request):
    total_predictions = PredictionImage.objects.count()
    last_prediction = PredictionImage.objects.last()

    avg_accuracy = PredictionImage.objects.aggregate(
        avg=Avg('prediction_accuracy')
    )['avg']

    recent_predictions = PredictionImage.objects.order_by('-id')[:5]
    # ...
```

Database queries chala kar **statistics** nikalta hai:
- Total kitni predictions hui
- Aakhri prediction
- Average accuracy
- Last 5 predictions

Aur `Dashboard.html` mein cards + table form mein show karta hai.

---

### 4.11 `HandWrittenApp/migrations/`

**Role:** Django models mein jo bhi changes hote hain, un ko track karne ke liye **migration files** auto-generate hoti hain. Ye SQL ki tarah lekin Python mein likhi hoti hain. `python manage.py makemigrations` se banti hain aur `python manage.py migrate` se database par apply hoti hain.

Is project mein 9 migrations hain:
- `0001_initial.py` - shuru ke `UserLogin` aur `UserSignup` models (purane).
- `0002` - field renames.
- `0003` - more renames.
- `0004_predictionimage_delete_userlogin...` - `PredictionImage` model add hua, purane custom auth models remove hue (kyunke ab Django ka built-in `User` use ho raha hai).
- `0005`, `0006` - `image` field changes.
- `0007_uploadedimage_remove_predictionimage_image...` - structure refinements.
- `0008_profile.py` - **`Profile` model add hua**.
- `0009_rename_uploaded_at_predictionimage_created_at...` - column rename to `created_at`.

In sab ko run karne ke baad `db.sqlite3` mein final tables ban jati hain.

---

### 4.12 `HandWrittenApp/Templates/` (HTML pages)

**Role:** Saare **HTML templates** yahan hain. Django template language use hoti hai jis mein `{% %}` se logic aur `{{ }}` se variables aate hain.

| Template | Role |
|---|---|
| `Index.html` | **Base layout** - navbar, footer, Bootstrap/CSS includes. Baaki saare pages `{% extends "Index.html" %}` kar ke isko inherit karte hain. |
| `Home.html` | Landing page - project ka intro, features, hero section. |
| `about.html` | About us page - project ki tafseel. |
| `Contact.html` | Contact form / contact info. |
| `Login.html` | Login form (`AuthenticationForm` render karta hai). |
| `Signup.html` | Signup form (`UserCreationForm` render karta hai). |
| `Prediction.html` | Image upload form + result section + model metrics table. |
| `profile.html` | Current user ka profile show karta hai. |
| `profile_edit.html` | Profile edit form. |
| `Dashboard.html` | Statistics cards + recent predictions table. |

**Example - `Prediction.html` ka flow:**
- Left side: file upload form (CSRF token ke sath POST).
- Right side: agar `image` context mein hai to uploaded image show, agar `predicted_text` hai to bara number dikhata hai, sath confidence percentage.
- Neeche performance metrics table (accuracy/precision/recall/F1) - agar values context mein available hon to.

---

### 4.13 `HandWrittenApp/static/`

**Role:** **CSS, JavaScript aur images** jaisi static files. Browser ke liye sidha serve hoti hain.

Andar do folders hain:
- `static/Statics/` - CSS files (jaise `static.css`, `Home.css`, `prediction.css`, `dashboard.css`) jo templates mein `{% static 'Statics/...' %}` ke through load hoti hain.
- `static/Images/` - logos, icons waghera.

Settings mein `STATIC_URL = 'statics/'` set hai.

---

### 4.14 `CNN_Model.h5`

**Role:** Pre-trained **Convolutional Neural Network model** jo MNIST-style handwritten digits par train hua hai. Ye Keras (HDF5) format mein save hai (`.h5` extension is liye).

**Input:** 28x28 grayscale image, shape `(1, 28, 28, 1)`, values 0-1.
**Output:** 10 probabilities (digit 0 se 9 ke liye).

Server start hote hi ye `views.py` mein RAM mein load ho jata hai aur baad mein har CNN prediction call par use hota hai. Iska size approx 1.3 MB hai.

---

### 4.15 `db.sqlite3`

**Role:** **SQLite database file**. Django automatic is mein tables banata hai jab migrations run hoti hain. Single file mein puri database aa jati hai, koi separate DB server install karne ki zaroorat nahi.

Is mein ye tables hain:
- `auth_user` - Django ke built-in users (signup/login)
- `HandWrittenApp_predictionimage` - har upload ki hui prediction ka record
- `HandWrittenApp_profile` - user profiles
- `HandWrittenApp_uploadedimage` - secondary upload table
- Django ki internal tables (sessions, migrations, content types, etc.)

> Note: `.gitignore` mein `db.sqlite3` shamil hai is liye ye repo mein push nahi hoti. Har machine apna local DB rakhti hai.

---

### 4.16 `media/` folder

**Role:** **User-uploaded files** yahan store hote hain. Settings mein `MEDIA_ROOT = BASE_DIR / 'media'` aur `MEDIA_URL = '/media/'` set hai.

Subfolders:
- `media/predictions/` - jab user prediction page par image upload karta hai to yahan save hoti hai.
- `media/profiles/` - profile pictures.

DEBUG mode mein `urls.py` mein `static(...)` add hone ki wajah se ye images browser mein serve ho jati hain.

---

## 5. Pura Application Ka Flow (End to End)

Maan lo ek naya user pehli baar app khol raha hai:

1. **User browser mein `http://127.0.0.1:8000/` kholta hai.**
   - `manage.py runserver` Django ko start karta hai.
   - Top-level `urls.py` request ko `HandWrittenApp/urls.py` ko forward karta hai.
   - `index_view` chalti hai aur `Home.html` (`Index.html` ko extend kare bagair direct) render hoti hai.

2. **User Signup button par click karta hai.**
   - URL `/signup/` → `user_signup_view`.
   - `UserCreationForm` show hota hai.
   - User username + password de kar submit karta hai.
   - Form validate ho kar `auth_user` table mein record save kar deta hai.
   - Redirect to `/login/`.

3. **Login.**
   - `/login/` → `user_login_view` → `AuthenticationForm`.
   - Successful login par session bana kar `Home` page par redirect.

4. **User Prediction page par jata hai.**
   - `/prediction/` → `prediction_view`.
   - Kyunke `@login_required` laga hai, agar logged-in nahi ho to `/login/` par bhej deta hai.
   - Agar logged-in hai to upload form show hota hai (`Prediction.html`).

5. **User digit image upload karta hai.**
   - Browser POST request bhejti hai (multipart/form-data).
   - `ImageUploadForm` validate hoti hai aur file `media/predictions/` mein save ho jati hai.
   - Server par:
     - **Pehle Tesseract OCR** chalti hai. Multiple thresholding variants + PSM modes try ho kar best digit string nikalti hai.
     - **Agar OCR fail hui** to image preprocess hoti hai (binary map → digit components → split → 28x28 resize) aur har crop ko `keras_model.predict` se predict kiya jata hai.
   - Final predicted digit aur confidence `PredictionImage` row mein save ho jate hain.
   - Result `Prediction.html` mein render hota hai - bara number, individual digits, confidence percentage.

6. **User Dashboard par jata hai.**
   - `/Dashboard/` → `dashboard` view.
   - DB queries chalti hain: total predictions count, last prediction, average accuracy, last 5 predictions.
   - `Dashboard.html` cards + table mein dikha deta hai.

7. **User Profile dekh/edit kar sakta hai.**
   - `/profile/` → `Profile` automatically `get_or_create` se ban jata hai pehli baar.
   - `/profile/edit/` par `ProfileForm` se name, job title, bio, profile picture update.

8. **Logout** - `/logout/` → session destroy → index page.

---

## 6. Application Ko Locally Kese Run Karna Hai

### Step 1 - Repository clone karen (agar already nahi ki)

```bash
git clone https://github.com/aslambaba/hrr.git
cd hrr
```

### Step 2 - Virtual environment banaen

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### Step 3 - Required packages install karen

Project mein `requirements.txt` mojood nahi, is liye manually install karen:

```bash
pip install --upgrade pip
pip install django==5.2 django-widget-tweaks
pip install tensorflow keras
pip install opencv-python pillow numpy scipy
pip install pytesseract
pip install scikit-learn
```

### Step 4 - Tesseract OCR install karen (system level)

`pytesseract` sirf wrapper hai, asli Tesseract engine alag se install karna parta hai:

- **macOS:** `brew install tesseract`
- **Ubuntu/Debian:** `sudo apt-get install tesseract-ocr`
- **Windows:** [Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki) se install karen.

### Step 5 - Database migrations chalaen

```bash
python manage.py migrate
```

Ye `db.sqlite3` file bana ke saari tables create kar dega.

### Step 6 - (Optional) Admin user banaen

```bash
python manage.py createsuperuser
```

### Step 7 - Server start karen

```bash
python manage.py runserver
```

Browser mein khol kar:
- App: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

Bas, ab app chal rahi hai. Signup → Login → Prediction page → image upload → result.

> Note: Agar Windows par `[Errno 2] No such file or directory` waghera ki errors aaye to `FIX_LONG_PATH_ISSUE.md` aur `enable_long_paths.ps1` dekhen.

---

## 7. Documentation Ko GitHub Par Kese Push Karna Hai

Project pehle se hi GitHub repo `https://github.com/aslambaba/hrr.git` se connected hai. Sirf documentation file commit kar ke push karni hai.

Terminal mein project root mein ja kar ye commands chalaen:

```bash
git status
git add ROMAN_URDU_DOCUMENTATION.md
git commit -m "docs: add detailed Roman Urdu documentation"
git push origin main
```

Agar credentials maang raha ho:
- Username: aapka GitHub username
- Password: GitHub **Personal Access Token** (PAT). Settings → Developer settings → Personal Access Tokens → Generate new token (classic) → `repo` scope → token copy kar ke password field mein paste karen.

Push hone ke baad GitHub par documentation visible ho jaye gi: `https://github.com/aslambaba/hrr/blob/main/ROMAN_URDU_DOCUMENTATION.md`.

---

### Ek Line Mein Sara Project

"Mera project Django + Python + TensorFlow/Keras + Tesseract OCR par based ek web app hai jo user ki upload ki hui handwritten image se single ya multi digit numbers recognize karta hai aur har prediction ko SQLite database mein save kar ke dashboard par statistics show karta hai."
