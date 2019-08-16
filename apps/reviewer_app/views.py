from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt

def index(request):

    context = {
    	"all_users": User.objects.all()
    }

    return render(request, "reviewer_app/index.html", context)

def process(request):

    
    newuser = {
        'first_name': request.POST['form_first_name'],
        'last_name': request.POST['form_last_name'],
        'email': request.POST['form_email'],
        'password': request.POST['form_password'],
    }

    if len(newuser['first_name']) < 3:
        return redirect ("/")
    if len(newuser['last_name']) < 3:
        return redirect ("/")
    if len(newuser['email']) < 3:
        return redirect ("/")
    if len(newuser['password']) < 3:
        return redirect ("/")

    password = bcrypt.hashpw(newuser['password'].encode(), bcrypt.gensalt())
    User.objects.create(first_name=(newuser['first_name']),last_name=newuser['last_name'],email=newuser['email'],password=password.decode())
    request.session['first_name']=newuser['first_name']

    return redirect("/books")
    
def login(request):
    user ={
        'email': request.POST['form_email'],
        'password': request.POST['form_password'],
        'first_name': User.objects.get(email=request.POST['form_email']).first_name,
        'last_name': User.objects.get(email=request.POST['form_email']).last_name,
        'id': User.objects.get(email=request.POST['form_email']).id
    }
    account = User.objects.get(email=user['email'])
    if bcrypt.checkpw(user['password'].encode(), account.password.encode()):
        request.session['id'] = user['id']
        request.session['email'] = user['email']
        request.session['first_name'] = user['first_name']
        return redirect('/books')
    else:
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

# def books(request,id):    
def books(request):
    if 'email' not in request.session:
        return redirect('/')
    
    review_list = {
        "recent_reviews": Review.objects.all().order_by('-created_at')[:5],
        "all_reviews": Review.objects.all().order_by('-created_at')
        
    }

    all_books = {
        "books": Book.objects.all()
    }

    return render(request, "reviewer_app/books.html", review_list, all_books)

def show_book(request,id):
    
    book = Book.objects.get(id=id)
    reviews = Review.objects.filter(book=book).order_by('-created_at')
    context = {
        'book':book,
        'reviews':reviews
    }

    return render(request, "reviewer_app/show_book.html", context)

def show_user(request,id):
    user = User.objects.get(id=id)
    count = user.reviews.count()
    user_reviews = Review.objects.filter(reviewer=user)
    context = {
        'user':user,
        'count':count,
        'user_reviews':user_reviews
    }
    
    return render(request,'reviewer_app/show_user.html',context)


def show_add(request):

    review_list = {
        "all_reviews": Review.objects.all(),
        "all_books": Book.objects.all()
    }

    return render(request, "reviewer_app/add.html", review_list)

def add_process(request):
    if not Book.objects.filter(title=request.POST['form_title']).exists():

        book = Book.objects.create(title=request.POST['form_title'],author=request.POST['form_author'])
        
        Review.objects.create(review = request.POST['form_review'],rating=request.POST['form_rating'],reviewer=User.objects.get(id=request.session['id']),book=book)

    else:

        book = Book.objects.get(title=request.POST['form_title'])

        Review.objects.create(review = request.POST['form_review'],rating=request.POST['form_rating'],reviewer=User.objects.get(id=request.session['id']),book=book)

    return redirect('/books')

def delete_review(request):
    review_to_delete = request.POST['review_to_delete']
    delete_object = Review.objects.get(id=review_to_delete)

    delete_object.delete()

    return redirect('/books')