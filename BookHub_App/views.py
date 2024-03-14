from django.shortcuts import render,redirect
from . models import Admin_log,Authors,Books
from rest_framework import viewsets
from .serializers import AuthorsSerializer, BooksSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# Create your views here.

def login_admin(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        is_admin=Admin_log.objects.filter(username=username,password=password)
        
        if is_admin:
            
            #session
            
             admin_details=Admin_log.objects.get(username=username,password=password)
             username=admin_details.username 
             request.session['admin_session']=username
             
             #end
             
             return render(request,'Author_listing.html')
        
        else:
             error_message="Invalid credentials"
             return render(request,'Admin_login.html',{'error_message':error_message})
    else:
        return render(request,'Admin_login.html')
          
         
def home(request):
    authors_list=Authors.objects.all()
    return render(request,'Author_listing.html',{'authors_list':authors_list})


def books(request):
    books_list = Books.objects.all()
    return render(request, 'Books_listing.html', {'books_list': books_list})
    
def add_author(request):
  
 if request.method == 'POST':
    author_name = request.POST.get('name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    
    if Authors.objects.filter(email=email).exists():
        error_message = "An author with this email already exists."
        return render(request, 'Add_Author.html', {'error_message': error_message})

    elif Authors.objects.filter(username=username).exists():
        error_message = "This username already exists."
        return render(request, 'Add_Author.html', {'error_message': error_message})
    
    
    elif not (username[0].isalpha() and '_' in username):
            error_message = "Username must start with a letter and contain an underscore."
            return render(request, 'Add_Author.html', {'error_message': error_message})


    else:
        Authors(author_name=author_name, username=username, email=email).save()
        return redirect('home')
 else:
    return render(request,'Add_Author.html')


        
def add_books(request):
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        book_name = request.POST.get('bookname')

        if not author_name or not book_name:
            error_message = "Author name and Book name are required."
            return render(request, 'Add_Book.html', {'error_message': error_message})

        try:
            author = Authors.objects.get(author_name=author_name)
        except Authors.DoesNotExist:
            error_message = f"Author with name {author_name} does not exist."
            return render(request, 'Add_Book.html', {'error_message': error_message})
        
        if Books.objects.filter(author=author, book_name__icontains=book_name).exists():
            error_message = f"Book '{book_name}' already exists for author '{author_name}'."
            return render(request, 'Add_Book.html', {'error_message': error_message})

        Books(author=author, book_name=book_name).save()

        return redirect('books')

    return render(request, 'Add_Book.html')


    


def author_details_view(request,id):
    
    author=Authors.objects.get(id=id)

    author_name=author.author_name
    username=author.username
    email=author.email
  
    booksss=Books.objects.filter(author=author)
    print(booksss,"aswathi")
   

    return render(request, 'Author_details_view.html',{'books':booksss,'author_name':author_name,'username':username,'email':email})
   
      
def author_edit(request,id):
    author_id=Authors.objects.get(id=id)
    print(author_id)

    context = {
    'id':author_id.id,
    'author_name':author_id.author_name,
    'username':author_id.username  ,
    'email':author_id.email
    }
    print(context)

    return render(request,'author_edit.html',context)

def book_edit(request,id):
    author_id=Books.objects.get(book_id=id)
    

    context = {
    'id':author_id.book_id,
    'author_name':author_id.author,
    'book_name':author_id.book_name
   
    }
    
    return render(request,'book_edit.html',context)

def author_edit_update(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        author_name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')

  
        if not (username[0].isalpha() and '_' in username):
            error_message = "Username must start with a letter and contain an underscore."
            
            context = {
                'error_message': error_message,
                'id': id,
                'author_name': author_name,
                'username': username,
                'email': email,
            }
            return render(request, 'Author_edit.html', context)

     
        else:
            author_data = Authors.objects.get(id=id)
            author_data.author_name = author_name
            author_data.username = username
            author_data.email = email
            author_data.save()

            return redirect('home')

    else:
        return render(request, 'author_edit.html')
    
def book_edit_update(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        author_name = request.POST.get('authorname')
        book_name = request.POST.get('bookname')

  
        book_data = Books.objects.get(book_id=id)
        
        # book_data.author  = author_name
        book_data.book_name = book_name
        book_data.save()

        return redirect('books')

    else:
        return render(request, 'book_edit.html')
    
def author_delete(request,id):
    data=Authors.objects.get(id=id)
    data.delete()
    return redirect('home')

def author_book_delete(request,id):
    data=Books.objects.get(book_id=id)
    data.delete()
    return redirect('books')


def search_authors(request):  
    if request.method == 'POST':   
        name=request.POST.get('name') 
        print(name)
      
        
        if not name.isalpha():
            message = "Invalid author name. Please enter only alphabetic characters."
            return render(request, 'Author_listing.html', {'msge': message})

        data= Authors.objects.filter(author_name__icontains=name)
        print(data)
        
        if data:
         return render(request,'author_search_result.html',{'data':data})   
        else: 
            msge="Sorry no results found "          
            return render(request,'Author_listing.html',{'msge':msge})
        
    else:
            return render(request,'Author_listing.html')


def search_books(request):  
    if request.method == 'POST':   
        bookname = request.POST.get('bookname') 

        if bookname:
            data = Books.objects.filter(book_name__icontains=bookname)
            
            if data:
                return render(request, 'books_search_result.html', {'data': data})
            else: 
                msge = "Sorry no results found."
                return render(request, 'books_search_result.html', {'msge': msge})
        else:
            msge = "Please enter a book name."
            return render(request, 'books_search_result.html', {'msge': msge})
        
    else:
        return render(request, 'Books_listing.html')
    
    
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer

class AuthorsListView(generics.ListAPIView):
    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['author_name', 'username', 'email']
    search_fields = ['author_name', 'username', 'email']
    

class BooksListView(generics.ListAPIView):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['book_name', 'author__author_name']
    search_fields = ['book_name', 'author__author_name']
    template_name = 'books_listing.html'

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        # Check the request content type to determine the response type
        if request.accepted_renderer.format == 'html':
            return render(request, self.template_name, {'books_list': serializer.data})
        else:
            return Response(serializer.data)