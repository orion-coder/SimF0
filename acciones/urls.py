# acciones/urls.py
from django.urls import path

from .views import (
	AccionView,
#	my_fbv,
	AccionListView,
	AccionCreateView,
	AccionUpdateView,
	AccionDeleteView,
	DatosListView,
)

app_name = 'acciones'
urlpatterns = [
	#path('', my_fbv, name='courses-list'),
	path('', AccionListView.as_view(), name='acciones-list'),
	path('create/', AccionCreateView.as_view(), name='acciones-create'),
	path('<int:id>/', AccionView.as_view(), name='acciones-detail'), #<-- intentamos llamar con la misma clase que para '' (primera opción). AccionView se llama dos veces
	path('<int:id>/update/', AccionUpdateView.as_view(), name='acciones-update'),
	path('<int:id>/delete/', AccionDeleteView.as_view(), name='acciones-delete'),
	path('bdd/', DatosListView.as_view(), name='datos-list'),
]