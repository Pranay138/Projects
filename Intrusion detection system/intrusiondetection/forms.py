from django.forms import Form, CharField, FileField, PasswordInput


class UserForm(Form):

    username=CharField(max_length=50)
    name=CharField(max_length=50)
    password=CharField(widget=PasswordInput())
    conformpassword = CharField(widget=PasswordInput())
    email=CharField(max_length=50)
    mobile=CharField(max_length=50)

class LoginForm(Form):

    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())