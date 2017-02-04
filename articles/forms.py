from models import Article
from django.forms import ModelForm, CharField
from django_summernote.widgets import SummernoteWidget
from django.utils.translation import ugettext_lazy as _


class ArticleForm(ModelForm):
    stags = CharField(max_length=100, required=False)
    class Meta:
        model = Article
        widgets = {'content': SummernoteWidget()}
        fields = ('title', 'stags', 'content')
