from django import forms

class MonitoringRequestForm(forms.Form):
	email = forms.EmailField(label="Email")

