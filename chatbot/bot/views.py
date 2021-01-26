

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
import json
# import requests
import random
from django.utils.decorators import method_decorator
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from .models import register,chat


def Chat(request):
    s = request.session.get('user')
    if s != None:
        r = register.objects.get(id=s)
        context = {'n': r.name}
        return render(request, 'chatbot.html', context)
    else:
        return redirect(login)

def respond_to_websockets(request,message):
    jokes = {
        'stupid': ["""Yo' Mama is so stupid, she needs a recipe to make ice cubes.""",
                   """Yo' Mama is so stupid, she thinks DNA is the National Dyslexics Association."""],
        'fat': ["""Yo' Mama is so fat, when she goes to a restaurant, instead of a menu, she gets an estimate.""",
                """ Yo' Mama is so fat, when the cops see her on a street corner, they yell, "Hey you guys, break it up!" """],
        'dumb': [
            """Yo' Mama is so dumb, when God was giving out brains, she thought they were milkshakes and asked for extra thick.""",
            """Yo' Mama is so dumb, she locked her keys inside her motorcycle."""]
    }

    result_message = {}
    s = request.session.get('user')
    r = register.objects.get(id=s)

    if message == 'fat':
        result_message['text'] = random.choice(jokes['fat'])
        c = chat.objects.get(user=r)
        count = c.fat
        c.fat = count+1
        c.save()

    elif message == 'stupid':
        result_message['text'] = random.choice(jokes['stupid'])
        c = chat.objects.get(user=r)
        count = c.stupid
        c.stupid = count + 1
        c.save()

    elif message == 'dump':
        result_message['text'] = random.choice(jokes['dumb'])
        c = chat.objects.get(user=r)
        count = c.dump
        c.dump = count + 1
        c.save()

    else:
        result_message = "I don't know any responses for that. If you're interested in yo mama jokes tell me fat, stupid or dumb."
    context = {'msg':result_message,'n':r.name}
    return render(request, 'chatbot.html', context)


def Register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        user = request.POST.get('user')
        pasw = request.POST.get('pasw')

        r = register(name=name, phone=phone, username=user, password=pasw)
        r.save()
        c = chat(user=r)
        c.save()
        return render(request,'userlogin.html')
    return render(request,'register.html')
def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pasw = request.POST.get('pasw')

        r = register.objects.filter(username=user, password=pasw)
        if r.exists():
            for i in r:
                request.session['user'] = i.id
                break
            return redirect(Chat)
        else:
            context = {'m':'Invalid username or password'}
            return render(request,'userlogin.html',context)
    return render(request, 'userlogin.html')

def logout(request):
    del request.session['user']
    return redirect(login)