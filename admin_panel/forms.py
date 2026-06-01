from django import forms
from django.contrib.auth.password_validation import validate_password
from core.models import User


class AdminProfileForm(forms.ModelForm):
    """Admin profile: username, email, profile picture."""
    class Meta:
        model = User
        fields = ['username', 'email', 'profile_pic']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and self.instance:
            if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('This email is already in use.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and self.instance:
            if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('This username is already in use.')
        return username


class AdminPasswordChangeForm(forms.Form):
    """Admin change password (forgot / update)."""
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Current password'}),
        label='Current Password'
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}),
        validators=[validate_password],
        label='New Password'
    )
    new_password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}),
        label='Confirm New Password'
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        pwd = self.cleaned_data.get('current_password')
        if pwd and not self.user.check_password(pwd):
            raise forms.ValidationError('Current password is wrong.')
        return pwd

    def clean(self):
        data = super().clean()
        if data.get('new_password') != data.get('new_password_confirm'):
            raise forms.ValidationError('New passwords do not match.')
        return data

    def save(self):
        self.user.set_password(self.cleaned_data['new_password'])
        self.user.save(update_fields=['password'])
