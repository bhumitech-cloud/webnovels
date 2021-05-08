from django.shortcuts import render
from django.http import HttpResponse
from .models import sites
from . import webnovel,royalroad,rrchapters,database
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

def insertNovel(request):
    id = int(request.GET["id"])
    url = request.GET["url"]
    if id == 1:
        title = url[30:]
        title = title[:title.index('_')]
        title = title.replace('-',' ')
        database.create_novels(title,url)
        webnovel.scrap_novelsdetails()
        webnovel.scrap_chapters()
        return HttpResponse("Srapping succesfull")
    elif id == 2:
        rev = url[::-1]
        index = 0 - rev.index('/')
        title =  url[index:].replace('-',' ')
        database.create_novels(title,url)
        royalroad.update_details()
        rrchapters.scrap_chapters()
        return HttpResponse("Srapping succesfull")
    else:
        return HttpResponse("Srapping unsuccessfull")