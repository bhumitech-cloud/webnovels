from bs4 import BeautifulSoup
import requests
from . import database
import mysql.connector
import time,random

def update_details():
    mydb = mysql.connector.connect(
    host="localhost",
    user="bhumit",
    password="admin123",
    database="novels"
    )
    mycursor = mydb.cursor()
    mycursor.execute("select novelID,title,url from test where url not in (select url from novelsdetails) and url like '%royalroad.com%';")
    myresult = mycursor.fetchall()
    session = requests.Session()
    for novels in myresult:
        novelID,title,url = novels
        tag_list = []
        start = time.time()
        page = session.get(url).text
        end = time.time()
        print("GET: ", end - start)
        soup = BeautifulSoup(page,'lxml')
        try:
            image = soup.find('div',class_ = 'col-md-3 hidden-sm hidden-xs text-center').find('img',src = True)["src"]
        except AttributeError:
            image = "no image"
            genre = "null"
            chapters = 0
            author = "null"
            description = "no description"
            update(novelID,title,url,chapters,author,genre,description,image)
            print("details inserted for: ", title)
            continue
        tags = soup.find('span',class_ = 'tags').find_all('a',class_ = "label label-default label-sm bg-blue-dark fiction-tag")
        for tag in tags:
            tag_list.append(tag.text)
        if len(tag_list) == 0:
            tag_list = ["Action"]
        genre = random.choice(tag_list)
        chapters = int(soup.find('table',id = "chapters")["data-chapters"])
        author = soup.find('h4').find_all('span')[1].text.strip("\n")
        description = (soup.find('div',class_ = "hidden-content").text.strip("\n"))[0:4950] + "..."
        database.create_novelsdetails(novelID,title,url,chapters,author,genre,description,image)
        print("details inserted for: ", title)


def scrap_novels(n):
    global url
    for pageno in range(1,n+1):
        page_url = url + str(pageno)
        page_data = requests.get(page_url).text
        print("pageno:" + str(pageno) + " Scrapped")
        soup = BeautifulSoup(page_data,'lxml')
        novel_object = soup.find_all('h2',class_ = 'fiction-title')
        for title in novel_object:
            add = "https://www.royalroad.com" + title.find('a',href = True)["href"]
            title = title.text.lstrip("\n").rstrip("\n")
            database.create_novels(title,add)
