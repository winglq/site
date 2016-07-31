from mysite.views import ViewBase
from django.forms import formset_factory
from models import RegisterMetadata, RegisterURL, RegisterResult
from forms import RegisterMetadataForm, RegisterForm
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
import uuid
import json
# Create your views here.


Reg_Formset = formset_factory(RegisterMetadataForm, extra=1)
class RegisterView(ViewBase):
    def create(self, request):
        form = RegisterMetadataForm(request.POST or None)
        if form.is_valid():
            reg_instance = form.save(commit=False)
            uid = uuid.uuid4()
            url = request.build_absolute_uri(reverse(new, args=(str(uid).replace('-',''),)))
            reg_instance.save()
            reg_url = RegisterURL(uuid=uid, URL=url, metadata=reg_instance)
            reg_url.save()
            return self.render(request, "register_create_success.html", {'url': url})
        else :
            return self.render(request, "register_create.html", {'form': form})

    def new(self, request, uuid):
        reg_url = get_object_or_404(RegisterURL, uuid=uuid)
        print str(reg_url.metadata.all_fields)
        print reg_url.metadata.name
        form = RegisterForm(request.POST or None, custom_fields=reg_url.metadata.all_fields.split())
        if form.is_valid():
            reg_result = RegisterResult(regurl=reg_url, results=str(form))
            reg_result.save()
            return self.render(request, "register_new_success.html", {})
        return self.render(request, "register_new.html", {'form': form})

    def list_registerred(self, request, uuid):
         reg_url = get_object_or_404(RegisterURL, uuid=uuid)
         reg_results = RegisterResult.objects.filter(regurl=reg_url)
         results = []
         for reg_result in reg_results:
             results.append(json.loads(reg_result.results))

         return self.render(request, "register_list_registerred.html", {'results': results})

    def list(self, request):
         all_meta = RegisterMetadata.objects.all()
         forms = []
         for meta in all_meta:
             form = RegisterMetadataForm(instance=meta)
             forms.append(form)
         return self.render(request, "list.html", {'forms': forms})


def create(request):
    return RegisterView().create(request)

def new(request, uuid):
    return RegisterView().new(request, uuid)

def list_registerred(request, uuid):
    return RegisterView().list_registerred(request,uuid)

def list(request):
    return RegisterView().list(request)
