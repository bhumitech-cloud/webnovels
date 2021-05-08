from bs4 import BeautifulSoup
import requests
import time
import mysql.connector



def create(data):
    mydb = mysql.connector.connect(
    host="localhost",
    user="bhumit",
    password="admin123",
    database="novels"
    )
    mycursor = mydb.cursor()
    sql = "INSERT INTO chapters(novelID,chapterno,chapter_title,chapter_link) VALUES (%s,%s,%s,%s)"
    mycursor.executemany(sql, data)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def get_chapter(novelID,url):
    mydb = mysql.connector.connect(
    host="localhost",
    user="bhumit",
    password="admin123",
    database="novels"
    )
    start = time.time()
    page_data = requests.get(url).text
    end = time.time()
    print("request time:",end-start)
    soup = BeautifulSoup(page_data, 'lxml')
    data = []
    try:
        table_data = soup.find('table',id="chapters").find_all('td',class_ = False)
    except AttributeError:
        create([(novelID,0,"no chapters","no link")])
        return
    table_data = soup.find('table',id="chapters").find_all('td',class_ = False)
    if len(table_data) == 0:
        create([(novelID,0,"no chapters","no link")])
        return
    chapter_no = 1
    for tab in table_data:
        chapter = tab.text.split()
        chapter_title = ' '.join(chapter)
        chapter_link = "www.royalroad.com" + tab.find('a',href= True)["href"]
        data.append((novelID,chapter_no,chapter_title,chapter_link))
        chapter_no += 1
    create(data)


def scrap_chapters():
    mydb = mysql.connector.connect(
    host="localhost",
    user="bhumit",
    password="admin123",
    database="novels"
    )
    mycursor = mydb.cursor()
    session = requests.Session()
    mycursor.execute("select novelID,url from test where novelID not in (select novelID from chapters)and url like '%royalroad.com%';")
    myresult = mycursor.fetchall()
    for novels in myresult:
        get_chapter(novels[0], novels[1])
        print("chapters inserted for: ", novels[0])
