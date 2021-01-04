from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .decorators.decorators import unauthenticated_user
from .forms.forms import RegisterUser
from .logics.url_checker import isValidURL
from .logics.shortner import *
from .models import Url, UserProfile
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

@login_required(login_url='loginU')
def home(request):

    return render(request,'home.html',)

@csrf_exempt
def getUrl(request):
    data = {}

    user = UserProfile.objects.get(id = request.user.id)
    if user.email_confirm != True:
        data['Url'] = 'error'
    else:
        data['Url'] = str(get_current_site(request)) + '/url/'
        url = request.POST.get('url')

        if isValidURL(url):
            print('valid url')
            s = Url.objects.last()
            if s is not None:
                id = s.uid + 1

                generated_link = idToShortURL(id)
            else:
                id = 1
                generated_link = idToShortURL(id)


            try:
                s = Url(original_link=url, generated_link=generated_link)
                s.save()
                data['Url'] = generated_link
            except:
                s = Url.objects.get(original_link=url)
                data['Url'] +=  s.generated_link
        else:
            print('Invalid url')
            data['Url']= 'your url is invalid'
    return JsonResponse(data)

def UrlDriver(request,url):
    id = shortURLToId(url)
    shortUrl = ''
    try:
        url = Url.objects.get(uid=id)
        url.visits +=1
        url.save()
        shortUrl = url.original_link
        print('generating id ',id)
    except:
        print('noting at id ',id)
        shortUrl = ''


    return redirect(shortUrl)

@unauthenticated_user
def Userlogin(request):
    if request.method == 'POST' or None:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(username+" "+password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'No Such User Found Create Account')
            return redirect('/register')

    return render(request,'login.html')

def register(request):
    form =  RegisterUser()
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            site = str(get_current_site(request)) + '/verifyEmail/' + username
            template = render_to_string('email.html', {'user': username,'site':site})
            email = EmailMessage(
                'Confirm Email for KillMyURl',
                template,
                settings.EMAIL_HOST_USER,
                [email],
            )
            email.fail_silently = False
            email.send()


            return redirect('loginU')
        else:
            print(form.cleaned_data)
            messages.add_message(request,messages.ERROR,form.errors)
            print('something went wrong with register form')
    return render(request,'register.html',context={'form':form})

@csrf_exempt
# @login_required(login_url='loginU')
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj = User.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@login_required(login_url='loginU')
def logoutUser(request):
    logout(request)
    return redirect('loginU')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

def verifyEmail(request,pk):
    if request.user.is_authenticated:
        logout(request)

    _User = User.objects.get(username = pk)
    _UserProfile = UserProfile.objects.get(user = _User)

    if request.method == 'POST':
        if _UserProfile.email_confirm == False:
            password = request.POST.get('password')
            user = authenticate(request, username=pk, password=password)
            if user is not None:
                _UserProfile.email_confirm = True
                _UserProfile.save()
                login(request, user)
                return redirect('home')
            else:
                messages.add_message(request,messages.ERROR,"Verification Failed... Use password which is used during registration")
        else:
            return HttpResponse('Invalid Request'+ str(_UserProfile.email_confirm))

    return render(request,'verifyUser.html')