from django import forms
from django.forms.widgets import DateInput
import django_filters
from django_filters.filters import DateFilter
# from core import widgets
from django_filters.filterset import FilterSet
from inventory.models import ActividadAgricola, Compra, ItemMovimiento, Venta



class DateTypeInput(forms.DateInput):
    input_type = 'date'

class LibroCompraFilter(FilterSet):
    fecha_desde = django_filters.DateFilter(widget=DateTypeInput(attrs={'placeholder': '1970-01-01'}), field_name='fechaDocumento', lookup_expr='gte', label='Desde')
    fecha_hasta = django_filters.DateFilter(widget=DateTypeInput(), field_name='fechaDocumento', lookup_expr='lte', label='Hasta')
    # fechaDocumento = django_filters.DateRangeFilter(label='Rango')
    
    def __init__(self, *args, **kwargs):
        super(LibroCompraFilter, self).__init__(*args, **kwargs)
        self.form.initial['esVigente'] = True

    class Meta:
        model = Compra
        fields = ["fecha_desde","fecha_hasta","comprobante","proveedor","deposito","esCredito","esVigente"]
   

class LibroVentaFilter(FilterSet):
    fecha_desde = django_filters.DateFilter(widget=DateTypeInput(attrs={'placeholder': '1970-01-01'}), field_name='fechaDocumento', lookup_expr='gte', label='Desde')
    fecha_hasta = django_filters.DateFilter(widget=DateTypeInput(), field_name='fechaDocumento', lookup_expr='lte', label='Hasta')
    # fechaDocumento = django_filters.DateRangeFilter(label='Rango')
    
    def __init__(self, *args, **kwargs):
        super(LibroVentaFilter, self).__init__(*args, **kwargs)
        self.form.initial['esVigente'] = True

    class Meta:
        model = Venta
        fields = ["fecha_desde","fecha_hasta","comprobante","cliente","deposito","esCredito","esVigente"]

class CompraInformeFilter(FilterSet):
    fecha_desde = django_filters.DateFilter(widget=DateTypeInput(attrs={'placeholder': '1970-01-01'}), field_name='fechaDocumento', lookup_expr='gte', label='Desde')
    fecha_hasta = django_filters.DateFilter(widget=DateTypeInput(), field_name='fechaDocumento', lookup_expr='lte', label='Hasta')
    fechaDocumento = django_filters.DateRangeFilter(label='Rango')
    def __init__(self, *args, **kwargs):
        super(CompraInformeFilter, self).__init__(*args, **kwargs)
        self.form.initial['esVigente'] = True

    
    class Meta:
        model = Compra
        fields = ["fechaDocumento","fecha_desde","fecha_hasta","comprobante","proveedor","deposito","cuenta","esCredito","esVigente"]

class VentaInformeFilter(FilterSet):
    fecha_desde = django_filters.DateFilter(widget=DateTypeInput(attrs={'placeholder': '1970-01-01'}), field_name='fechaDocumento', lookup_expr='gte', label='Desde')
    fecha_hasta = django_filters.DateFilter(widget=DateTypeInput(), field_name='fechaDocumento', lookup_expr='lte', label='Hasta')
    fechaDocumento = django_filters.DateRangeFilter(label='Rango')

    def __init__(self, *args, **kwargs):
            super(VentaInformeFilter, self).__init__(*args, **kwargs)
            self.form.initial['esVigente'] = True
            
    class Meta:
        model = Venta
        fields = ["fechaDocumento","fecha_desde","fecha_hasta","comprobante","cliente","deposito","cuenta","esCredito","esVigente"]

class ProduccionAgricolaInformeFilter(FilterSet):
    fecha_desde = django_filters.DateFilter(widget=DateTypeInput(attrs={'placeholder': '1970-01-01'}), field_name='fechaDocumento', lookup_expr='gte', label='Desde')
    fecha_hasta = django_filters.DateFilter(widget=DateTypeInput(), field_name='fechaDocumento', lookup_expr='lte', label='Hasta')

    def __init__(self, *args, **kwargs):
            super(ProduccionAgricolaInformeFilter, self).__init__(*args, **kwargs)
            self.form.initial['esVigente'] = True

    fechaDocumento = django_filters.DateRangeFilter(label='Rango')
    class Meta:
        model = ActividadAgricola
        fields = ["fechaDocumento","fecha_desde","fecha_hasta","tipoActividadAgricola","zafra","finca","lote","empleado","esServicioContratado","esVigente"]

class InventarioDepositoInformeFilter(FilterSet):
    fecha_desde = django_filters.DateFilter(widget=DateTypeInput(attrs={'placeholder': '1970-01-01'}), field_name='fechaDocumento', lookup_expr='gte', label='Desde')
    fecha_hasta = django_filters.DateFilter(widget=DateTypeInput(), field_name='fechaDocumento', lookup_expr='lte', label='Hasta')

    def __init__(self, *args, **kwargs):
        super(InventarioDepositoInformeFilter, self).__init__(*args, **kwargs)
        self.form.initial['esVigente'] = True

    # fechaDocumento = django_filters.DateRangeFilter(label='Rango')
    class Meta:
        model = ItemMovimiento
        fields = ["fecha_desde","fecha_hasta","tipoMovimiento","item","deposito","esVigente"]