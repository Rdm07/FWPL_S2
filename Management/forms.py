from django import forms
from django.conf import settings
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.forms import ModelForm
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from material import *
from models import *

from Player.models import Profile
from Management.models import *

class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Username', max_length=50)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False, initial=False,
                                     label='Remember Me')


class ProfileForm(UserCreationForm):

	first_name = forms.CharField(max_length=200, required=True)
	last_name = forms.CharField(max_length=200, required=True)
	email = forms.EmailField(required=True)

	def save(self, commit=True):
		user = super(ProfileForm, self).save(commit=False)
		user.email = self.cleaned_data.get('email')
		user.first_name = self.cleaned_data.get('first_name')
		user.last_name = self.cleaned_data.get('last_name')
		if commit:
			user.save()
		return user
	
	class Meta:
		model = Profile
		fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

class SPTAForm(forms.ModelForm):

	class Meta:
		model = SinglePlayerTeamAnswer
		exclude = ['for_question', 'by_player', 'points']

		widgets = {
			'bonus': forms.CheckboxInput(attrs={'class': 'filled-in'})
			}

class YNAForm(forms.ModelForm):

	class Meta:
		model = YesNoAnswer
		exclude = ['for_question', 'by_player', 'points']

		widgets = {
			'bonus': forms.CheckboxInput(attrs={'class': 'filled-in'})
			}

class WDLAForm(forms.ModelForm):

	class Meta:
		model = WinDrawLoseAnswer
		exclude = ['for_question', 'by_player', 'points']

		widgets = {
			'bonus': forms.CheckboxInput(attrs={'class': 'filled-in'})
			}

class SAForm(forms.ModelForm):

	class Meta:
		model = ScorelineAnswer
		exclude = ['for_question', 'by_player', 'points']

		widgets = {
			'bonus': forms.CheckboxInput(attrs={'class': 'filled-in'})
			}

class SIAForm(forms.ModelForm):

	class Meta:
		model = SingleIntegerAnswer
		exclude = ['for_question', 'by_player', 'points']

		widgets = {
			'bonus': forms.CheckboxInput(attrs={'class': 'filled-in'})
			}

class TAVAForm(forms.ModelForm):

	class Meta:
		model = TeamAndValueAnswer
		exclude = ['for_question', 'by_player', 'points']

		widgets = {
			'bonus': forms.CheckboxInput(attrs={'class': 'filled-in'})
			}

class SPTAForm_NoBonus(forms.ModelForm):

	class Meta:
		model = SinglePlayerTeamAnswer
		exclude = ['for_question', 'by_player', 'points']

		widgets = {
			'bonus': forms.CheckboxInput(attrs={'class': 'filled-in', 'disabled': 'True'})
			}

class YNAForm_NoBonus(forms.ModelForm):

	class Meta:
		model = YesNoAnswer
		exclude = ['for_question', 'by_player', 'points']

		widgets = {
			'bonus': forms.CheckboxInput(attrs={'class': 'filled-in', 'disabled': 'True'})
			}

class WDLAForm_NoBonus(forms.ModelForm):

	class Meta:
		model = WinDrawLoseAnswer
		exclude = ['for_question', 'by_player', 'points']

		widgets = {
			'bonus': forms.CheckboxInput(attrs={'class': 'filled-in', 'disabled': 'True'})
			}

class SAForm_NoBonus(forms.ModelForm):

	class Meta:
		model = ScorelineAnswer
		exclude = ['for_question', 'by_player', 'points']

		widgets = {
			'bonus': forms.CheckboxInput(attrs={'class': 'filled-in', 'disabled': 'True'})
			}

class SIAForm_NoBonus(forms.ModelForm):

	class Meta:
		model = SingleIntegerAnswer
		exclude = ['for_question', 'by_player', 'points']

		widgets = {
			'bonus': forms.CheckboxInput(attrs={'class': 'filled-in', 'disabled': 'True'})
			}

class TAVAForm_NoBonus(forms.ModelForm):

	class Meta:
		model = TeamAndValueAnswer
		exclude = ['for_question', 'by_player', 'points']

		widgets = {
			'bonus': forms.CheckboxInput(attrs={'class': 'filled-in', 'disabled': 'True'})
			}

