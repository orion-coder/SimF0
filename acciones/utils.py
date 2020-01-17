import csv

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
def FillTableStock(bdd_fields,bdd_OHLCdata): # clases de la libreria bootstrap 4.3.1 utilizada en el fichero común: base.html
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
	