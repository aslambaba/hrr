from django import forms
# from .models import UploadedImage
from .models import Profile



from .models import PredictionImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = PredictionImage
        fields = ['image']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'job_title', 'bio', 'profile_picture']

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'job_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your job title'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write something about yourself'
            }),
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }

class UserProfileEditForm(forms.Form):
    """Simple profile edit form backing the MOCK_USER_DATA structure."""
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)