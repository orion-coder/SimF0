# activosHD/urls.py
from django.urls import path

from .views import (
	ActivoView,
#	my_fbv,
	ActivoListView,
	DatosListView,
)

app_name = 'activosHD'
urlpatterns = [
	#path('', my_fbv, name='courses-list'),
	path('', ActivoListView.as_view(), name='activos-list'),
	path('<int:id>/', ActivoView.as_view(), name='activos-detail'), #<-- intentamos llamar con la misma clase que para '' (primera opción). AccionView se llama dos veces
	path('bdd/', DatosListView.as_view(), name='datos-list'),
]