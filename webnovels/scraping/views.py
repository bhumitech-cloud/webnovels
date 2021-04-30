from django.shortcuts import render
from django.http import HttpResponse
from .models import sites
import mysql.connector

def login(request):
    return render(request,'login.html')

def scrap(request):
    if request.POST["username"] == 'bhumit' and request.POST["password"] =='bhum1234':
        mydb = mysql.connector.connect(
        host="localhost",
        user="bhumit",
        password="admin123",
        database="novels"
        )
        mycursor = mydb.cursor()
        mycursor.execute("select * from websites;")
        results = mycursor.fetchall()
        sitelist = []
        for result in results:
            site = sites()
            site.id,site.title,site.link = result
            sitelist.append(site)
        return render(request,'scraper.html',{'websites':sitelist})
    else:
        return HttpResponse('wrong username and password')