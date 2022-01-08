import calculation
from .layout import CancelButton, DeleteButton, Formset
from .widgets import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, Button, ButtonHolder, Column, Div, Fieldset,
                                 Layout, Row, Submit, Field)
from django import forms
from django.db.models import fields

from .models import Acopio, AcopioCalificacion, AcopioDetalle, AjusteStock, AjusteStockDetalle, Compra, CompraDetalle, OrdenCompra, OrdenCompraDetalle, PedidoCompra, PedidoCompraDetalle, PlanActividadZafra, PlanActividadZafraDetalle


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
                u'Detalles',
                Formset(
                    "AcopioDetalleInline",#, stacked=True
                ), 
                Formset(
                    "AcopioCalificacionDetalleInline",#, stacked=True
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


# ORDEN COMPRA
class CompraForm(forms.ModelForm):
    total = forms.DecimalField(
        widget=calculation.SumInput('subtotal',   attrs={'readonly':True}),
    )
    total_iva = forms.DecimalField(
        widget=calculation.SumInput('impuesto',   attrs={'readonly':True}),
    )
    class Meta:
        model = Compra
        fields = ['fechaDocumento','esCredito','comprobante', 'timbrado','proveedor','cuenta','deposito','observacion']
        widgets = {'fechaDocumento':DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['total'].label = False
        self.fields['total_iva'].label = False
        self.helper.layout = Layout(
            "fechaDocumento",
            "esCredito",
            "comprobante",
            "timbrado",
            "proveedor",
            "cuenta",
            "deposito",
            "observacion",
            Fieldset(
                u'Detalle',
                Formset(
                    "CompraDetalleInline"#, stacked=True
                ), 
                
            ),
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total: </span>'), css_class="text-right"), Column("total")
            ), 
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total Impuesto: </span>'), css_class="text-right"), Column("total_iva")
            ),
            Row(
                Div(Submit("submit", "Guardar"), HTML("""<a class="btn btn-secondary" href="{% url 'compra_list' %}"> Cancelar</a>""" ))
            ) 
        )

class CompraDetalleForm(forms.ModelForm):
    subtotal = forms.DecimalField(
        widget=calculation.FormulaInput('cantidad*costo', attrs={'readonly':True}),
        label = "SubTotal"
    )
    impuesto = forms.DecimalField(
        widget=calculation.FormulaInput('parseFloat((subtotal*porcentajeImpuesto)/(porcentajeImpuesto+100)).toFixed(0)', attrs={'readonly':True}),
        label = "Impuesto"
    )
    class Meta:
        model = CompraDetalle
        fields = ['item', 'cantidad','costo','porcentajeImpuesto','impuesto','subtotal']


class AjusteStockForm(forms.ModelForm):
    class Meta:
       model = AjusteStock
       #template_name = 'inventory/ajuste_stock_create.html'
       fields = ['fechaDocumento','comprobante','empleado','deposito','observacion',]
       widgets = { 'fechaDocumento':DateInput }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "fechaDocumento",
            "comprobante",
            "empleado",
            "deposito",
            "observacion",
            Fieldset(
                u'Detalle',
                Formset(
                    "AjusteStockDetalleInline"#, stacked=True
                ), 
                Row(
                Div(Submit("submit", "Guardar"), HTML("""<a class="btn btn-secondary" href="{% url 'plan_actividad_zafra_list' %}"> Cancelar</a>""" ))
                ) 
            )
        )

class AjusteStockDetalleForm(forms.ModelForm):
    class Meta:
        model = AjusteStockDetalle
        fields = ['item', 'cantidad',]
