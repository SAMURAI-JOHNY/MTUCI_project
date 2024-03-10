from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label="Имя")
    usermail = forms.EmailField(label="email")