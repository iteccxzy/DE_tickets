from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *arg, **kwarg):
        if request.user.is_authenticated:
            return redirect ('/')
        else:
            return view_func(request, *arg,**kwarg)
    return wrapper_func
