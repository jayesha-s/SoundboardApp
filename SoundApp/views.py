from time import time
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from gtts import gTTS
from playsound import playsound
#Added below packages
import os
from SoundApp.models import Buttons


def demo(request):
   return render(request,"demo.html")


def signup(request):
   return render(request, "signup.html")


def signup_user(request):
   if request.method == 'POST':
       username = request.POST['username']
       password = request.POST['password']


       try:
           user = User.objects.get(username = username)
           return redirect("/")
      
       except User.DoesNotExist:
           user = User.objects.create_user(username = username, password = password)
           user.save()
           auth.login(request,user) #Added this line
           return redirect("/home")
      
   return render(request, "signup.html")


def login(request):
   return render(request, "login.html")


def login_user(request):
   if request.method == 'POST':
           username = request.POST['username']
           password = request.POST['password']
          
           x = auth.authenticate(username = username, password = password)


           if x is None:
               return redirect("/signup")
           else:
               auth.login(request,x) #Added this line
               return redirect("/home")
   return render(request, "login.html")


def home(request): #completely changed this function
   if request.method == 'POST':
       if 'btn' in request.POST:
           audio_text = request.POST.get('btn')
           speech = gTTS(text = audio_text, lang = 'en', tld = 'com')
           unique_name =  str(request.user) + "_" + str(time()).replace('.','')
           file_name = f"{unique_name}.mp3";
           speech.save(file_name)
           playsound(file_name)
           os.remove(file_name)
   buttons_obj = Buttons.objects.filter(user_id=request.user.id)
   return render(request, "home.html", {'buttons_obj':buttons_obj})


def show_form(request):
   return render(request,"user_form.html")


def insert_text(request): #Added this function
   if('btn_name' in request.POST and 'text_to_speech' in request.POST and request.POST.get('text_to_speech')):
       button_record = Buttons(button_text=request.POST.get('btn_name'),audio_text=request.POST.get('text_to_speech'),user_id=request.user.id)
       button_record.save()
   return redirect("/home")
