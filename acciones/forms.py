# acciones/forms.py
from django import forms
from .models import Accion

class AccionModelForm(forms.ModelForm):
	class Meta:
		model = Accion
		fields = [
			'tick'
		]
		
	def clean_tick(self):
		tick = self.cleaned_data.get('tick')
		if tick.lower() == 'abc':
			raise forms.ValidationError("This is not a valid tick")
		return tick