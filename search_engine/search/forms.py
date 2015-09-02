from django import forms

class search_form(forms.Form): 
	query = forms.CharField(label='Search',max_length=140)
	#All my attributes here