from django.shortcuts import render
from django.views import View

# Create your views here.


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request=request, template_name='index.html', context=context)


class AddDonationView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request=request, template_name='form.html', context=context)


class LoginView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request=request, template_name='login.html', context=context)


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request=request, template_name='register.html', context=context)