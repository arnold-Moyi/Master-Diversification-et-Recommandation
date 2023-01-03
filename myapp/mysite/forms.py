from django import forms


class SignUpForm(forms.Form):
    firstname = forms.CharField(
        widget = forms.TextInput(
            attrs = {'class':'form-control', 'input_type':'text', 'id':'firstname',}
        )
    )
    lastname = forms.CharField(
        widget= forms.TextInput(
            attrs = {'class':'form-control', 'input_type':'text', 'id':'lastname'}
        )
    )
    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {'class':'form-control', 'input_type':'text', 'id':'username'}
        )
    )
    email = forms.EmailField(
        widget = forms.EmailInput(
            attrs = {'class':'form-control', 'input_type':'email', 'id':'email'}
        )
    )
    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {'class':'form-control', 'input_type':'password', 'id':'password'}
        )
    )
    
    
class ContactForm(forms.Form):
    name = forms.CharField(
        widget = forms.TextInput(
            attrs = {'class':'form-control-contact', 'input_type':'text', 'id':'name'}
         )
    )
    mail = forms.EmailField(
    widget = forms.EmailInput(
        attrs = {'class':'form-control-contact', 'input_type':'email', 'id':'email'}
        )
    )
    message = forms.CharField(
        widget = forms.Textarea(
            attrs = {'class':'form-control-contact', 'input_type':'text', 'id':'message'}
        )
    )
    
    