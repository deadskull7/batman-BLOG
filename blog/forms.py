from django import forms
from django.contrib.auth.models import User
from .models import Post, Comment, Contact
from pagedown.widgets import PagedownWidget
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    content=forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Post
        fields = ('title', 'content', 'image')


class CommentForm(forms.ModelForm):
    text=forms.CharField(widget=PagedownWidget())

    class Meta:
        model = Comment
        fields = ('author', 'text')


"""class ContactForm(forms.Form):
    name = forms.CharField(max_length=30, widget=forms.TextInput(
            attrs={
                'placeholder': 'Write your name here'
            })
        )
    email = forms.EmailField(max_length=254,widget=forms.TextInput(attrs={'placeholder': 'Write your email here'}))
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
    )
    

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')  """


class ContactForm(forms.ModelForm):
      class Meta:      
          model = Contact
          fields = '__all__'
          widgets = { 
            'comment': forms.Textarea(attrs={'placeholder': 'Tell Something'}),
          }  


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )



          