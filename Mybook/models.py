from django.db import models
from django.db.models import Model
from django.contrib.auth.models import User
# Create your models here.
class books(models.Model):
    book_name = models.CharField(max_length=50)
    author = models.CharField(max_length=60)
    category= models.CharField(max_length=50)
    quantity = models.IntegerField()
    language = models.CharField(max_length=30)
    pages = models.IntegerField()
    book_published = models.IntegerField()
    summary = models.CharField(max_length=800)
    image = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)




    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url =''
        return url
    
   
    @property
    def imagetURL(self):
        try:
            url = self.image2.url
        except:
            url = ''
        return url


class Registerbook(models.Model):
    user_id = models.ForeignKey(User, on_delete= models.CASCADE, null=True, blank=True)
    book_id = models.ForeignKey(books, on_delete= models.CASCADE, null=True, blank=True)
    date_field = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    reg_status = models.IntegerField(default=1)


class Wishlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    book = models.ForeignKey(books, on_delete= models.CASCADE, null=True, blank=True)