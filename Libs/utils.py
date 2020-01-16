#import csv # Para lectura del contenido de ficheros csv
import pandas as pd 
import glob
#import os


def TestMult(a,b):
	return(a*b+3)

def GetFolderNames(path):
	L_DIRS = glob.glob(path+"*/")
	L_DIRS = [x[len(path):-1] for x in L_DIRS] # para quedarnos solo con el nombre del Ticker\n"
#"print(\"\\nListado de CARPETAS en \", dataPath,\"(\",len(L_DIRS),\"):\\n\",L_DIRS)\n"
	return(L_DIRS)
	
def GetFileNamesinFolder(path):
	L_FILES = glob.glob(path+"*.csv")
	L_FILES = [x[len(path):-4] for x in L_FILES] # para quedarnos solo con el nombre del Ticker\n",
#"print(\"\\nListado de FICHEROS en \", dataPath,\"(\",len(L_FILES),\"):\\n\",L_FILES)\n"
	return(L_FILES)

# Read File "path/filename.csv"
def ReadStockDataCSV_pd(FullNamecsv):
	# Read data from file 'path/filename.csv' 
	# (in the same directory that your python process is based)
	# Control delimiters, rows, column names with read_csv (see later) 
	#nF = 'BDD/'+nombreF;
	data = pd.read_csv(FullNamecsv,sep=',') #,parse_dates=True,index_col=0)  # "filename.csv"
	# Preview the first 5 lines of the loaded data 
	data.head()	
	print('desde RStockCSV_pd data.head()\n',data.head())
	#print(data)
	return(data)

# FILE Scrapping: Lectura de tickers desde ficheros, de forma similar a Yahoo web scraping
# Falta Añadir FInicio, FFin
def ReadF(tickers,path):
	#print('path:',path,' Tickers:',tickers)
	def ReadStockCSV_pd(nombreF): # Read data from file 'filename.csv'
		nF = path+nombreF+".csv"	#'BDD/'+nombreF
		# print('nF:',nF)
		return(pd.read_csv(nF,sep=',',index_col=[0], parse_dates=[0]))
	datas = map (ReadStockCSV_pd,tickers)
	return(pd.concat(datas, keys=tickers, names=['Ticker', 'Date'],sort=False)) 

# FILE Scrapping: Lectura de tickers desde ficheros, de forma similar a Yahoo web scraping
# Parametros: Lista de Tickers, path donde estan los ficheros, FInicio, FFin
def ReadF_2F(tickers,path,startdate, enddate):
   def ReadStockCSV_pd(nombreF): # Read data from file 'filename.csv' 
      nF = path+nombreF+".csv" #'BDD/'+nombreF;
      td = pd.read_csv(nF,sep=',',index_col=[0], parse_dates=[0])
      #mask=
      td_mask = td[startdate:enddate]
      return(td_mask)
   print('2) dataPath:',path,'\nCARTERA:',tickers,'\nFechas Análisis: [',startdate,'-',enddate,']') # FFin.strftime('%d/%m/%Y')
   datas = map (ReadStockCSV_pd,tickers)
   return(pd.concat(datas, keys=tickers, names=['Ticker', 'Date'],sort=False))	 
	 
# File Scrapping and build Close Historic Matrix
# Parametros: LCARTERA Lista de tickers o nombres de los ficheros con los datos historicos
def Close_FileScrapping(LCARTERA,dataPath):
	global ES_data
	ES_data = ReadF(LCARTERA, dataPath) #ReadF_2F(LCARTERA, dataPath, FInicio, FFin)
	#print('3)',ES_data)
	#ES_data.head()
	# Isolate the `Adj Close` values and transform the DataFrame
	ES_C = ES_data[['Close']].reset_index().pivot('Date', 'Ticker', 'Close').interpolate().bfill() #"Adj Close"
	#ES_C.head()
	return ES_C

# Obtiene para cada ticker de ES_data la FechaI del primer dato, la FechaF del último dato, y NSes el número de sesiones
# y construye un dataframe
def Fechas_CARTERA(LCARTERA):
	C_Lim = pd.DataFrame(columns=["Ticker","FechaI", "FechaF", "NSes"])
	C_Lim.set_index("Ticker",inplace=True)
	for x in LCARTERA:
		NSes = len(ES_data.loc[[x]]) # NSes = len(ES_data.loc[x])
		if(NSes != 0):
			C_Lim.loc[x]=[ES_data.loc[x].index[0].date().strftime('%d/%m/%Y'),ES_data.loc[x].index[-1].date().strftime('%d/%m/%Y'),NSes]
		else:
			C_Lim.loc[x]=['-','-',0]
	#print('\nFechas de la CARTERA\n',C_Lim) #C_Lim.sort_index(inplace=True)
	return C_Lim
	 
	
# Rutina para dataframe leidos con pandas
def FillTableStock_pd(bdd_OHLCdata):
	my_pyT = '<table class="table table-striped table-hover table-sm table-bordered" style="width: 100%;">' \
				'<thead class="thead-dark">' \
				'<tr>' \
				'<th scope="col">#</th>'
	for d_F in bdd_OHLCdata.columns:
		my_pyT += '<th scope="col">'+d_F+'</th>'
	my_pyT += '</tr>' \
	'</thead>' \
	'<tbody>'
	print('Fill_pd')
	for idx in range(bdd_OHLCdata.shape[0]):
		my_pyT += '<tr>'
		my_pyT += '<th scope="row">'+str(idx)+'</th>'
		d_F = bdd_OHLCdata.loc[idx]
		for d_C in d_F:
			my_pyT += '<td>'+str(d_C)+'</td>'
		my_pyT += '</tr>'
	my_pyT += '</tbody>'
	my_pyT += '</table>'
	return(my_pyT)

# Rutina para datos de matrices leidas a pelo de .csv
def FillTableStock(bdd_fields,bdd_OHLCdata):
	my_pyT = '<div class="TablaScrollableCapFix"><table class="table table-striped table-hover table-sm" style="width: 100%;">' \
				'<thead class="thead-dark">' \
				'<tr>' \
				'<th scope="col">#</th>'
	for d_F in bdd_fields:
		my_pyT += '<th scope="col">'+str(d_F)+'</th>'
	my_pyT += '</tr>' \
	'</thead>' \
	'<tbody>'
	#for d_F in bdd_OHLCdata:
	for idx, d_F in enumerate(bdd_OHLCdata):
		my_pyT += '<tr>'
		my_pyT += '<td scope="row">'+str(idx)+'</td>'
		my_pyT += '<td>'+str(d_F[0])+'</td>'
		for d_C in d_F[1:]:
			my_pyT += '<td>'+str(round(d_C,2))+'</td>'
		my_pyT += '</tr>'
	my_pyT += '</tbody>'
	my_pyT += '</table></div>'
	return(my_pyT)

def ReadStockCSV(nombreF):
	with open('BDD/'+nombreF) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		fields = next(csv_reader) 	
		#print(f'Column names are {", ".join(fields)}')
		rows = []
		for row in csv_reader:
			rows.append(row)
			#print(f'{", ".join(row)}')
		print("Total no. of rows: %d"%(csv_reader.line_num)) 
	return(fields,rows)
	