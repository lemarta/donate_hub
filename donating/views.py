from django.shortcuts import render
from django.views import View

from donating.models import Donation, Institution

# Create your views here.


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        
        donations = Donation.objects.filter(quantity__isnull=False)
        organisations = Institution.objects.all()

        foundations = []
        ngos = []
        local_collections = []

        for organisation in organisations:
            if organisation.type == 1:
                foundations.append(organisation)
            elif organisation.type == 2:
                ngos.append(organisation)
            elif organisation.type == 3:
                local_collections.append(organisation) 


        total_donations = sum([int(donation.quantity) for donation in donations])
        total_organiations = sum([1 for _ in organisations])

        context = {
            'total_donations': total_donations,
            'total_organiations': total_organiations,
            'foundations': foundations,
            'ngos': ngos,
            'local_collections': local_collections,
            }
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