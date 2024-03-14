"""Admin_Book_Hub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, BookViewSet,AuthorsListView,BooksListView
from . import views

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('authors/', AuthorsListView.as_view(), name='api-authors-list'),
    path('books/', BooksListView.as_view(), name='api-books-list'),

    
    
    path('', views.login_admin,name='login_admin'),
    path('login_admin/',views.login_admin,name='login_admin'),
    path('home/',views.home,name='home'),
    path('books/',views.books,name='books'),
    path('add_author/',views.add_author,name='add_author'),
    path('add_books/',views.add_books,name='add_books'),
    
    
    
    path('author_edit/<int:id>',views.author_edit,name='author_edit'), 
    path('book_edit/<int:id>',views.book_edit,name='book_edit'), 
    path('author_edit_update/',views.author_edit_update,name='author_edit_update'),
    path('book_edit_update/',views.book_edit_update,name='book_edit_update'),
   

    path('author_delete/<int:id>',views.author_delete,name='author_delete'),
    path('author_book_delete/<int:id>',views.author_book_delete,name='author_book_delete'),
    
    


    path('author_details_view/<int:id>',views.author_details_view,name='author_details_view'),
    # path('author_search_result/',views.author_search_result,name='author_search_result'),
    path('author_details_view/<int:id>',views.author_details_view,name='author_details_view'),

    
    path('search_authors/',views.search_authors,name='search_authors'),
    path('search_books/',views.search_books,name='search_books'),
    
    
]
