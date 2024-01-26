from django.db import models

# Create your models here.

class Admin_log(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    
    def __str__(self):
        return self.username


class Authors(models.Model):
    author_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.author_name


class Books(models.Model):
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=200)
    author_name  = models.ForeignKey(Authors,on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.book_name
