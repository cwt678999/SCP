from django import forms
from captcha.fields import CaptchaField

class RegisterForm(forms.Form):

    usertype = (
        ('competitor',"参赛选手"),
        ('organizer',"赛事主办方"),
    )
    username = forms.CharField(label="用户名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')
    type = forms.ChoiceField(label='用户类型',choices=usertype)