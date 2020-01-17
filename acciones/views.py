# acciones/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
# Utilizo esta clase pq el listado de acciones no funciona bien (con View) tal como se comenta en el video.
# Se crean y borran nuevos acciones pero al listar parece que la BDD no se haya modificiado.
# desde admin se puede comprabar que efectivamente los cambios si se han introducido en la BDD.
from django.views.generic import (
    ListView	
)

from .forms import AccionModelForm
from .models import Accion
from .models import all_products

#BASE VIEW CLASS = View
from .utils import (   # Rutinas con utilidades para leer .csv, crea htmls, etc
	FillTableStock_pd,
	FillTableStock,
	ReadStockCSV
)
from .utils_pd import (   # Rutinas con utilidades para leer .csv, crea htmls, etc
	ReadStockCSV_pd,
	#Get_EstadisticaPrecio,
)

from .utB_H import (   # Rutinas con utilidades para evaluar el precio: CAGR, std, etc
	GetParamPrecio
)

class AccionObjectMixin(object):
	model = Accion
	def get_object(self):
		id = self.kwargs.get('id')
		obj = None
		if id is not None:
			obj = get_object_or_404(self.model, id=id)
		return obj 

class AccionDeleteView(AccionObjectMixin,View):
	template_name = "acciones/accion_delete.html" # DetailView
	# def get_object(self):
		# id = self.kwargs.get('id')
		# obj = None
		# if id is not None:
			# obj = get_object_or_404(Accion, id=id)
		# return obj

	def get(self, request, id=None, *args, **kwargs):
		# GET method
		context = {}
		obj = self.get_object()
		if obj is not None:
			context['object'] = obj
		return render(request, self.template_name, context)

	def post(self, request, id=None,  *args, **kwargs):
		# POST method
		print('detete POST',request.POST)
		context = {}
		obj = self.get_object()
		if obj is not None:
			obj.delete()
			context['object'] = None
			return redirect('/acciones/') # <-- tras borrado, vuelta al listado de acciones
		return render(request, self.template_name, context)


class AccionUpdateView(AccionObjectMixin,View):
	template_name = "acciones/accion_update.html" # DetailView
	# def get_object(self):
		# id = self.kwargs.get('id')
		# obj = None
		# if id is not None:
			# obj = get_object_or_404(Accion, id=id)
		# return obj

	def get(self, request, id=None, *args, **kwargs):
		# GET method
		context = {}
		obj = self.get_object()
		if obj is not None:
			form = AccionModelForm(instance=obj)
			context['object'] = obj
			context['form'] = form
		return render(request, self.template_name, context)

	def post(self, request, id=None,  *args, **kwargs):
		# POST method
		context = {}
		obj = self.get_object()
		if obj is not None:
			form = AccionModelForm(request.POST, instance=obj)
			if form.is_valid():
				form.save()
			context['object'] = obj
			text['form'] = form
		return render(request, self.template_name, context)

class AccionCreateView(View):
	template_name = "acciones/accion_create.html" #DetailView
	def get(self, request, *args, **kwargs): # id=None (default)
		#GET method 
		print('11111111111111111111111111111111111')
		print(request.POST)
		form = AccionModelForm()
		context = {"form": form}
		return render(request, self.template_name, context) #return render(request, 'about.html',{})

	def post(self, request, *args, **kwargs): # id=None (default)
		#POST method 
		print('2222222222222222222222222222222222222')
		print(request.POST)
		form = AccionModelForm(request.POST)
		if form.is_valid():
			form.save()
			form = AccionModelForm() # <- limpia casilla de entrada despues de salvar
		context = {"form": form}
		return render(request, self.template_name, context) #return render(request, 'about.html',{})

# class AccionListView(View):
	# template_name = 'acciones/accion_list.html'
	# queryset = Accion.objects.all()
	
	# def get_queryset(self):
		# return self.queryset
	
	# def get(self, request, *args, **kwargs): 
		# context = {'object_list': self.get_queryset()} #self.queryset}
		# #print(context)
		# return render(request, self.template_name, context)

class AccionListView(ListView):
	template_name = 'acciones/accion_list.html'
	queryset = Accion.objects.all() 

class DatosListView(ListView):
	template_name = 'acciones/datos_list.html'
	queryset = all_products.objects.all() 
	
# class AccionListView(View):
	# template_name = 'about.html' # 'acciones/accion_detail.html' #DetailView
	# def get(self, request, *args, **kwargs): # id=None (default)
		# #GET method 
		# context = {} #                 {'object':self.get_object()}
		# return render(request, self.template_name, context) #return render(request, 'about.html',{})

#class MyListView(AccionListView)
#	queryset = Accion.objects.filter(id=1)
		
class AccionView(AccionObjectMixin, View):
	template_name = 'acciones/accion_detail.html' #DetailView
	def get(self, request, id=None, *args, **kwargs): # id=None (default)
		#GET method 
		itemBDD = self.get_object()
		context = {
			'object':itemBDD,
		}
		# context.update({
			# 'datos':[[1,2,3,4,"5"],						
						# [6,7,8,9,10]]
			# })
		# print(context["datos"])
		# print(context["datos"][0])
		print(f'Acción de la Base de datos: {itemBDD.tick}')

		NFile = itemBDD.tick+".MC diario 2000-2018.csv" # ".csv"
		print('Nombre del fichero',NFile)
		#ddm = ReadStockCSV(NFile)	# Lectura .csv por filas
		dd = ReadStockCSV_pd(NFile)# Lectura .csv con Lib pandas
		#print('desde views.py, FIELDS:',dd.columns)
		print('desde views.py, dd.head()\n',dd.head())
		print('desde views.py, dd.index\n',dd.index)
		
		#print('.loc\n',dd.loc[0:1])
		ddm = dd.values
		print ('matriz\n',ddm)
		#Tpy = FillTableStock_pd(dd)						# Llena la tabla a partir del dataframe leido con pandas
		Tpy = FillTableStock(dd.columns,ddm)			# Llena tabla con nombres columnas y array de datos
		#print(Tpy)
		
		#EstadP = Get_EstadisticaPrecio(dd) #,FInicio,FFin)
		
		Results_dict =  {'CAGR':8.34,'std_Y': 23.45}
		print('AccionView Results_dict:',Results_dict)
		print(itemBDD.tick,(itemBDD.tick).split())
		
		
		TRes = GetParamPrecio((itemBDD.tick).split(),dd)
		print('Tabla Estadisticas Precio\n')
		print(TRes)
		TResHTML = TRes.to_html()
		
		context.update({
			'results': Results_dict,
			'bdd_fields': dd.columns, # Nombres de las columnas
			'bdd_rows': dd, # datos de la accion
			'TRes': TRes, # resultados obtenidos para la serie de precios seleccionada
			'TResHTML': TResHTML, # resultados obtenidos para la serie de precios seleccionada
			'TABLApy': Tpy,
		})
		
		# if id is not None:
			# obj = get_object_or_404(accion, id=id)
			# context['object'] = obj
		return render(request, self.template_name, context) #return render(request, 'about.html',{})


# HTTP METHODS
def my_fbv(request, *args, **kwargs):
	print(request.method)
	return render(request, 'about.html', {})