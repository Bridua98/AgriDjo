from django.shortcuts import reverse
from email.policy import default
import calculation
from .layout import CancelButton, DeleteButton, Formset
from .widgets import DateInput, DecimalMaskInput, InvoiceMaskInput, ItemCustomSelect
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, Button, ButtonHolder, Column, Div, Fieldset,
                                 Layout, Row, Submit, Field)
from django import forms
from django.db.models import fields
from django.contrib.auth.models import User

from .models import Acopio, AcopioCalificacion, AcopioDetalle, ActividadAgricola, ActividadAgricolaItemDetalle, ActividadAgricolaMaquinariaDetalle, AjusteStock, AjusteStockDetalle, CierreZafra, CierreZafraDetalle, Cobro, CobroDetalle, CobroMedio, Compra, CompraDetalle, Contrato, CuotaCompra, CuotaVenta, Item, LiquidacionAgricola, LiquidacionAgricolaDetalle, NotaCreditoEmitida, NotaCreditoEmitidaDetalle, NotaCreditoRecibida, NotaCreditoRecibidaDetalle, NotaDebitoEmitida, NotaDebitoEmitidaDetalle, NotaDebitoRecibida, NotaDebitoRecibidaDetalle, OrdenCompra, OrdenCompraDetalle, PedidoCompra, PedidoCompraDetalle, Persona, PlanActividadZafra, PlanActividadZafraDetalle, TransferenciaCuenta, Venta, VentaDetalle, Zafra


from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    """
    Custom user register form
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['autofocus'] = True
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.helper.layout = Layout(

            Row(
                Column('first_name'),
                Column('last_name'),
                
            ),
            Row(
                Column('username'),
                Column('email'),
            ),
            Row(
                Column('password1'),
                Column('password2'), 
            ),
            "is_active",
            ButtonHolder(
                Submit('submit', 'Guardar',  css_class='btn btn-success'),
                CancelButton()
            )
            
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email","is_active",)


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        self.fields['password'].help_text = "Las contraseñas no se almacenan en bruto, así que no hay manera de ver la contraseña del usuario, pero se puede cambiar la contraseña mediante <a href='%s'>este formulario.</a>"%reverse("password_change")
        self.helper.layout = Layout(

            Row(
                Column('first_name'),
                Column('last_name'),
                
            ),
            Row(
                Column('username'),
                Column('email'),
            ),
            Row(
                Column('password'),
            ),
            "is_active",
            ButtonHolder(
                Submit('submit', 'Guardar',  css_class='btn btn-success'),
                CancelButton(),
            )
            
        )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "email","is_active",)

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
        #self.fields['total'].widget = DecimalMaskInput()
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
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'plan_actividad_zafra_list' %}"> Cancelar</a>""" ))
            ) 
        )

class PlanActividadZafraDetalleForm(forms.ModelForm):
    class Meta:
        model = PlanActividadZafraDetalle
        fields = ['fechaActividad', 'finca', 'tipoActividadAgricola', 'descripcion','costo']
        widgets = { 'fechaActividad':DateInput,'costo': DecimalMaskInput }



class AcopioForm(forms.ModelForm):
    class Meta:
        model = Acopio
        fields = ['fecha', 'zafra', 'deposito', 'conductor','conductor','camion','comprobante','pBruto','pTara','pDescuento','pBonificacion','esTransportadoraPropia','observacion']
        widgets = {'fecha':DateInput,'pBruto':DecimalMaskInput,'pTara':DecimalMaskInput,'pDescuento':DecimalMaskInput,'pBonificacion':DecimalMaskInput}

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
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'plan_actividad_zafra_list' %}"> Cancelar</a>""" ))
            ) 
        )

class AcopioDetalleForm(forms.ModelForm):
    class Meta:
        model = AcopioDetalle
        fields = ['acopio', 'finca', 'lote', 'peso']
        widgets = {'peso':DecimalMaskInput}

class AcopioCalificacionForm(forms.ModelForm):
    class Meta:
        model = AcopioCalificacion
        fields = ['acopio', 'calificacionAgricola', 'grado', 'porcentaje', 'peso']
        widgets = {'grado':DecimalMaskInput,'porcentaje':DecimalMaskInput,'peso':DecimalMaskInput}

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
        #self.fields['cantidad'].widget = DecimalMaskInput()
        self.fields["proveedor"].queryset =  proveedor = Persona.objects.filter(esProveedor=True)
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
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'pedido_compra_list' %}"> Cancelar</a>""" ))
            ) 
        )

class PedidoCompraDetalleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["item"].queryset =  item = Item.objects.filter(tipoItem__pk=2) # sea igual a normal
    class Meta:
        model = PedidoCompraDetalle
        fields = ['item', 'cantidad']
        widgets = {'cantidad':DecimalMaskInput}


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
        self.fields["proveedor"].queryset =  proveedor = Persona.objects.filter(esProveedor=True)
        self.fields['total'].label = False
        #self.fields['total'].widget = DecimalMaskInput()
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
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'pedido_compra_list' %}"> Cancelar</a>""" ))
            ) 
        )

class OrdenCompraDetalleForm(forms.ModelForm):
    subtotal = forms.DecimalField(
        widget=calculation.FormulaInput('(cantidad*(precio-descuento))', attrs={'readonly':True}),
        label = "SubTotal"
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["item"].queryset =  item = Item.objects.filter(tipoItem__pk=2) # sea igual a normal
    class Meta:
        model = OrdenCompraDetalle
        fields = ['item', 'cantidad','precio','descuento']
        widgets = {'cantidad':DecimalMaskInput,'precio':DecimalMaskInput,'descuento':DecimalMaskInput}


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
        self.fields["proveedor"].queryset =  proveedor = Persona.objects.filter(esProveedor=True)
        self.fields['total'].label = False
        #self.fields['total'].widget = DecimalMaskInput()
        self.fields['total_iva'].label = False
        #self.fields['total_iva'].widget = DecimalMaskInput()
        self.fields['comprobante'].widget = InvoiceMaskInput()
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
                    "CompraDetalleInline",#, stacked=True
                    css_class="compra-detalle-container"
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
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'compra_list' %}"> Cancelar</a>""" ))
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
    item = ItemCustomSelect()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["item"].queryset =  item = Item.objects.filter(tipoItem__pk=2) # sea igual a normal
    class Meta:
        model = CompraDetalle
        fields = ['item', 'cantidad','costo','porcentajeImpuesto','impuesto','subtotal']
        widgets = {'costo':DecimalMaskInput,'cantidad':DecimalMaskInput,'porcentajeImpuesto':DecimalMaskInput,'impuesto':DecimalMaskInput,'subtotal':DecimalMaskInput}

class CuotaCompraForm(forms.ModelForm):
    class Meta:
        model = CuotaCompra
        fields = ['fechaVencimiento','monto']
        widgets = { 'fechaVencimiento':DateInput,'monto':DecimalMaskInput}

class AjusteStockForm(forms.ModelForm):
    class Meta:
       model = AjusteStock
       fields = ['fechaDocumento','comprobante','empleado','deposito','observacion',]
       widgets = { 'fechaDocumento':DateInput }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields["empleado"].queryset =  proveedor = Persona.objects.filter(esEmpleado=True)
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
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'plan_actividad_zafra_list' %}"> Cancelar</a>""" ))
                ) 
            )
        )

class AjusteStockDetalleForm(forms.ModelForm):
    class Meta:
        model = AjusteStockDetalle
        fields = ['item', 'cantidad',]
        widgets = {'cantidad':DecimalMaskInput}


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
        widgets = {'fechaDocumento':DateInput,'cantidadTrabajada': DecimalMaskInput}
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['totalMaquinaria'].label = False
        #self.fields['totalMaquinaria'].widget = DecimalMaskInput()
        self.fields['totalItem'].label = False
        #self.fields['totalItem'].widget = DecimalMaskInput()
        self.fields["empleado"].queryset =  proveedor = Persona.objects.filter(esEmpleado=True)
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
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'actividad_agricola_list' %}"> Cancelar</a>""" ))
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
        widgets = {'haTrabajada':DecimalMaskInput,'precio':DecimalMaskInput,'subtotalMaquinaria':DecimalMaskInput}

class ActividadAgricolaItemDetalleForm(forms.ModelForm):
    subtotalItem = forms.DecimalField(
        widget=calculation.FormulaInput('costo*cantidad', attrs={'readonly':True}),
        label = "SubTotal"
    )
    class Meta:
        model = ActividadAgricolaItemDetalle
        fields = ['item', 'deposito','dosis','costo','cantidad','porcentajeImpuesto','subtotalItem']
        widgets = {'dosis':DecimalMaskInput,'costo':DecimalMaskInput,'cantidad':DecimalMaskInput,'porcentajeImpuesto':DecimalMaskInput,'subtotalItem':DecimalMaskInput}

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
        #self.fields['cantidad'].widget = DecimalMaskInput()
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
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'pedido_compra_list' %}"> Cancelar</a>""" ))
            ) 
        )

class PedidoCompraDetalleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields["item"].queryset =  item = Item.objects.filter(tipoItem__pk=2) # sea igual a normal
    class Meta:
        model = PedidoCompraDetalle
        fields = ['item', 'cantidad']
        widgets = {'cantidad':DecimalMaskInput}


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
        self.fields['costoPactado'].widget = DecimalMaskInput()
        self.helper.layout = Layout(
            "fecha",
            "zafra",
            "persona",
            "descripcion",
            "costoPactado",
            Row(
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'contrato_list' %}"> Cancelar</a>""" ))
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
        fields = ['fechaDocumento','esCredito','comprobante','cliente','cuenta','deposito','observacion']
        widgets = {'fechaDocumento':DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['total'].label = False
        #self.fields['total'].widget = DecimalMaskInput()
        self.fields['total_iva'].label = False
        #self.fields['total_iva'].widget = DecimalMaskInput()
        self.fields['comprobante'].widget = InvoiceMaskInput()
        self.fields["cliente"].queryset =  proveedor = Persona.objects.filter(esCliente=True)
        self.helper.layout = Layout(
            "fechaDocumento",
            "esCredito",
            "comprobante",
            "cliente",
            "cuenta",
            "deposito",
            "observacion",
            Fieldset(
                u'Detalle',
                Formset(
                    "VentaDetalleInline"#, stacked=True
                ), 
                Formset(
                    "CuotaVentaInline",
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
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'venta_list' %}"> Cancelar</a>""" ))
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
    item = ItemCustomSelect()
    class Meta:
        model = VentaDetalle
        fields = ['item', 'cantidad','precio','porcentajeImpuesto','impuesto','subtotal']
        widgets = {'cantidad':DecimalMaskInput,'precio':DecimalMaskInput,'porcentajeImpuesto':DecimalMaskInput,'impuesto':DecimalMaskInput,'subtotal':DecimalMaskInput}

class CuotaVentaForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.disable_csrf = True
    #     self.helper.form_tag = False
    #     self.helper.include_media = False
    #     self.helper.layout = Layout(
    #         Row(
    #             Column("fechaVencimiento"),  
    #             Column("monto"),   
    #         ),
    #         Column(
    #             'DELETE',
    #             hidden='hidden'
    #         ),
    #         Button("button",  "Eliminar", css_class="btn btn-block btn-danger",data_formset_delete_button=""),
    #     )
    class Meta:
        model = CuotaVenta
        fields = ['fechaVencimiento','monto']
        widgets = { 'fechaVencimiento':DateInput }

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
        fields = ['fechaDocumento','esCredito','comprobante','timbrado','proveedor','cuenta','deposito',"compra",'observacion']
        widgets = {'fechaDocumento':DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['total'].label = False
        #self.fields['total'].widget = DecimalMaskInput()
        self.fields['total_iva'].label = False
        #self.fields['total_iva'].widget = DecimalMaskInput()
        self.fields['comprobante'].widget = InvoiceMaskInput()
        self.fields["proveedor"].queryset =  proveedor = Persona.objects.filter(esProveedor=True)
        self.fields["compra"].queryset =  compra = Compra.objects.filter(esVigente=True)
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
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'nota_credito_recibida_list' %}"> Cancelar</a>""" ))
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
        widgets = {'cantidad':DecimalMaskInput,'valor':DecimalMaskInput,'porcentajeImpuesto':DecimalMaskInput,'impuesto':DecimalMaskInput,'subtotal':DecimalMaskInput}



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
        #self.fields['total'].widget = DecimalMaskInput()
        self.fields['total_iva'].label = False
        #self.fields['total_iva'].widget = DecimalMaskInput()
        self.fields['comprobante'].widget = InvoiceMaskInput()
        self.fields["cliente"].queryset =  proveedor = Persona.objects.filter(esCliente=True)
        self.fields["venta"].queryset =  venta = Venta.objects.filter(esVigente=True)
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
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'nota_credito_recibida_list' %}"> Cancelar</a>""" ))
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
        widgets = {'cantidad':DecimalMaskInput,'valor':DecimalMaskInput,'porcentajeImpuesto':DecimalMaskInput,'impuesto':DecimalMaskInput,'subtotal':DecimalMaskInput}



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
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'transferencia_cuenta_list' %}"> Cancelar</a>""" ))
            ) 
        )



# COBROS
class CobroForm(forms.ModelForm):
    total = forms.DecimalField(
        widget=calculation.SumInput('cancelacion',   attrs={'readonly':True}),
    )
    class Meta:
        model = Cobro
        fields = ['fechaDocumento','comprobante','cliente','cuenta','cobrador','montoASaldar','observacion']
        widgets = {'fechaDocumento':DateInput,'montoASaldar':DecimalMaskInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['total'].label = False
        #self.fields['total'].widget = DecimalMaskInput()
        self.fields['comprobante'].widget = InvoiceMaskInput()
        self.fields["cliente"].queryset =  proveedor = Persona.objects.filter(esCliente=True)
        self.fields["cobrador"].queryset =  proveedor = Persona.objects.filter(esEmpleado=True)
        self.helper.layout = Layout(
            "fechaDocumento",
            "comprobante",
            "cliente",
            "cuenta",
            "cobrador",
            "montoASaldar",
            "observacion",
            Fieldset(
                u'Detalle',
                Formset(
                    "CobroDetalleInline"#, stacked=True
                ), 
                Formset(
                    "CobroMedioInline",
                    stacked=True,
                ), 
            ),
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total: </span>'), css_class="text-right"), Column("total")
            ), 
            Row(
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'cobro_list' %}"> Cancelar</a>""" ))
            ) 
        )

class CobroDetalleForm(forms.ModelForm):
    check = forms.BooleanField(label='Sel.',required=False)
    comprobante = forms.CharField(max_length=30,disabled = True)
    monto = forms.DecimalField(max_digits=15,disabled = True)
    saldo = forms.DecimalField(max_digits=15,disabled = True)
    class Meta:
        model = CobroDetalle
        fields = ['cuotaVenta','check','cancelacion']
        widgets = {
            'cancelacion':DecimalMaskInput,
            'monto':DecimalMaskInput,
            'saldo':DecimalMaskInput,
            'cuotaVenta': forms.HiddenInput
        }

class CobroMedioForm(forms.ModelForm):
    class Meta:
        model = CobroMedio
        fields = ['numero','comprobante','medioCobro','observacion','monto']
        widgets = {'cancelacion':DecimalMaskInput}


# LIQUIDACION AGRICOLA
class LiquidacionAgricolaSelectionForm(forms.ModelForm):
    class Meta:
        model = LiquidacionAgricola
        fields = ['tipo','zafra','proveedor','precioUnitario']
        widgets = {'precioUnitario':DecimalMaskInput}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['zafra'].required = True
        self.fields['zafra'].required = True
        self.fields['tipo'].required = True
        self.fields['precioUnitario'].required = True
        self.fields["proveedor"].queryset =  proveedor = Persona.objects.filter(esProveedor=True)

class LiquidacionAgricolaForm(forms.ModelForm):
    total = forms.DecimalField(
        widget=calculation.SumInput('subtotal',   attrs={'readonly':True}),
    )
    class Meta:
        model = LiquidacionAgricola
        fields = ['fechaDocumento','tipo','zafra','proveedor','precioUnitario','observacion']
        widgets = {'fechaDocumento':DateInput,'precioUnitario':DecimalMaskInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['total'].label = False
        #self.fields['total'].widget = DecimalMaskInput()
        self.fields["proveedor"].queryset =  proveedor = Persona.objects.filter(esProveedor=True)
        self.helper.layout = Layout(
            "fechaDocumento",
            "tipo",
            "zafra",
            "proveedor",
            "precioUnitario",
            "observacion",
            Fieldset(
                u'Detalle',
                Formset(
                    "LiquidacionAgricolaDetalleInline"#, stacked=True
                )
            ),
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total: </span>'), css_class="text-right"), Column("total")
            ), 
            Row(
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'liquidacion_agricola_list' %}"> Cancelar</a>""" ))
            ) 
        )

class LiquidacionAgricolaDetalleForm(forms.ModelForm):
    check = forms.BooleanField(label='Sel.',required=False)
    movimiento = forms.CharField(max_length=300,disabled = True)
    subTotal = forms.DecimalField(max_digits=15,disabled = True)
    subTotal.label = "Sub Total"
    class Meta:
        model = LiquidacionAgricolaDetalle
        fields = ['secuenciaOrigen','finca','lote','cantidad']
        widgets = {
            'secuenciaOrigen': forms.HiddenInput,
            'cantidad':DecimalMaskInput,
            'subTotal':DecimalMaskInput,   
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['finca'].widget.attrs.update({'readonly':True, 'style': 'pointer-events:none;'})
        self.fields['lote'].widget.attrs.update({'readonly':True, 'style': 'pointer-events:none;'})
        self.fields['cantidad'].widget.attrs.update({'readonly':True, 'style': 'pointer-events:none;'})

# NOTA DEBITO RECIBIDA
class NotaDebitoRecibidaForm(forms.ModelForm):
    total = forms.DecimalField(
        widget=calculation.SumInput('subtotal',   attrs={'readonly':True}),
    )
    total_iva = forms.DecimalField(
        widget=calculation.SumInput('impuesto',   attrs={'readonly':True}),
    )
    class Meta:
        model = NotaDebitoRecibida
        fields = ['fechaDocumento','esCredito','comprobante','timbrado','proveedor','cuenta','deposito',"compra",'observacion']
        widgets = {'fechaDocumento':DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['total'].label = False
        #self.fields['total'].widget = DecimalMaskInput()
        self.fields['total_iva'].label = False
        #self.fields['total_iva'].widget = DecimalMaskInput()
        self.fields['comprobante'].widget = InvoiceMaskInput()
        self.fields["proveedor"].queryset =  proveedor = Persona.objects.filter(esProveedor=True)
        self.fields["compra"].queryset =  compra = Compra.objects.filter(esVigente=True)
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
                    "NotaDebitoRecibidaDetalleInline"#, stacked=True
                ), 
                
            ),
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total: </span>'), css_class="text-right"), Column("total")
            ), 
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total Impuesto: </span>'), css_class="text-right"), Column("total_iva")
            ),
            Row(
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'nota_credito_recibida_list' %}"> Cancelar</a>""" ))
            ) 
        )

class NotaDebitoRecibidaDetalleForm(forms.ModelForm):
    subtotal = forms.DecimalField(
        widget=calculation.FormulaInput('valor*cantidad', attrs={'readonly':True}),
        label = "SubTotal"
    )
    impuesto = forms.DecimalField(
        widget=calculation.FormulaInput('parseFloat((subtotal*porcentajeImpuesto)/(porcentajeImpuesto+100)).toFixed(0)', attrs={'readonly':True}),
        label = "Impuesto"
    )
    class Meta:
        model = NotaDebitoRecibidaDetalle
        fields = ['item', 'cantidad','valor','porcentajeImpuesto','impuesto','subtotal']
        widgets = {'cantidad':DecimalMaskInput,'valor':DecimalMaskInput,'porcentajeImpuesto':DecimalMaskInput,'impuesto':DecimalMaskInput,'subtotal':DecimalMaskInput}



# NOTA DE DEBITO EMITIDA
class NotaDebitoEmitidaForm(forms.ModelForm):
    total = forms.DecimalField(
        widget=calculation.SumInput('subtotal',   attrs={'readonly':True}),
    )
    total_iva = forms.DecimalField(
        widget=calculation.SumInput('impuesto',   attrs={'readonly':True}),
    )
    class Meta:
        model = NotaDebitoEmitida
        fields = ['fechaDocumento','esCredito','comprobante', 'timbrado','cliente','cuenta','deposito',"venta",'observacion']
        widgets = {'fechaDocumento':DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['total'].label = False
        #self.fields['total'].widget = DecimalMaskInput()
        self.fields['total_iva'].label = False
        #self.fields['total_iva'].widget = DecimalMaskInput()
        self.fields['comprobante'].widget = InvoiceMaskInput()
        self.fields["cliente"].queryset =  proveedor = Persona.objects.filter(esCliente=True)
        self.fields["venta"].queryset =  venta = Venta.objects.filter(esVigente=True)
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
                    "NotaDebitoEmitidaDetalleInline"#, stacked=True
                ), 
                
            ),
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total: </span>'), css_class="text-right"), Column("total")
            ), 
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total Impuesto: </span>'), css_class="text-right"), Column("total_iva")
            ),
            Row(
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'nota_credito_recibida_list' %}"> Cancelar</a>""" ))
            ) 
        )

class NotaDebitoEmitidaDetalleForm(forms.ModelForm):
    subtotal = forms.DecimalField(
        widget=calculation.FormulaInput('valor*cantidad', attrs={'readonly':True}),
        label = "SubTotal"
    )
    impuesto = forms.DecimalField(
        widget=calculation.FormulaInput('parseFloat((subtotal*porcentajeImpuesto)/(porcentajeImpuesto+100)).toFixed(0)', attrs={'readonly':True}),
        label = "Impuesto"
    )
    class Meta:
        model = NotaDebitoEmitidaDetalle
        fields = ['item', 'cantidad','valor','porcentajeImpuesto','impuesto','subtotal']
        widgets = {'cantidad':DecimalMaskInput,'valor':DecimalMaskInput,'porcentajeImpuesto':DecimalMaskInput,'impuesto':DecimalMaskInput,'subtotal':DecimalMaskInput}


# CIERRE DE ZAFRAS
class CierreZafraForm(forms.ModelForm):

    totalCostoV = forms.DecimalField(
        widget=calculation.SumInput('costoTotal',   attrs={'readonly':True}),
    )
    totalAcopiadoV = forms.DecimalField(
        widget=calculation.SumInput('cantidadAcopioNeto',   attrs={'readonly':True}),
    )
    totalCultivadoV = forms.DecimalField(
        widget=calculation.SumInput('haCultivada',   attrs={'readonly':True}),
    )
    class Meta:
        model = CierreZafra
        fields = ['fecha', 'zafra', 'observacion']
        widgets = {'fecha':DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['totalCostoV'].label = False
        #self.fields['totalCostoV'].widget = DecimalMaskInput()
        self.fields['totalAcopiadoV'].label = False
        #self.fields['totalAcopiadoV'].widget = DecimalMaskInput()
        self.fields['totalCultivadoV'].label = False
        #self.fields['totalCultivadoV'].widget = DecimalMaskInput()
        self.helper.layout = Layout(
            "fecha",
            "zafra",
            "observacion",
            Fieldset(
                u'Detalle',
                Formset(
                    "CierreZafraDetalleInline"#, stacked=True
                ),  
            ),
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total HA Cultivada: </span>'), css_class="text-right"), Column("totalCultivadoV"),
            ), 
             Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total Acopiado: </span>'), css_class="text-right"), Column("totalAcopiadoV"),
            ), 
             Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total Costo: </span>'), css_class="text-right"), Column("totalCostoV")
            ), 
            Row(
                Div(Submit("submit", "Guardar",css_class = "btn btn-success"), HTML("""<a class="btn btn-secondary" href="{% url 'cierre_zafra_list' %}"> Cancelar</a>""" ))
            ) 
        )

class CierreZafraDetalleForm(forms.ModelForm):
    check = forms.BooleanField(label='Sel.',required=False)
    class Meta:
        model = CierreZafraDetalle
        fields = ['check','finca','haCultivada','cantidadAcopioNeto','rendimiento','costoTotal','costoHA','costoUnit']
        widgets = {'haCultivada':DecimalMaskInput,'cantidadAcopioNeto':DecimalMaskInput,'cantidadAcopioNeto':DecimalMaskInput,'rendimiento':DecimalMaskInput,'costoTotal':DecimalMaskInput,'costoHA':DecimalMaskInput,'costoUnit':DecimalMaskInput}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['finca'].widget.attrs.update({'readonly':True, 'style': 'pointer-events:none;'})
        self.fields['haCultivada'].widget.attrs.update({'readonly':True, 'style': 'pointer-events:none;'})
        self.fields['cantidadAcopioNeto'].widget.attrs.update({'readonly':True, 'style': 'pointer-events:none;'})
        self.fields['rendimiento'].widget.attrs.update({'readonly':True, 'style': 'pointer-events:none;'})
        self.fields['costoTotal'].widget.attrs.update({'readonly':True, 'style': 'pointer-events:none;'})
        self.fields['costoHA'].widget.attrs.update({'readonly':True, 'style': 'pointer-events:none;'})
        self.fields['costoUnit'].widget.attrs.update({'readonly':True, 'style': 'pointer-events:none;'})

class CierreZafraSelectionForm(forms.ModelForm):
    class Meta:
        model = CierreZafra
        fields = ['zafra']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['zafra'].required = True
        self.fields["zafra"].queryset =  zafra = Zafra.objects.filter(estaCerrado=False)
