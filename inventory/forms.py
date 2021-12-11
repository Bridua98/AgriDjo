import calculation
from .layout import CancelButton, DeleteButton, Formset
from .widgets import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, Button, ButtonHolder, Column, Div, Fieldset,
                                 Layout, Row, Submit, Field)
from django import forms
from django.db.models import fields

from .models import Acopio, AcopioCalificacion, AcopioDetalle, OrdenCompra, OrdenCompraDetalle, PedidoCompra, PedidoCompraDetalle, PlanActividadZafra, PlanActividadZafraDetalle


class PlanActividadZafraForm(forms.ModelForm):
    total = forms.DecimalField(
        widget=calculation.SumInput('costo',   attrs={'readonly':True}),
    )
    class Meta:
        model = PlanActividadZafra
        fields = ['fecha', 'zafra', 'observacion']
        widgets = {'fecha':DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['total'].label = False
        self.helper.layout = Layout(
            "fecha",
            "zafra",
            "observacion",
            Fieldset(
                u'Detalle',
                Formset(
                    "PlanActividadZafraDetalleInline"#, stacked=True
                ), 
                
            ),
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total: </span>'), css_class="text-right"), Column("total")
            ), 
            Row(
                Div(Submit("submit", "Guardar"), HTML("""<a class="btn btn-secondary" href="{% url 'plan_actividad_zafra_list' %}"> Cancelar</a>""" ))
            ) 
        )

class PlanActividadZafraDetalleForm(forms.ModelForm):
    class Meta:
        model = PlanActividadZafraDetalle
        fields = ['fechaActividad', 'finca', 'tipoActividadAgricola', 'descripcion','costo']
        widgets = { 'fechaActividad':DateInput }



class AcopioForm(forms.ModelForm):
    class Meta:
        model = Acopio
        fields = ['fecha', 'zafra', 'deposito', 'conductor','conductor','camion','comprobante','pBruto','pTara','pDescuento','pBonificacion','esTransportadoraPropia','observacion']
        widgets = {'fecha':DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "fecha",
            "zafra",
            "deposito",
            "conductor",
            "camion",
            "comprobante",
            "pBruto",
            "pTara",
            "pDescuento",
            "pBonificacion",
            "esTransportadoraPropia",
            "observacion",
            Fieldset(
                u'Detalle',
                Formset(
                    "AcopioDetalleInline"#, stacked=True
                ), 
                
            ),
            Row(
                Div(Submit("submit", "Guardar"), HTML("""<a class="btn btn-secondary" href="{% url 'plan_actividad_zafra_list' %}"> Cancelar</a>""" ))
            ) 
        )

class AcopioDetalleForm(forms.ModelForm):
    class Meta:
        model = AcopioDetalle
        fields = ['acopio', 'finca', 'lote', 'peso']

class AcopioCalificacionForm(forms.ModelForm):
    class Meta:
        model = AcopioCalificacion
        fields = ['acopio', 'calificacionAgricola', 'grado', 'porcentaje', 'peso']

# PEDIDO COMPRA
class PedidoCompraForm(forms.ModelForm):
    cantidad = forms.DecimalField(
        widget=calculation.SumInput('cantidad',   attrs={'readonly':True}),
    )
    class Meta:
        model = PedidoCompra
        fields = ['proveedor','fechaDocumento', 'fechaVencimiento', 'observacion']
        widgets = {'fechaDocumento':DateInput,'fechaVencimiento':DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['cantidad'].label = False
        self.helper.layout = Layout(
            "proveedor",
            "fechaDocumento",
            "fechaVencimiento",
            "observacion",
            Fieldset(
                u'Detalle',
                Formset(
                    "PedidoCompraDetalleInline"#, stacked=True
                ), 
                
            ),
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Cantidad: </span>'), css_class="text-right"), Column("cantidad")
            ), 
            Row(
                Div(Submit("submit", "Guardar"), HTML("""<a class="btn btn-secondary" href="{% url 'pedido_compra_list' %}"> Cancelar</a>""" ))
            ) 
        )

class PedidoCompraDetalleForm(forms.ModelForm):
    class Meta:
        model = PedidoCompraDetalle
        fields = ['item', 'cantidad']


# ORDEN COMPRA
class OrdenCompraForm(forms.ModelForm):
    total = forms.DecimalField(
        widget=calculation.SumInput('precio',   attrs={'readonly':True}),
    )
    class Meta:
        model = OrdenCompra
        fields = ['pedidoCompra','proveedor','fechaDocumento', 'observacion']
        widgets = {'fechaDocumento':DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['total'].label = False
        self.helper.layout = Layout(
            "pedidoCompra",
            "proveedor",
            "fechaDocumento",
            "observacion",
            Fieldset(
                u'Detalle',
                Formset(
                    "OrdenCompraDetalleInline"#, stacked=True
                ), 
                
            ),
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total: </span>'), css_class="text-right"), Column("total")
            ), 
            Row(
                Div(Submit("submit", "Guardar"), HTML("""<a class="btn btn-secondary" href="{% url 'pedido_compra_list' %}"> Cancelar</a>""" ))
            ) 
        )

class OrdenCompraDetalleForm(forms.ModelForm):
    class Meta:
        model = OrdenCompraDetalle
        fields = ['item', 'cantidad','precio','descuento']


