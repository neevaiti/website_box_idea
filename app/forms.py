from django import forms

class IdeaForm(forms.Form):
    title = forms.CharField(label='Titre', max_length=200, widget=forms.TextInput)
    description = forms.CharField(label='Description', widget=forms.Textarea)

class CommentForm(forms.Form):
    text = forms.CharField(label='Commentaire', widget=forms.Textarea)