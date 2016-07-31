from django.forms import ModelForm, Form
from django import forms
from models import RegisterMetadata
from mysite.forms import FormBase
from collections import OrderedDict
import json


class RegisterMetadataForm(ModelForm, FormBase):
    class Meta:
        model = RegisterMetadata
        fields = ('name', 'description', 'all_fields',)

    @property
    def list(self):
        #if not self.is_valid():
        #    raise Exception("list function need valid form")
        all_fields = self.get_all_fields()
        d = OrderedDict()
        d['name'] = all_fields['name']
        d['reg_form_url'] = self.instance.registerurl.URL
        return d




class RegisterForm(Form):
    def __init__(self, *args, **kwargs):
        custom_fields = kwargs.pop('custom_fields')
        super(RegisterForm, self).__init__(*args, **kwargs)
        for custom_field in custom_fields:
            self.fields[custom_field] = forms.CharField(max_length=100)

    def __unicode__(self):
        if self.is_valid():
            fields = {}
            for k, v in self.fields.iteritems():
                fields[k] = self.cleaned_data[k]
            return json.dumps(fields)
        else:
            return "RegisterForm"
