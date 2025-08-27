from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'account-page__form-input', 'placeholder': ('Your Name')})
        )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'account-page__form-input', 'placeholder':('Your Email')})
        )
    
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'account-page__form-input', 'placeholder': ('Password')})
        )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'account-page__form-input', 'placeholder': ('Confirm Password')})
        )
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is busy")
        return email
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        
        if commit:
            user.save()
        return user