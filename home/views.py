from models import HomeArticle
from mysite.views import ViewBase
# Create your views here.
class HomeView(ViewBase):
    def index(self, request):
        article = list(HomeArticle.objects.all())[-1].article
        return self.render(request, "index.html", {'article': article})
def index(request):
    hv = HomeView()
    return hv.index(request)
