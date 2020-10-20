from django.urls import path
from .import views

urlpatterns = [
    path ('', views.home, name='home'),
    path('login', views.user_login, name='login'),
    path('user_logout', views.user_logout, name ='user_logout'),
    path('signup', views.sign_up, name = 'signup'),
    path('sign_up2', views.sign_up2, name = 'sign_up2'),
    path('admin_panel', views.admin1, name ='admin_panel'),
    path('adminlogin', views.admin_login, name='admin_login'),
    path('admin_logout', views.admin_logout, name = 'admin_logout'),
    path('add', views.add_books, name = 'add'),
    path('update/<int:id>/', views.update_books, name = 'update_books'),
    path('delete/<int:id>/', views.delete_books, name = 'delete_books'),
    path('book_view/<int:id>/', views.book_view, name = 'book_view'),
    path('categorysort/<str:name>/', views.categorysort, name ='categorysort'),
    path('admin_users', views.admin3, name = 'admin_users'),
    path('mobile', views.mobile, name = 'mobile'),
    path('otp', views.otp, name = 'otp'),
    path('yourbooks', views.your_books, name = 'yourbooks'),
    path('register_book/<int:id>/', views.register_book, name = 'register_book'),
    path('deleteuser/<int:id>/', views.delete_user, name = 'delete_user'),
    path('car', views.cart, name ='cart'),
    path('addtowishlist/<int:id>',views.addtowishlist,name="addtowishlist"),
    path('cart_delete/<int:id>/',views.cart_delete,name="cart_delete"),
    path('savecartitem/',views.savecartitem,name="savecartitem"),
    path('admin_report', views.admin2, name = 'admin_report')
]
