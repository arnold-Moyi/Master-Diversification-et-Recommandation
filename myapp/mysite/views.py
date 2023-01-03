import email
from django.urls import reverse
from email.message import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from mysite.models import Contact
from .forms import ContactForm, SignUpForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from .token_generator import account_activation_token
from django.core.mail import EmailMessage
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

#importation for recommendation
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

from .models import Lieu, Rating

# Create your views here.
@login_required()
def dashboard(request):
    params = Lieu.objects.all()
    params['recommended']=recommmender(request)
    
    return render(request, 'base/dashboard/dashboard.html', params)
 
def home(request):
    
    return render(request, 'base/home.html')

def About(request):
    
    return render(request, 'base/About/about.html')

def Register(request):
    context = {}
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['firstname']
                last_name = form.cleaned_data['lastname']
                username = form.cleaned_data['username']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                
                user = User.objects.filter(email = email)
                if not user.exists():
                    user = User.objects.create_user( 
                        first_name = first_name,
                        last_name = last_name,
                        username = username,
                        email = email,
                        password = password)
                    
                    current_site = get_current_site(request)
                    email_subject = 'Activate Your Account'
                    message = render_to_string('base/activateCompte/activate_account.html', {
                        'user':user,
                        'domain':current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                        
                    })
                    to_email = form.cleaned_data.get('email')
                    emails = EmailMessage(email_subject, message, to=[to_email])
                    emails.content_subtype = "html"
                    emails.send()
                    
                    return HttpResponse('we have sent you an email, please confirm your email adress')
                
                else :
                    messages.error(request, 'this compt exist please change your email adress')
        else:
            if not request.user.is_authenticated:
                form = SignUpForm()
                context['form'] = form
                return render(request, 'base/register/register.html', context)
    else:
        return redirect(reverse('base/home'))


def activate_account(request, uidb64, token):
    
    uid = force_bytes(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    
    try:
        user = User.objects.get(pk =uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully, now you can to connect')
    else:
        return HttpResponse('Activation Link is invalid')


def Login(request):   
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)
            
            if not user:
                messages.error(request, 'username or password incorrect')
                
            else:
                login(request, user)
                return redirect(reverse('dashboard'))
            
        return render(request, 'base/login/login.html')
    
    else :
        return render(request, 'base/home.html')
        
    

def Logout(request):
    
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse, 'login')



def ContactUs(request):
    context = {}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            
            name = form.cleaned_data['username']
            mail = form.cleaned_data['mail']
            message = form.cleaned_data['message']
            
            Contact.objects.create(
                name = name,
                mail = mail,
                message = message
            )
            return HttpResponse('your message is send with succesfully')
    
    form = ContactForm()
    context['form'] = form    
    return render(request, 'base/contact/contactUs.html', context)

def generateRecommendation(request):  
    lieu = Lieu.objects.all()
    rating = Rating.objects.all()
    
    x = []
    y = []
    A = []
    B = []
    C = []
    D = []
    
    #Movie Data Frames
    for item in lieu:
        x=[item.id, item.name_place, item.adress, item.telephone, item.image.url, item.categories]
        y+=[x]
    lieux_df = pd.DataFrame(y, columns=['lieuId','namePlace', 'adress', 'telephone', 'image', 'categories'])
    print("Lieux DataFrame")
    print(lieux_df)
    print(lieux_df.dtypes)
    
    print("***********************************************************")
    #Rating Data Frames
    for item in rating:
        A = [item.user.id, item.lieu, item.rating]
        B+=[A]
    rating_df = pd.DataFrame(B, columns =['userid', 'lieuId', 'rating'])
    print("rating DataFrame")
   
    print(rating_df)
    print(rating_df.dtypes)
    
    if request.user.is_authenticated:
        userid = request.user.id
        
        userInput = Rating.objects.select_related('lieu').filter(user = userid)
        if userInput.count() == 0:
            recommmenderQuery = None
            userInput = None
       
          
      