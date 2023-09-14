from django.shortcuts import render,redirect
from django.views.generic import CreateView,FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login

from myapp.models import User
from myapp.form import RegistrationForm,SignInForm

# Create your views here.
class SignUpView(CreateView):
    model=User
    template_name="register.html"
    form_class=RegistrationForm
    success_url=reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request,"Account has been created")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request,"failed to create an account")
        return super().form_invalid(form)
    

class SignInView(FormView):
    model=User
    form_class=SignInForm
    template_name="login.html"
    
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                messages.success(request,"login successfully")
                return redirect("register")
            messages.error(request,"login failed")
        return render(request,self.template_name,{"form":form})