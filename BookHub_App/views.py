from django.shortcuts import render
from . models import Admin_log
from django.http import JsonResponse

# Create your views here.

def login_admin(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        is_admin=Admin_log.objects.filter(username=username,password=password)
        
        if is_admin:
            
            #for setting session
            
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
        return render(request,'Author_listing.html')
def books(request):
        return render(request,'Books_listing.html')
def add_author(request):
        return render(request,'Books_listing.html')
def add_books(request):
        return render(request,'Books_listing.html')
def author_details_view(request):
        return render(request,'Books_listing.html')