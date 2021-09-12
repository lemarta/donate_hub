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
from rest_framework.parsers import JSONParser


from donating.models import Category, Donation, Institution, CustomUser
from donating.serializers import DonationSerializer
from donating.forms import DonationForm, UserForm
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

    def post(self, request, *args, **kwargs):

        bags = request.POST.get('bags')
        category_id = request.POST.get('categories')
        organisation_id = request.POST.get('organisation')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone')
        city = request.POST.get('city')
        zip_code = request.POST.get('postcode')
        pick_up_date = request.POST.get('data')
        pick_up_time = request.POST.get('time')
        pick_up_comment = request.POST.get('more_info')
        user = request.user

        organisation = Institution.objects.get(id=organisation_id)
        category = Category.objects.get(id=category_id)

        donation = Donation.objects.create(
            quantity=bags, 
            institution=organisation,
            address=address, 
            phone_number=phone_number, 
            city=city, 
            zip_code=zip_code, 
            pick_up_date=pick_up_date, 
            pick_up_time=pick_up_time, 
            pick_up_comment=pick_up_comment,
            user=user,
            )

        donation.categories.add(category)
        donation.save()

        return redirect('success')



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

        form = UserForm(instance=user)

        return render(request, template_name='user.html', context={'form': form})




# class Donation2View(APIView):

#         # parser_classes = [JSONParser]

#         def put(self, request, id, format=None):
#             donation = self.get_obje0w(donation, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
