# Load the Pandas libraries with alias 'pd' 
import pandas as pd 

def ReadStockCSV_pd(nombreF):
	# Read data from file 'filename.csv' 
	# (in the same directory that your python process is based)
	# Control delimiters, rows, column names with read_csv (see later) 
	nF = 'BDD/'+nombreF;
	data = pd.read_csv(nF,sep=',') #,parse_dates=True,index_col=0)  # "filename.csv"
	# Preview the first 5 lines of the loaded data 
	data.head()	
	print('desde ReadStockCSV_pd data.head()\n',data.head())
	#print(data)
	return(data)
	
"""def Get_EstadisticaPrecio(dd):
	
	
	
	
	return Estadisticos
"""