from django import forms


class CommentForm(forms.Form):
    content = forms.CharField()


class PostForm(forms.Form):
    content = forms.CharField()
    photo = forms.ImageField()