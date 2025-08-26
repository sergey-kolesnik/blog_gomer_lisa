from django.views.generic.base import TemplateView

class IndexPageView(TemplateView):
    template_name = "account/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context
    
class LoginView():
    pass

class RegisterView():
    pass