from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_fun(request ,*args,**kwargs):
        if request.user.is_authenticated:
            print('decorator run')
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_fun