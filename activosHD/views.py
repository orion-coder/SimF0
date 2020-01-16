# activosHD/views.py
import pandas as pd
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# Create your views here.

from django.views import View
# Utilizo esta clase pq el listado de acciones no funciona bien (con View) tal como se comenta en el video.
# Se crean y borran nuevos acciones pero al listar parece que la BDD no se haya modificiado.
# desde admin se puede comprobar que efectivamente los cambios si se han introducido en la BDD.
from django.views.generic import (
    ListView	
)

#from .forms import AccionModelForm
from .models import Activo
from .models import all_products

from Libs.utils import ( # Rutinas con utilidades para leer .csv, crea htmls, etc
	TestMult,
	GetFolderNames,
	GetFileNamesinFolder,
	Close_FileScrapping, #(LCARTERA,dataPath),
	Fechas_CARTERA, #(LCARTERA),
)

#BASE VIEW CLASS = View
# from .utils import (   # Rutinas con utilidades para leer .csv, crea htmls, etc
	# FillTableStock_pd,
	# FillTableStock,
	# ReadStockCSV
# )
# from .utils_pd import (   # Rutinas con utilidades para leer .csv, crea htmls, etc
	# ReadStockCSV_pd,
	##Get_EstadisticaPrecio,
# )

# from .utB_H import (   # Rutinas con utilidades para evaluar el precio: CAGR, std, etc
	# GetParamPrecio
# )

class ActivoObjectMixin(object):
	model = Activo
	def get_object(self):
		id = self.kwargs.get('id')
		obj = None
		if id is not None:
			obj = get_object_or_404(self.model, id=id)
		return obj 

#class ActivoListView(ListView):
#	template_name = 'activos/activo_list.html'
#	queryset = Activo.objects.all() 
class ActivoListView(ListView):
	template_name = 'activos/activo_list.html'
	def get(self, request, id=None, *args, **kwargs): # id=None (default)

		#if request.method == "POST":
			#name = request.POST['myvalue']
			#print(name)
			#print('request.POST:',request.POST)
	
		Results_dict =  {'CAGR':8.34,'std_Y': 23.45}
		print('ActivoView Results_dict:',Results_dict)
		#print(itemBDD.tick,(itemBDD.tick).split())
		
		
		# TRes = GetParamPrecio((itemBDD.tick).split(),dd)
		# print('Tabla Estadisticas Precio\n')
		# print(TRes)
		# TResHTML = TRes.to_html()
		
		# context.update({
			# 'results': Results_dict,
			# 'bdd_fields': dd.columns, # Nombres de las columnas
			# 'bdd_rows': dd, # datos del activo
			# 'TRes': TRes, # resultados obtenidos para la serie de precios seleccionada
			# 'TResHTML': TResHTML, # resultados obtenidos para la serie de precios seleccionada
			# 'TABLApy': Tpy,
		# }) 

		context = ({
			'Texto0':'Prueba de lectura ficheros en HD',
		})
		context.update({
			'results': Results_dict,
			'testLib': TestMult(5,5),
#			'MKTidx': [0],
			'L_FolderNames': GetFolderNames('YAHOOBDD\\'),
			'L_FileNames': [] #GetFileNamesinFolder('YAHOOBDD\\ES35\\'),
		})
		
		# if id is not None:
			# obj = get_object_or_404(activo, id=id)
			# context['object'] = obj
		return render(request, self.template_name, context) #return render(request, 'about.html',{})

	def post(self, request, id=None, *args, **kwargs): # id=None (default)

		if request.method == "POST":
			MKTidx = request.POST.get("MKTidx", None) # se obtiene un string  int( )
			MKTname = request.POST.get("MKTname", None)
			#print('MKT[',MKTidx,']=',MKTname)
	
		Results_dict = {	'CAGR':8.34,
								'std_Y': 23.45,
							}
		
		# TRes = GetParamPrecio((itemBDD.tick).split(),dd)
		# print('Tabla Estadisticas Precio\n')
		# print(TRes)
		# TResHTML = TRes.to_html()
		
		# context.update({
			# 'results': Results_dict,
			# 'bdd_fields': dd.columns, # Nombres de las columnas
			# 'bdd_rows': dd, # datos del activo
			# 'TRes': TRes, # resultados obtenidos para la serie de precios seleccionada
			# 'TResHTML': TResHTML, # resultados obtenidos para la serie de precios seleccionada
			# 'TABLApy': Tpy,
		# }) 


		#print('MKTidx',MKTidx)
		L_FolderNames = GetFolderNames('YAHOOBDD\\')
		print('L_FolderNames:',L_FolderNames)
		L_FileNames=[]
		T_Activos=pd.DataFrame()
		
		if len(MKTidx)!=0:
			MKTidx = MKTidx.split(",") # Para separar el string si hay varios indices seleccionados "0,2"
			for mkt in MKTidx:
				print('mkt:',mkt)
				Dir = 'YAHOOBDD\\'+L_FolderNames[int(mkt)]+'\\'
				L_FileNames = GetFileNamesinFolder(Dir)
				if(len(L_FileNames)>0):
					#print('Dir:',Dir,' LCARTERA:',L_FileNames)
					CC=Close_FileScrapping(L_FileNames,Dir)
					df_CLim = Fechas_CARTERA(L_FileNames)
					T_Activos=T_Activos.append(df_CLim)
					#print('df_CLim:',df_CLim)
					#print('T_Activos::',T_Activos)
					
	#		print('L_FileNames:',L_FileNames)
			#LCARTERA = ['REP.mc','REE.mc']
			#print('Dir:',Dir,' LCARTERA:',L_FileNames)
			#CC=Close_FileScrapping(L_FileNames,Dir)
			#df_CLim = Fechas_CARTERA(L_FileNames)
			
			#df_CLim.reset_index(inplace=True) # drop=True)
			#T_Activos=df_CLim.to_html() # index_names=False index=False) # HttpResponse( )   'Siguiente paso'			
			T_Activos.reset_index(inplace=True) # drop=True)
			if len(T_Activos) > 0:
				L_FileNames=list(T_Activos['Ticker']) # nos quedamos con todos los tickers del dataframe
			#print('LFN:',L_FileNames)
			T_Activos=T_Activos.to_html(justify='center',classes='Tablesorter-OrdenFiltro') # index_names=False index=False) # HttpResponse( )   'Siguiente paso'			
			

#		else:
#			MKTidx = [0]

		
		context = ({
			'Texto0':'Prueba de lectura ficheros en HD',
		})
		context.update({
			'results': Results_dict,
			'MKTidx': MKTidx,
			'MKTname': MKTname,
			'L_FolderNames': L_FolderNames,
			'L_FileNames': L_FileNames,
			'T_Activos': T_Activos,
		})
		
		# if id is not None:
			# obj = get_object_or_404(activo, id=id)
			# context['object'] = obj
		return render(request, self.template_name, context) #return render(request, 'about.html',{})
		

class DatosListView(ListView):
	template_name = 'activos/datos_list.html'
	queryset = all_products.objects.all() 
	
# class AccionListView(View):
	# template_name = 'about.html' # 'acciones/accion_detail.html' #DetailView
	# def get(self, request, *args, **kwargs): # id=None (default)
		# #GET method 
		# context = {} #                 {'object':self.get_object()}
		# return render(request, self.template_name, context) #return render(request, 'about.html',{})

#class MyListView(AccionListView)
#	queryset = Accion.objects.filter(id=1)
		
class ActivoView(ActivoObjectMixin, View):
	template_name = 'activos/activo_detail.html' #DetailView
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
		print('ActivoView Results_dict:',Results_dict)
		print(itemBDD.tick,(itemBDD.tick).split())
		
		
		TRes = GetParamPrecio((itemBDD.tick).split(),dd)
		print('Tabla Estadisticas Precio\n')
		print(TRes)
		TResHTML = TRes.to_html()
		
		context.update({
			'results': Results_dict,
			'bdd_fields': dd.columns, # Nombres de las columnas
			'bdd_rows': dd, # datos del activo
			'TRes': TRes, # resultados obtenidos para la serie de precios seleccionada
			'TResHTML': TResHTML, # resultados obtenidos para la serie de precios seleccionada
			'TABLApy': Tpy,
		})
		
		# if id is not None:
			# obj = get_object_or_404(activo, id=id)
			# context['object'] = obj
		return render(request, self.template_name, context) #return render(request, 'about.html',{})


# HTTP METHODS
def my_fbv(request, *args, **kwargs):
	print(request.method)
	return render(request, 'about.html', {})