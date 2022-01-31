from django import forms
from django.forms.widgets import DateInput
import django_filters
from django_filters.filters import DateFilter
# from core import widgets
from django_filters.filterset import FilterSet
from inventory.models import ActividadAgricola, Compra, Venta



class DateTypeInput(forms.DateInput):
    input_type = 'date'

class LibroCompraFilter(FilterSet):
    fecha_desde = django_filters.DateFilter(widget=DateTypeInput(attrs={'placeholder': '1970-01-01'}), field_name='fechaDocumento', lookup_expr='gte', label='Desde')
    fecha_hasta = django_filters.DateFilter(widget=DateTypeInput(), field_name='fechaDocumento', lookup_expr='lte', label='Hasta')
    fechaDocumento = django_filters.DateRangeFilter(label='Rango')
    class Meta:
        model = Compra
        fields = ["fecha_desde","fecha_hasta","comprobante","proveedor"]


class LibroVentaFilter(FilterSet):
    fechaDocumento = django_filters.DateFilter(widget=DateInput(attrs={'type':'fechaDocumento'}))
    class Meta:
        model = Venta
        fields = ["fechaDocumento","comprobante","cliente"]

class CompraInformeFilter(FilterSet):
    fechaDocumento = django_filters.DateFilter(widget=DateInput(attrs={'type':'fechaDocumento'}))
    class Meta:
        model = Compra
        fields = ["fechaDocumento","comprobante","proveedor"]

class VentaInformeFilter(FilterSet):
    fechaDocumento = django_filters.DateFilter(widget=DateInput(attrs={'type':'fechaDocumento'}))
    class Meta:
        model = Venta
        fields = ["fechaDocumento","comprobante","cliente"]

class ProduccionAgricolaInformeFilter(FilterSet):
    fechaDocumento = django_filters.DateFilter(widget=DateInput(attrs={'type':'fechaDocumento'}))
    class Meta:
        model = ActividadAgricola
        fields = ["fechaDocumento","zafra","finca"]