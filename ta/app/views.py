from django.db.models import Count
from django.shortcuts import render,redirect
from django.views import View
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from . models import Customer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator




# Create your views here.
@login_required
def home(request):
    return render(request,"app/home.html")

@method_decorator(login_required,name='dispatch')
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()          
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations!User Registered Successfully")
        else:
            messages.warning(request,"Invalid data input")
        return render(request, 'app/customerregistration.html',locals())
    
@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form= CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            mobile =form.cleaned_data['mobile']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']

            reg=Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"congratulations!Profile Save Successfully")
        else:
            messages.warning(request,"Invalid data input")
        return render(request, 'app/profile.html',locals())

@login_required   
def address(request):
    add = Customer.objects.filter(user=request.user) 
    return render(request, 'app/address.html',locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form= CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        form= CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success (request, "Congratulations! Profile Update Successfully")
        else:
            messages.warning (request, "Invalid Input Data")
        return redirect("address")
    
