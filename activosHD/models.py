# activosHD/models.py
from django.db import models
from django.urls import reverse
import csv

# Create your models here.
class Activo(models.Model):
	tick			= models.CharField(max_length=120)
	nombre		= models.CharField(max_length=120,blank=True,null=True)
	industria	= models.CharField(max_length=120,blank=True,null=True)
	sector		= models.CharField(max_length=120,blank=True,null=True)
	subsector	= models.CharField(max_length=120,blank=True,null=True)
	pais			= models.CharField(max_length=120,blank=True,null=True)
	description = models.TextField(blank=True,null=True)
	# cotizacion Fecha O H L C V   ¿Esto seria otra class o struct
	# dividendos Fecha D

#	def populate
	
	def get_absolute_url(self):
		#return f"/products/{self.id}"
		return reverse("activos:activos-detail", kwargs={"id": self.id}) # f"/products/{self.id}"	

#class StockTS:
class all_products(models.Model):
    def get_all_products():
        items = []
        #with open('EXACT FILE PATH OF YOUR CSV FILE','r') as fp:
        with open('BDD/','r') as fp:
            # You can also put the relative path of csv file
            # with respect to the manage.py file
            reader1 = csv.reader(fp, delimiter=',')
            for value in reader1:
               items.append(value)
        return items
		  
