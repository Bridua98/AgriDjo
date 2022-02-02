import calculation
from .layout import CancelButton, DeleteButton, Formset
from .widgets import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, Button, ButtonHolder, Column, Div, Fieldset,
                                 Layout, Row, Submit, Field)
from django import forms
from django.db.models import fields

from .models import Acopio, AcopioCalificacion, AcopioDetalle, ActividadAgricola, ActividadAgricolaItemDetalle, ActividadAgricolaMaquinariaDetalle, AjusteStock, AjusteStockDetalle, Compra, CompraDetalle, Contrato, CuotaCompra, NotaCreditoEmitida, NotaCreditoEmitidaDetalle, NotaCreditoRecibida, NotaCreditoRecibidaDetalle, OrdenCompra, OrdenCompraDetalle, PedidoCompra, PedidoCompraDetalle, PlanActividadZafra, PlanActividadZafraDetalle, TransferenciaCuenta, Venta, VentaDetalle


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
        widget=calculation.SumInput('subtotal',   attrs={'readonly':True}),
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
    subtotal = forms.DecimalField(
        widget=calculation.FormulaInput('(cantidad*(precio-descuento))', attrs={'readonly':True}),
        label = "SubTotal"
    )
    class Meta:
        model = OrdenCompraDetalle
        fields = ['item', 'cantidad','precio','descuento']


# COMPRA
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
                Formset(
                    "CuotaCompraInline",
                    stacked=True,
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

class CuotaCompraForm(forms.ModelForm):
    class Meta:
        model = CuotaCompra
        fields = ['fechaVencimiento','monto']
        widgets = { 'fechaVencimiento':DateInput }



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


# ACTIVIDADES AGRICOLAS
class ActividadAgricolaForm(forms.ModelForm):
    totalMaquinaria = forms.DecimalField(
        widget=calculation.SumInput('subtotalMaquinaria',   attrs={'readonly':True}),
    )
    totalItem = forms.DecimalField(
        widget=calculation.SumInput('subtotalItem',   attrs={'readonly':True}),
    )
    class Meta:
        model = ActividadAgricola
        fields = ['fechaDocumento','tipoActividadAgricola','zafra', 'finca','lote','esServicioContratado','empleado','cantidadTrabajada','observacion']
        widgets = {'fechaDocumento':DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['totalMaquinaria'].label = False
        self.fields['totalItem'].label = False
        self.helper.layout = Layout(
            "fechaDocumento",
            "tipoActividadAgricola",
            "zafra",
            "finca",
            "lote",
            "esServicioContratado",
            "empleado",
            "cantidadTrabajada",
            "observacion",
            Fieldset(
                u'Detalle',
                Formset(
                    "ActividadAgricolaMaquinariaDetalleInline"#, stacked=True
                ), 
                Formset(
                    "ActividadAgricolaItemDetalleInline",#, stacked=True
                ),       
            ),
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total Máquina: </span>'), css_class="text-right"), Column("totalMaquinaria")
            ), 
             Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total Items: </span>'), css_class="text-right"), Column("totalItem")
            ), 
            Row(
                Div(Submit("submit", "Guardar"), HTML("""<a class="btn btn-secondary" href="{% url 'actividad_agricola_list' %}"> Cancelar</a>""" ))
            ) 
        )

class ActividadAgricolaMaquinariaDetalleForm(forms.ModelForm):
    subtotalMaquinaria = forms.DecimalField(
        widget=calculation.FormulaInput('precio*haTrabajada', attrs={'readonly':True}),
        label = "SubTotal"
    )
    class Meta:
        model = ActividadAgricolaMaquinariaDetalle
        fields = ['maquinaria', 'haTrabajada','precio','subtotalMaquinaria']

class ActividadAgricolaItemDetalleForm(forms.ModelForm):
    subtotalItem = forms.DecimalField(
        widget=calculation.FormulaInput('costo*cantidad', attrs={'readonly':True}),
        label = "SubTotal"
    )
    class Meta:
        model = ActividadAgricolaItemDetalle
        fields = ['item', 'deposito','dosis','costo','cantidad','porcentajeImpuesto','subtotalItem']

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


# CONTRATO FORM
class ContratoForm(forms.ModelForm):
    class Meta:
        model = Contrato
        fields = ['fecha','zafra','persona','descripcion','costoPactado']
        widgets = {'fecha':DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "fecha",
            "zafra",
            "persona",
            "descripcion",
            "costoPactado",
            Row(
                Div(Submit("submit", "Guardar"), HTML("""<a class="btn btn-secondary" href="{% url 'contrato_list' %}"> Cancelar</a>""" ))
            ) 
        )

# VENTAS
class VentaForm(forms.ModelForm):
    total = forms.DecimalField(
        widget=calculation.SumInput('subtotal',   attrs={'readonly':True}),
    )
    total_iva = forms.DecimalField(
        widget=calculation.SumInput('impuesto',   attrs={'readonly':True}),
    )
    class Meta:
        model = Venta
        fields = ['fechaDocumento','esCredito','comprobante', 'timbrado','cliente','cuenta','deposito','observacion']
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
            "cliente",
            "cuenta",
            "deposito",
            "observacion",
            Fieldset(
                u'Detalle',
                Formset(
                    "VentaDetalleInline"#, stacked=True
                ), 
                
            ),
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total: </span>'), css_class="text-right"), Column("total")
            ), 
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total Impuesto: </span>'), css_class="text-right"), Column("total_iva")
            ),
            Row(
                Div(Submit("submit", "Guardar"), HTML("""<a class="btn btn-secondary" href="{% url 'venta_list' %}"> Cancelar</a>""" ))
            ) 
        )

class VentaDetalleForm(forms.ModelForm):
    subtotal = forms.DecimalField(
        widget=calculation.FormulaInput('precio*cantidad', attrs={'readonly':True}),
        label = "SubTotal"
    )
    impuesto = forms.DecimalField(
        widget=calculation.FormulaInput('parseFloat((subtotal*porcentajeImpuesto)/(porcentajeImpuesto+100)).toFixed(0)', attrs={'readonly':True}),
        label = "Impuesto"
    )
    class Meta:
        model = VentaDetalle
        fields = ['item', 'cantidad','precio','porcentajeImpuesto','impuesto','subtotal']


# NOTA DE CREDITO RECIBIDA
class NotaCreditoRecibidaForm(forms.ModelForm):
    total = forms.DecimalField(
        widget=calculation.SumInput('subtotal',   attrs={'readonly':True}),
    )
    total_iva = forms.DecimalField(
        widget=calculation.SumInput('impuesto',   attrs={'readonly':True}),
    )
    class Meta:
        model = NotaCreditoRecibida
        fields = ['fechaDocumento','esCredito','comprobante', 'timbrado','proveedor','cuenta','deposito',"compra",'observacion']
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
            "compra",
            "observacion",
            Fieldset(
                u'Detalle',
                Formset(
                    "NotaCreditoRecibidaDetalleInline"#, stacked=True
                ), 
                
            ),
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total: </span>'), css_class="text-right"), Column("total")
            ), 
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total Impuesto: </span>'), css_class="text-right"), Column("total_iva")
            ),
            Row(
                Div(Submit("submit", "Guardar"), HTML("""<a class="btn btn-secondary" href="{% url 'nota_credito_recibida_list' %}"> Cancelar</a>""" ))
            ) 
        )

class NotaCreditoRecibidaDetalleForm(forms.ModelForm):
    subtotal = forms.DecimalField(
        widget=calculation.FormulaInput('valor*cantidad', attrs={'readonly':True}),
        label = "SubTotal"
    )
    impuesto = forms.DecimalField(
        widget=calculation.FormulaInput('parseFloat((subtotal*porcentajeImpuesto)/(porcentajeImpuesto+100)).toFixed(0)', attrs={'readonly':True}),
        label = "Impuesto"
    )
    class Meta:
        model = NotaCreditoRecibidaDetalle
        fields = ['esDevolucion','item', 'cantidad','valor','porcentajeImpuesto','impuesto','subtotal']



# NOTA DE CREDITO EMITIDA
class NotaCreditoEmitidaForm(forms.ModelForm):
    total = forms.DecimalField(
        widget=calculation.SumInput('subtotal',   attrs={'readonly':True}),
    )
    total_iva = forms.DecimalField(
        widget=calculation.SumInput('impuesto',   attrs={'readonly':True}),
    )
    class Meta:
        model = NotaCreditoEmitida
        fields = ['fechaDocumento','esCredito','comprobante', 'timbrado','cliente','cuenta','deposito',"venta",'observacion']
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
            "cliente",
            "cuenta",
            "deposito",
            "venta",
            "observacion",
            Fieldset(
                u'Detalle',
                Formset(
                    "NotaCreditoEmitidaDetalleInline"#, stacked=True
                ), 
                
            ),
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total: </span>'), css_class="text-right"), Column("total")
            ), 
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total Impuesto: </span>'), css_class="text-right"), Column("total_iva")
            ),
            Row(
                Div(Submit("submit", "Guardar"), HTML("""<a class="btn btn-secondary" href="{% url 'nota_credito_recibida_list' %}"> Cancelar</a>""" ))
            ) 
        )

class NotaCreditoEmitidaDetalleForm(forms.ModelForm):
    subtotal = forms.DecimalField(
        widget=calculation.FormulaInput('valor*cantidad', attrs={'readonly':True}),
        label = "SubTotal"
    )
    impuesto = forms.DecimalField(
        widget=calculation.FormulaInput('parseFloat((subtotal*porcentajeImpuesto)/(porcentajeImpuesto+100)).toFixed(0)', attrs={'readonly':True}),
        label = "Impuesto"
    )
    class Meta:
        model = NotaCreditoEmitidaDetalle
        fields = ['esDevolucion','item', 'cantidad','valor','porcentajeImpuesto','impuesto','subtotal']



# TRANSFERENCIA CUENTA 
class TransferenciaCuentaForm(forms.ModelForm):
    class Meta:
        model = TransferenciaCuenta
        fields = ['fecha','comprobante','cuentaSalida','cuentaEntrada','monto','observacion']
        widgets = {'fecha':DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            "fecha",
            "comprobante",
            "cuentaSalida",
            "cuentaEntrada",
            "monto",
            "observacion",
            Row(
                Div(Submit("submit", "Guardar"), HTML("""<a class="btn btn-secondary" href="{% url 'transferencia_cuenta_list' %}"> Cancelar</a>""" ))
            ) 
        )


