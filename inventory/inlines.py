from extra_views.advanced import InlineFormSetFactory
from inventory.widgets import DecimalMaskInput, ItemCustomSelect, MaquinariaCustomSelect

from .models import AcopioCalificacion, AcopioDetalle, ActividadAgricolaItemDetalle, ActividadAgricolaMaquinariaDetalle, AjusteStockDetalle, CierreZafraDetalle, CobroDetalle, CobroMedio, CompraDetalle, CuotaCompra, CuotaVenta, LiquidacionAgricolaDetalle, NotaCreditoEmitidaDetalle, NotaCreditoRecibida, NotaCreditoRecibidaDetalle, NotaDebitoEmitidaDetalle, NotaDebitoRecibidaDetalle, OrdenCompra, OrdenCompraDetalle, PedidoCompraDetalle, PlanActividadZafraDetalle, VentaDetalle
from .forms import AcopioCalificacionForm, AcopioDetalleForm, ActividadAgricolaItemDetalleForm, ActividadAgricolaMaquinariaDetalleForm, AjusteStockDetalleForm, CierreZafraDetalleForm, CobroDetalleForm, CobroMedioForm, CompraDetalleForm, CuotaCompraForm, CuotaVentaForm, LiquidacionAgricolaDetalleForm, NotaCreditoEmitidaDetalleForm, NotaCreditoRecibidaDetalleForm, NotaCreditoRecibidaForm, NotaDebitoEmitidaDetalleForm, NotaDebitoRecibidaDetalleForm, OrdenCompraDetalleForm, PedidoCompraDetalleForm, PlanActividadZafraDetalleForm, VentaDetalleForm
from django import forms
from django.forms import widgets
class PlanActividadZafraDetalleInline(InlineFormSetFactory):
    model = PlanActividadZafraDetalle
    form_class = PlanActividadZafraDetalleForm
    factory_kwargs = {
        'extra':1 ,
        'widgets':{
            'fechaActividad':widgets.DateInput(
                attrs={
                    'wrapper_class':'col-sm-1',
                    'type':'date'
                }
            ),
            'finca':widgets.Select(
                attrs={
                    'wrapper_class':'col-sm-2',
                }
            ),
            'tipoActividadAgricola':widgets.Select(
                attrs={
                    'wrapper_class':'col-sm-2',
                }
            ),
            'costo':DecimalMaskInput(
                attrs={
                    'wrapper_class':'col-sm-2',
                }
            ),

        }
    }
    fields =  ['fechaActividad', 'finca', 'tipoActividadAgricola','descripcion','costo']

class AcopioDetalleInline(InlineFormSetFactory):
    model = AcopioDetalle
    form_class = AcopioDetalleForm
    factory_kwargs = {
        'extra':1 ,
        'widgets':{
            'finca':widgets.Select(
                attrs={
                    'wrapper_class':'col-sm-5',
                }
            ),
            'lote':widgets.Select(
                attrs={
                    'wrapper_class':'col-sm-4',
                }
            ),
            #'peso':DecimalMaskInput()
        }
    }
    fields = ['acopio', 'finca', 'lote', 'peso']

class AcopioCalificacionDetalleInline(InlineFormSetFactory):
    model = AcopioCalificacion
    form_class = AcopioCalificacionForm
    factory_kwargs = {
        'extra':1 ,
        'widgets':{
            'calificacionAgricola':widgets.Select(
                attrs={
                    'wrapper_class':'col-sm-5',
                }
            ),

        }
    }
    fields = ['acopio', 'calificacionAgricola', 'grado', 'porcentaje','peso']

class PedidoCompraDetalleInline(InlineFormSetFactory):
    model = PedidoCompraDetalle
    form_class = PedidoCompraDetalleForm
    factory_kwargs = {
        'extra':1,
        'widgets':{
            'item':widgets.Select(
                attrs={
                    'wrapper_class':'col-sm-10',
                }
            ),
            'cantidad':widgets.NumberInput(
                attrs={
                    'wrapper_class':'col-sm-2',
                    'class':'text-right',
                }
            ),
        }
    }
    fields =  ['item','cantidad']

class OrdenCompraDetalleInline(InlineFormSetFactory):
    model = OrdenCompraDetalle
    form_class = OrdenCompraDetalleForm
    factory_kwargs = {
        'extra':1,
        'widgets':{
            'item':widgets.Select(
                attrs={
                    'wrapper_class':'col-sm-4',
                }
            ),
            'cantidad':widgets.NumberInput(
                attrs={
                    'wrapper_class':'col-sm-1',
                    'class':'text-right',
                }
            ),
        } 
    
    }

    fields = ['item', 'cantidad','precio','descuento']

class CompraDetalleInline(InlineFormSetFactory):
    model = CompraDetalle
    form_class = CompraDetalleForm
    factory_kwargs = {
        'extra':1 ,
        'widgets':{
            'item':ItemCustomSelect(
                attrs={
                    'wrapper_class':'col-sm-4',
                    'data-item-select':True,

                }
            ),
            'cantidad':widgets.NumberInput(
                attrs={
                    'wrapper_class':'col-sm-1',
                    'class':'text-right',
                }
            ),
            'costo':widgets.NumberInput(
                attrs={
                    'class':'text-right item-costo',
                }
            ),
            'porcentajeImpuesto':widgets.NumberInput(
                attrs={
                    'class':'text-right item-porcentaje-impuesto',
                }
            ),
        }
    }
    fields = ['item', 'cantidad','costo','porcentajeImpuesto',]

class CuotaCompraInline(InlineFormSetFactory):
    model = CuotaCompra
    form_class =CuotaCompraForm
    factory_kwargs = {'extra':1 }
    fields = ['fechaVencimiento','monto']

class CuotaVentaInline(InlineFormSetFactory):
    model = CuotaVenta
    form_class =CuotaVentaForm
    factory_kwargs = {'extra':1 }
    fields = ['fechaVencimiento','monto']

class AjusteStockDetalleInline(InlineFormSetFactory):
    model = AjusteStockDetalle
    form_class = AjusteStockDetalleForm
    factory_kwargs = {
        'extra':1 ,
        'widgets':{
            'item':widgets.Select(
                attrs={
                    'wrapper_class':'col-sm-10',
                }
            ),
            'cantidad':widgets.NumberInput(
                attrs={
                    'wrapper_class':'col-sm-2',
                    'class':'text-right',
                }
            ),
        } 
    }
    fields = ['item', 'cantidad',]

class ActividadAgricolaMaquinariaDetalleInline(InlineFormSetFactory):
    model = ActividadAgricolaMaquinariaDetalle
    form_class = ActividadAgricolaMaquinariaDetalleForm
    factory_kwargs = {
        'extra':1,
        'widgets':{
            'maquinaria':MaquinariaCustomSelect(
                attrs={
                    'wrapper_class':'col-sm-4',
                    'data-maquinaria-select':True,
                }
            ),
            'precio':widgets.NumberInput(
                attrs={
                    'class':'text-right precio-ha',
                }
            ),
        } 
    }
    fields = ['maquinaria', 'haTrabajada','precio','subtotalMaquinaria']

class ActividadAgricolaItemDetalleInline(InlineFormSetFactory):
    model = ActividadAgricolaItemDetalle
    form_class = ActividadAgricolaItemDetalleForm
    factory_kwargs = {
        'extra':1, 
        'widgets':{
            'item':ItemCustomSelect(
                attrs={
                    'wrapper_class':'col-sm-2',
                    'data-item-select':True,
                }
            ),
            'porcentajeImpuesto':widgets.NumberInput(
                attrs={
                    'class':'text-right item-porcentaje-impuesto',
                }
            ),
            'costo':widgets.NumberInput(
                attrs={
                    'class':'text-right item-costo',
                }
            ),
            'cantidad':widgets.NumberInput(
                attrs={
                    'wrapper_class':'col-sm-1',
                }
            ),
        }
    }
    fields = ['item', 'deposito','dosis','costo','cantidad','porcentajeImpuesto','subtotalItem']

class VentaDetalleInline(InlineFormSetFactory):
    model = VentaDetalle
    form_class = VentaDetalleForm
    factory_kwargs = {
        'extra':1,
        'widgets':{
            'item':ItemCustomSelect(
                attrs={
                    'wrapper_class':'col-sm-4',
                    'data-item-select':True,
                }
            ),
            'porcentajeImpuesto':widgets.NumberInput(
                attrs={
                    'class':'text-right item-porcentaje-impuesto',
                }
            ),
            'precio':widgets.NumberInput(
                attrs={
                    'class':'text-right item-precio',
                }
            ),
            'cantidad':widgets.NumberInput(
                attrs={
                    'wrapper_class':'col-sm-1',
                }
            ),
        }

    }
    fields = ['item', 'cantidad','precio','porcentajeImpuesto',]

class NotaCreditoRecibidaDetalleInline(InlineFormSetFactory):
    model = NotaCreditoRecibidaDetalle
    form_class = NotaCreditoRecibidaDetalleForm
    factory_kwargs = {
        'extra':1, 
        'widgets':{
            'item':ItemCustomSelect(
                attrs={
                    'wrapper_class':'col-sm-3',
                    'data-item-select':True,
                }
            ),
            'porcentajeImpuesto':widgets.NumberInput(
                attrs={
                    'class':'text-right item-porcentaje-impuesto',
                }
            ),
            'valor':widgets.NumberInput(
                attrs={
                    'class':'text-right item-costo',
                }
            ),
            'cantidad':widgets.NumberInput(
                attrs={
                    'wrapper_class':'col-sm-1',
                }
            ),
        }        
    }
    fields = ['esDevolucion','item', 'cantidad','valor','porcentajeImpuesto',]

class NotaCreditoEmitidaDetalleInline(InlineFormSetFactory):
    model = NotaCreditoEmitidaDetalle
    form_class = NotaCreditoEmitidaDetalleForm
    factory_kwargs = {
        'extra':1,
        'widgets':{
            'item':ItemCustomSelect(
                attrs={
                    'wrapper_class':'col-sm-3',
                    'data-item-select':True,
                }
            ),
            'porcentajeImpuesto':widgets.NumberInput(
                attrs={
                    'class':'text-right item-porcentaje-impuesto',
                }
            ),
            'valor':widgets.NumberInput(
                attrs={
                    'class':'text-right item-precio',
                }
            ),
            'cantidad':widgets.NumberInput(
                attrs={
                    'wrapper_class':'col-sm-1',
                }
            ),
        } 
    
    }
    fields = ['esDevolucion','item', 'cantidad','valor','porcentajeImpuesto',]

class CobroDetalleInline(InlineFormSetFactory):
    model = CobroDetalle
    form_class = CobroDetalleForm
    factory_kwargs = {'extra':1 }
    fields = ['cuotaVenta','check','comprobante', 'monto', 'saldo','cancelacion',]

class CobroMedioInline(InlineFormSetFactory):
    model = CobroMedio
    form_class = CobroMedioForm
    factory_kwargs = {'extra':1}
    fields = ['numero','comprobante','medioCobro','observacion','monto',]

class LiquidacionAgricolaDetalleInline(InlineFormSetFactory):
    model = LiquidacionAgricolaDetalle
    form_class = LiquidacionAgricolaDetalleForm
    factory_kwargs = {'extra':1 }
    fields = ['secuenciaOrigen','check','movimiento', 'finca', 'lote','cantidad','subTotal']

class NotaDebitoRecibidaDetalleInline(InlineFormSetFactory):
    model = NotaDebitoRecibidaDetalle
    form_class = NotaDebitoRecibidaDetalleForm
    factory_kwargs = {
        'extra':1,
        'widgets':{
            'item':ItemCustomSelect(
                attrs={
                    'wrapper_class':'col-sm-3',
                    'data-item-select':True,
                }
            ),
            'porcentajeImpuesto':widgets.NumberInput(
                attrs={
                    'class':'text-right item-porcentaje-impuesto',
                }
            ),
            'valor':widgets.NumberInput(
                attrs={
                    'class':'text-right item-costo',
                }
            ),
            'cantidad':widgets.NumberInput(
                attrs={
                    'wrapper_class':'col-sm-1',
                }
            ),
        }
    }
    fields = ['item', 'cantidad','valor','porcentajeImpuesto',]


class NotaDebitoEmitidaDetalleInline(InlineFormSetFactory):
    model = NotaDebitoEmitidaDetalle
    form_class = NotaDebitoEmitidaDetalleForm
    factory_kwargs = {
        'extra':1,
        'widgets':{
            'item':ItemCustomSelect(
                attrs={
                    'wrapper_class':'col-sm-3',
                    'data-item-select':True,
                }
            ),
            'porcentajeImpuesto':widgets.NumberInput(
                attrs={
                    'class':'text-right item-porcentaje-impuesto',
                }
            ),
            'valor':widgets.NumberInput(
                attrs={
                    'class':'text-right item-precio',
                }
            ),
            'cantidad':widgets.NumberInput(
                attrs={
                    'wrapper_class':'col-sm-1',
                }
            ),
        }  
    
    }
    fields = ['item', 'cantidad','valor','porcentajeImpuesto',]

class CierreZafraDetalleInline(InlineFormSetFactory):
    model = CierreZafraDetalle
    form_class = CierreZafraDetalleForm
    factory_kwargs = {'extra':1 }
    fields = ['check','finca','haCultivada','cantidadAcopioNeto','rendimiento','costoTotal','costoHA','costoUnit',]