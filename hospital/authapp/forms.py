from django.contrib.auth.models import User
from .models import SampleCollection, Profile
from django import forms

# from .models import Profile



class UserRegistration(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField()
    email = forms.EmailField(required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password','password2')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords doesn\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(required=True)
    aadhar_number = forms.CharField(required=True)
    class Meta:
        model = Profile
        fields = ('phone_number', 'aadhar_number')
        

class SampleCollectionForm(forms.ModelForm):
    class Meta:
        model = SampleCollection
        fields = ('age','fever','drycough','tiredness','difficultybreathing','chestpain','lossofspeech','date')