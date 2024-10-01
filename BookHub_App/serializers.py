
from rest_framework import serializers
from .models import Authors, Books




class AuthorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authors
        fields = ['id', 'author_name', 'username', 'email']

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['book_id', 'book_name', 'author', 'created_date']
     