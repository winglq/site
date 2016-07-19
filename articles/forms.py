from models import Article
from django.forms import ModelForm
from django_summernote.widgets import SummernoteWidget


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        widgets = {'content': SummernoteWidget()}
        fields = ('title', 'content')
