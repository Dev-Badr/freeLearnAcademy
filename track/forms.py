from django import forms
from django.forms import widgets

class SearchForm(forms.Form):
    query = forms.CharField(label='',
		required = True,
		max_length = 63,
		widget = widgets.TextInput(
			attrs={
				'placeholder':"Search..",
				'name':"search", 
				"class":"form-control"
			}
		)
	)