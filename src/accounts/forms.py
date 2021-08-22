from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models import Q

from .models import UserAccount


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ('email', 'username')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserLoginForm(forms.ModelForm):
    query = forms.CharField(label='Username or Email')
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        query = self.cleaned_data.get("query")
        password = self.cleaned_data.get("password")
        
        user_qs = UserAccount.objects.filter(
            Q(username=query) |
            Q(email=query)
        ).distinct().first()
        
        if not user_qs:
            raise forms.ValidationError("Invalid username/email or password")
        
        if not user_qs.is_active:
            raise forms.ValidationError("Inactive account")
        
        if not user_qs.check_password(password):
            raise forms.ValidationError("invalid username/email or password")
        
        return super(UserLoginForm, self).clean()

