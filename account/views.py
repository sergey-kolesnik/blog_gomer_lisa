from django.views.generic.base import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth import login

from .forms import CustomUserCreationForm

class IndexPageView(TemplateView):
    template_name = "account/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context


class RegisterView(View):
    template_name = "account/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("blog:index")

    def get(self, request):
        form  = self.form_class()
        return render(request, self.template_name, {"form": form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        print(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(self.success_url)
        else:
            print(form.errors)
            return render(request, self.template_name, {"form": form})

class LoginView():
    pass

