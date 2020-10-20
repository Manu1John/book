from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import books,Registerbook,Wishlist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth,User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import load_backend, login
import json
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
import requests
import base64
from PIL import Image
from base64 import decodestring
import binascii
from django.core.files import File
from django.core.files.base import ContentFile
from datetime import *
import datetime
 
# Create your views here.
def home(request):
    booklist = books.objects.all()
    return render(request, 'home.html', {'booklist': booklist})
   
   
def bookgrid(request):
    booklist = books.objects.all()
    category = category.objects.all()
    return render(request, 'category.html', {'booklist': booklist},{'category':category})



def categorysort(request,name):
    booklist = books.objects.all()
    return render(request, 'category.html', {'booklist': booklist,'cat':name})

def admin1(request):
    if request.session.has_key('username'):
        username=request.session['username']
        booklist = books.objects.all()
        return render(request, 'admin_panel.html', {'booklist':booklist})
    else:
        return render(request, 'adminlogin.html')

def admin2(request):
   
    # chart_order = []
    # for i in range(0,6):
    #     Reg =Registerbook.objects.filter(created_at__month = month-5+i)
    #     chart_order.append(Reg)
    Reg =Registerbook.objects.all()
    chart = Reg.count()
    context = {'chart':chart}
    return render (request, 'admin_report.html',context)

# for i in range(0,6):
#     chart_order = Order.objects.filter(date_orderd__year = year,date_orderd__month = month-5+i,complete=True)
#     order_total = 0
#     for items in chart_order:
#         try:
#             order_total += round(items.get_cart_total,2)
#         except:
#             order_total += 0
#     chart_values.append(round(order_total,2))        
# print(chart_values)


def admin3(request):
    user = Registerbook.objects.all()
    return render(request, 'admin_users.html', {'user':user})


def delete_user(request,id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('admin_users')


def user_login(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect(home)
        else:
            messages.error(request,'invalied username or password')
            return redirect('login')
    else:
        return render(request, 'login.html')

def user_logout(request):
    auth.logout(request)
    return redirect('home')
    
def sign_up(request):
    if request.method == 'POST':
        username =request.POST['username']
        email = request.POST['email']
        password1 =request.POST['password1']
        password2 = request.POST['password2']
        number = request.POST['number']
        dit = {'email' :email, 'username':username, 'number' :number}
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'Username is already taken')
                return render(request,'signup.html',dit) 
            elif User.objects.filter(email = email).exists():
                messages.error(request, 'Email is already taken')
                return render(request,'signup.html',dit)

            else:
                user =User.objects.create_user(username=username, email=email, password=password1, first_name=password1,last_name=number)
                user.save()
                number = request.POST['number']
                user=User.objects.get(last_name=number)
                print(user)
            
                if user:
                    username = user.username 
                    password=user.first_name
                    request.session['username'] =  username
                    request.session['password'] = password
                    

                    url = "https://d7networks.com/api/verifier/send"
                    number=str(91) + number
                    
                    payload = {'mobile': number,
                    'sender_id': 'SMSINFO',
                    'message': 'Your otp code is {code}',
                    'expiry': '900'}
                    files = [

                    ]
                    headers = {
                    'Authorization': 'Token 5c65fd70b87eef0d1f01b8538a5c49b025b9ebbf'
                    }

                    response = requests.request("POST", url, headers=headers, data = payload, files = files)

                    print(response.text.encode('utf8'))
                    data=response.text.encode('utf8')
                    datadict=json.loads(data.decode('utf-8'))

                    id=datadict['otp_id']
                    status=datadict['status']
                    print('id:',id)
                    request.session['id'] = id
                    return render(request,'otp.html')
        else:
            messages.error(request,'password is incorrect')
            return render(request,'signup.html',dit)
    
    else:

        return render(request,'signup.html')

def sign_up2(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method == 'POST':
        username = request.POST ['username']
        email = request.POST ['email']
        password1 = request.POST ['password1']
        password2 = request.POST ['password2']
        dic = {'username':username ,'email': email}
        if password1==password2:
            if User.objects.filter(username = username).exists():
                messages.error(request,'User Name is already taken')
                return render(request,'signup2.html',dic)      
            elif User.objects.filter(email = email).exists():
                messages.error(request, 'Email is already taken')
                return render(request,'signup2.html',dic)


            else:
                user=User.objects.create_user(username = username, email = email, password=password1)
                user.save()
                return redirect(user_login)
        else:
            messages.error(request,'Incorrect Password')
            return render(request, 'signup2.html',dic)
    else:
       return render(request,'signup2.html')






def admin_login(request):
    if request.session.has_key('username'):
        username=request.session['username']
        return redirect(admin1)
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == "manu" and password == "1234":
            request.session['username']=username
            return redirect(admin1)
        else:
            messages.error(request,'Invalid username or password')
            return render(request,'adminlogin.html')
    else:
        messages.error(request, 'Please Enter Username and password')
        return render(request, 'adminlogin.html')

def admin_logout(request):
    if request.session.has_key('username'):
        request.session.delete()
    else:
        pass
    return redirect(admin_login)


def add_books(request):
    if request.method == 'POST':        
            id = request.POST.get('id')
            book_name = request.POST.get('bookname')
            author = request.POST.get('author')
            category = request.POST.get('category')
            quantity = request.POST.get('quantity')
            language = request.POST.get('language')
            pages = request.POST.get('pages')
            book_published = request.POST.get('book_published')
            summary = request.POST.get('summary')
            image = request.FILES.get('myfile')
            image_data =request.POST['image64data']
            print('data', image_data)
            value = image_data.strip('data:image/png;base64,')
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),name='temp.' + ext)
            image2 = data
            post = books.objects.create(author=author,id=id,book_name=book_name,image=image,category=category,quantity=quantity,language=language,pages=pages,book_published=book_published,summary=summary, image2=image2)
            return redirect('admin_panel')
    else:
        return render(request,'add.html')


def update_books(request,id):
    booklist = books.objects.get(id=id)
    if request.method == 'POST':
        booklist.book_name =request.POST['bookname']
        booklist.author = request.POST['author']
        booklist.category = request.POST['category']
        booklist.quantity = request.POST['quantity']
        booklist.language = request.POST['language']
        booklist.pages = request.POST['pages']
        booklist.summary = request.POST['summary']
        booklist.book_published = request.POST['book_published']
        #booklist.image2 = request.FILES.get('mfile')
        
        
        if 'myfile' not in request.POST:
             image = request.FILES['myfile']
        else:
            image= booklist.image

        if 'mfile' not in request.POST:
            image2 = request.FILES['mfile']
        else:
            image2 = booklist.image2
        booklist.image2 = image2
        booklist.image=image
        booklist.save()
        
        return redirect('admin_panel')

    else:
        return render(request,'update.html' , {'booklist':booklist})


def delete_books(request,id):
    if request.method == 'GET':
        booklist = books.objects.get(id=id)
        booklist.delete()
        return redirect('admin_panel')

def book_view(request,id):
    booklist =books.objects.get(id=id)
    return render(request, 'bookview.html', {'booklist':booklist})

            


def mobile(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method=='POST':
        number = request.POST['number']
        user=User.objects.get(last_name=number)
        print(user)
       
        if user:
            username = user.username
            password=user.first_name
            request.session['username'] =  username
            request.session['password'] = password
            

            url = "https://d7networks.com/api/verifier/send"
            number=str(91) + number
            
            payload = {'mobile': number,
            'sender_id': 'SMSINFO',
            'message': 'Your otp code is {code}',
            'expiry': '900'}
            files = [

            ]
            headers = {
            'Authorization': 'Token 5c65fd70b87eef0d1f01b8538a5c49b025b9ebbf'
            }

            response = requests.request("POST", url, headers=headers, data = payload, files = files)

            print(response.text.encode('utf8'))
            data=response.text.encode('utf8')
            datadict=json.loads(data.decode('utf-8'))

            id=datadict['otp_id']
            status=datadict['status']
            print('id:',id)
            request.session['id'] = id
            return render(request,'otp.html')

        else:
            messages.error(request,'mobail number not registerd')
            return render(request,'mobile.html')
# {"otp_id":"6939d5de-8517-4788-b556-054404497e8d","status":"open","expiry":900}'
 
    return render(request,'mobile.html')


def otp(request):
    if request.user.is_authenticated:
        return redirect(home)
    if request.method=='POST':
        otp=request.POST['otp']
       
        id=request.session['id']
        url = "https://d7networks.com/api/verifier/verify"

        payload = {'otp_id': id,
        'otp_code': otp}
        files = [

        ]
        headers = {
        'Authorization': 'Token 5c65fd70b87eef0d1f01b8538a5c49b025b9ebbf'
        }

        response = requests.request("POST", url, headers=headers, data = payload, files = files)

        print(response.text.encode('utf8'))
        data=response.text.encode('utf8')
        datadict=json.loads(data.decode('utf-8'))
        status=datadict['status']
        
        if status=='success':
            username = request.session['username']   
            password =  request.session['password']
            per=authenticate(username=username,password=password)

            login(request,per)

            return redirect(home)

        
        else:
            messages.info(request,'incorrectotp')
            return render(request,'otp.html')

    return render(request,'otp.html')




#def wishlist(request): 
#return render(request,'wishlist.html')

def addtowishlist(request,id):
    x = datetime.datetime.now()
    M = x.strftime("%d/%m/%Y")
    StartDate = str(M)

    date_1 = datetime.datetime.strptime(StartDate, "%d/%m/%Y")
    end_date = date_1 + datetime.timedelta(days=10)

    print(end_date)

    k = end_date.strftime("%d/%m/%Y")
    print(k)
    book = books.objects.get(id=id)
    wishl, created = Registerbook.objects.get_or_create(user_id=request.user,book_id=book,reg_status=0)
    return redirect('/')

def cart(request):
    user = User.objects.get(username=request.user)
    wish = Registerbook.objects.filter(user_id=user,reg_status=0)
    return render(request,'cart.html',{'wishlist':wish})
    
        

def your_books(request):
   Reg =Registerbook.objects.filter(user_id=request.user,reg_status=1)
   return render(request, 'yourbooks.html', {'booklist':Reg})
   

def register_book(request,id):
   
    book = books()
    register = Registerbook()
    book = books.objects.get(id=id)
    print(book)
    date_field = request.POST.get('fdate')
    
    Registerbook.objects.create(user_id = request.user, book_id =book,  date_field=date_field )

        #register.save()

    Reg =Registerbook.objects.filter(user_id=request.user)
    return render(request, 'yourbooks.html', {'booklist':Reg})
   
    

def cart_delete(request,id):
    wish = Registerbook.objects.get(id=id)
    wish.delete()
    return redirect('/car')


def savecartitem(request):
    fg = request.POST.getlist("product_id[]")
    dg = request.POST.get("datef")
    print(dg)

    a = len(fg)
    # print(a)
    # print(fg[0])
    for i in range(0,a):
        wish = Registerbook.objects.get(id=fg[i])
        wish.reg_status = 1
        wish.date_field = dg
        wish.save()
        print(wish)
        # print(fg[i])

    # print(fg)
    return redirect("/")





