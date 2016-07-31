from models import Comment
from django.forms import ModelForm, TextInput, EmailInput, Textarea
from django_summernote.widgets import SummernoteWidget

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content',)
        widgets = {
            'name': TextInput(attrs={"placeholder": "Name"}),
            'email': EmailInput(attrs={"placeholder": "Email Address"}),
            'content': Textarea(attrs={"placeholder": "Comment",
                                       "rows": 2}),
            }

