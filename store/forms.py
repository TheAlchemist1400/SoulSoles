from django import forms
from django.contrib.auth.models import User
from .models import SourcingRequest

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 150)
    password = forms.CharField(widget = forms.PasswordInput)
    
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
class SourcingRequestForm(forms.ModelForm):
    SIZE_OPTIONS = [
        ("4", "4"), ("4.5", "4.5"), ("5", "5"), ("5.5", "5.5"),
        ("6", "6"), ("6.5", "6.5"), ("7", "7"), ("7.5", "7.5"),
        ("8", "8"), ("8.5", "8.5"), ("9", "9"), ("9.5", "9.5"), ("10", "10")
    ]
    
    sizes = forms.MultipleChoiceField(
        choices = SIZE_OPTIONS,
        widget = forms.CheckboxSelectMultiple,
        required=True,
        label = "Select up to three sizes"
    )
    
    class Meta:
        model = SourcingRequest
        fields = ['sneaker_name', 'sizes']
        
    def clean_sizes(self):
        selected_sizes = self.cleaned_data.get("sizes") # Declare & initial seselected_data variable to sizes checked
        if len(selected_sizes) > 3:
            raise forms.ValidationError("You cannot select more than 3 sizes")
        return selected_sizes
        