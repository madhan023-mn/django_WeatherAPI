from django.shortcuts import render,redirect
from . import models
import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Create your views here.
def home(request):
    return render(request,'home.html')

#signup page
def signup(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')

        if password != cpassword:
            return render(request, "signup.html", {
                "error": "Passwords do not match."
            })
        
        models.Signup.objects.create(name=name,email=email,
                                     password=password,
                                     cpassword=cpassword)
        
        return redirect('login')
    return render(request,'signup.html')


def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=models.Signup.objects.filter(email=email,
                                          password=password).first()
        if user:
            print("User Name:", user.name)
            request.session['user_id'] = user.id
            request.session['name'] = user.name
            return redirect('weather')
        else:
            return render(request, "login.html", {
                "error": "Invalid Email or Password"
            })

    return render(request,'login.html')



def weather(request):
    print(request.session.get('user_id'))
    if 'user_id' not in request.session:
        return redirect('login')
    name = request.session.get('name')
    
    
    if request.method=="POST":
       

        city=request.POST.get('city')
        url='http://api.weatherapi.com/v1/current.json'
        query_param={
            'key':os.getenv("APIKEY"),
            'q':city
        }
        response=requests.get(url,params=query_param)
        if response.status_code==200:
            data=response.json()

            weather_data=models.Weather(city=data["location"]["name"],
            country = data["location"]["country"],
            temperature = data["current"]["temp_c"],
            humidity = data["current"]["humidity"],
            wind_speed = data["current"]["wind_kph"],
            weather_condition = data["current"]["condition"]["text"],)

            weather_data.save()

            records={
                'data':weather_data,
                'name':name
            }
            print(records)

            return render(request,'weather.html',records)
    return render(request,'weather.html',{'name':name})

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']

    if 'name' in request.session:
        del request.session['name']

    return redirect('login')