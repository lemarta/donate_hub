from django import forms
from django.forms.fields import ChoiceField
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from donating.models import Category, Donation, Institution, CustomUser
from donating.serializers import DonationSerializer
from donating.forms import UserForm
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


class AddDonationView(LoginRequiredMixin, View):

    login_url = '/login'

    def get(self, request, *args, **kwargs):

        categories = Category.objects.all()
        organisations = Institution.objects.all()

        context = {
            'categories': categories,
            'organisations': organisations,
        }
        
        return render(request=request, template_name='form.html', context=context)


class SuccessView(View):

    def get(self, request, *args, **kwargs):

        context = {}
        return render(request=request, template_name='form-confirmation.html', context=context) 


class LoginView(View):
    def get(self, request, *args, **kwargs):

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
            if self.request.GET.get('next'): 
                return redirect(self.request.GET.get('next'))
            else:
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
 

class LogoutView(View):

    def get(self, request, *args, **kwargs):
        
        logout(request)

        return redirect("index")


class UserView(View):

    def get(self, request, *args, **kwargs):

        user = request.user

        user_donations_base = Donation.objects.filter(user=user)

        user_donations = []
        for user_donation in user_donations_base:
            donation_categories = user_donation.categories.all()
            user_donations.append((user_donation, donation_categories))

        form = UserForm(instance=user)

        context = {
            'form': form,
            'user_donations': user_donations,
        }

        return render(request, template_name='user.html', context=context)


class Donation2View(APIView):

        def post(self, request, *args, **kwargs):

            donation_serializer = DonationSerializer(data=request.data)
            if donation_serializer.is_valid():
                donation_serializer.save(user = request.user)
                return Response(donation_serializer.data)
            return Response(donation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
