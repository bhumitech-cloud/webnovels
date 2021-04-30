from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return render(request,'login.html')



def scrap(request):
    if request.POST["username"] == 'bhumit' and request.POST["password"] =='bhum1234':
        return render(request,'scrapper.html')
    else:
        return HttpResponse('wrong username and password')