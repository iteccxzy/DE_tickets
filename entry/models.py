from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Business(models.Model):
    id = models.AutoField(primary_key=True)
    bs = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    tel = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    foto =models.ImageField(default="profile.png",null=True, blank=True, upload_to='fotos')

    def __str__(self):
        return self.name

class Plans(models.Model):
    plan_id = models.IntegerField(primary_key= True)
    desc = models.CharField(max_length=200)
    
    def __str__(self):
        return self.desc

    class Meta:
        verbose_name_plural = "Plans"

class Offices(models.Model):
    ofi_id = models.AutoField(primary_key=True)
    business = models.ForeignKey('Business', on_delete = models.CASCADE)
    plan =    models.ForeignKey('Plans', models.DO_NOTHING, blank=True, null=True)
    desc = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.desc

    class Meta:
        verbose_name_plural = "Offices"



class Stocks(models.Model):
    st_id =     models.AutoField(primary_key=True)
    office =    models.ForeignKey('Offices', on_delete=models.CASCADE)
    plan =      models.ForeignKey('Plans', models.DO_NOTHING, blank=True, null=True)
    
    st_date=   models.DateField()
    st_time =   models.TimeField()
    state =     models.BooleanField(blank=True, null=True)
    qt =        models.IntegerField(blank=True, null=True)

class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Customers"

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    office = models.ForeignKey('Offices', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customers', on_delete= models.CASCADE)
    odate = models.DateField()
    otime =  models.TimeField() 


