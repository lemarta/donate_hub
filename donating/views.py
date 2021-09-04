from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.views import LoginView, FormView

from donating.models import Donation, Institution, CustomUser
# Create your views here.

User = get_user_model()


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
        
        # temporary
        logout(request)

        context = {}
        return render(request=request, template_name='login.html', context=context)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return redirect("register")

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, 'login.html')


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request=request, template_name='register.html', context=context)


    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            CustomUser.objects.create_user(first_name=name, last_name=surname, email=email, password= password)

            return redirect('/login')

        else:
            return HttpResponse("Passwords aren't matching") # temporary - will modify this later
 