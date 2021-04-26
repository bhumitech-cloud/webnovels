from django.db import models

# Create your models here.
class novels():
    id : int
    title : str
    img : str
    author :str
    genre : str
    link : str
    description :str
    chapter: str
    
class chapter():
    no :int
    title: str
    link:str