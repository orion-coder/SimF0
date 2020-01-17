# pages/views.py
from django.shortcuts import render,HttpResponse

# Create your views here.
def home_view(request,*args, **kwargs):  # *args, **kwargs propios de python
	print(args,kwargs)
	print(request.user,request)
	#return HttpResponse("<h2>Hi there, people!!<br>Django testing...</h2>") # string of HTML response
	return render(request,"home.html",{})

def about_view(request,*args, **kwargs):  # *args, **kwargs propios de python
	#return HttpResponse("<h2>About Page</h2>") # string of HTML response
	my_context={
		"titulo":"abc this is about me",
		"my_number": 123,
		"my_list": [12,23,245,"abc"],
		"my_html": "<h3>Texto HTML</h3>"
	}
	return render(request,"about.html",my_context)

def contact_view(request,*args, **kwargs):  # *args, **kwargs propios de python
	#return HttpResponse("<h2>Contact Page</h2>") # string of HTML response
	return render(request,"contact.html",{})
	
def sim0_view(request,*args, **kwargs):  # *args, **kwargs propios de python
	return render(request,"sim0.html",{})
	
def sistemas_view(request,*args, **kwargs):  # *args, **kwargs propios de python
	return render(request,"sistemas.html",{})
	
# activosHD--> gestionamos la pagina desde 
#  activosHD/views.py
#  activosHD/templates/activos/activo_list.html
#	Libs/utils.py -> rutinas genericas python
#
#def activosHD_view(request,*args, **kwargs):  # *args, **kwargs propios de python
#	return render(request,"activosHD.html",{})
