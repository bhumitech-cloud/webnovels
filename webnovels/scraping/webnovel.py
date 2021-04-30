from bs4 import BeautifulSoup
import requests
import time
from . import database
import mysql.connector

url = "https://www.webnovel.com/category/0_novel_page"

def scrap_novelsdetails():
    mydb = mysql.connector.connect(
        host="localhost",
        user="bhumit",
        password="admin123",
        database="novels"
        )
    mycursor = mydb.cursor()
    session = requests.Session()
    mycursor.execute("select novelID,title,url from test where url not in (select url from novelsdetails) and url like '%webnovel.com%';")
    myresult = mycursor.fetchall()
    for novels in myresult:
        id,title,url = novels
        start = time.time()
        page = session.get(url).text
        end = time.time()
        print("Session: ", end- start)
        soup = BeautifulSoup(page,'lxml')
        novel_object = soup.find('div',class_ = 'det-info g_row c_000 fs16 pr')
        image = "https:" + novel_object.find('img',src = True)["src"]
        genre = novel_object.find('a',title = True)["title"]
        try:
            chapters =  int(novel_object.find('p',class_="mb12 lh24 det-hd-detail c_000 fs0").find_all('span')[-2].text.replace(" Chapters","").replace(",",""))
        except ValueError:
            chapters = 0
        author = novel_object.find('p',class_ = "ell dib vam").text.lstrip("Author: ").split("Translator")[0]
        try:
            description = (str(soup.find_all('p',class_="c_000")[2]).replace("<br/>","\n").replace('<p class="c_000">','').replace('</p>',''))[0:4950] + "..."
        except IndexError:
            description = "No description"
        database.create_novelsdetails(id,title,url,chapters,author,genre,description,image)
        print("details inserted for: ", title)

def scrap_novels(n):
    mydb = mysql.connector.connect(
        host="localhost",
        user="bhumit",
        password="admin123",
        database="novels"
        )
    for pageno in range(1,n+1):
        #time.sleep()
        page_url = url + str(pageno)
        page_data = requests.get(page_url).text

        print("pageno:" + str(pageno) + " Scrapped")

        soup = BeautifulSoup(page_data,'lxml')
        novel_object = soup.find_all('h3',class_ = 't_sub1 ell mb4')

        for title in novel_object:
            add = "https://www.webnovel.com" + title.find('a',href = True)["href"]
            database.create_novels(title.text,add)

def get_chapter(novelID,url):
    url = url + "/catalog"
    page_data = requests.get(url).text
    soup = BeautifulSoup(page_data, 'lxml')
    try:
        chapter_title = soup.find( 'div', class_="j_catalog_list" ).find_all( 'a' )
    except AttributeError:
        data = [(novelID,0,"no chapters","no link")]
        create(data)
        return
    data = []
    while chapter_title[0].text.split()[0] != '1':
        chapter_title.pop(0)
    for chapters in chapter_title:
        t = chapters.text.split()
        no = int(t[0])
        title = ' '.join(t[1:-2])
        link = chapters["href"].lstrip("//")
        data.append((novelID, no, title, link))
    for dat in data:
        print(dat)
    database.create_chapters(data)

def scrap_chapters():
    mydb = mysql.connector.connect(
        host="localhost",
        user="bhumit",
        password="admin123",
        database="novels"
        )
    mycursor = mydb.cursor()
    session = requests.Session()
    mycursor.execute("select novelID,url from test where novelID not in (select novelID from chapters)and url like '%webnovel.com%';")
    myresult = mycursor.fetchall()
    for novels in myresult:
        get_chapter(novels[0], novels[1])
        print("chapters inserted for: ", novels[0])
