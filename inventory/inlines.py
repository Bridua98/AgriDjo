from extra_views.advanced import InlineFormSetFactory

from .models import AcopioCalificacion, AcopioDetalle, ActividadAgricolaItemDetalle, ActividadAgricolaMaquinariaDetalle, AjusteStockDetalle, CierreZafraDetalle, CobroDetalle, CobroMedio, CompraDetalle, CuotaCompra, CuotaVenta, LiquidacionAgricolaDetalle, NotaCreditoEmitidaDetalle, NotaCreditoRecibida, NotaCreditoRecibidaDetalle, NotaDebitoEmitidaDetalle, NotaDebitoRecibidaDetalle, OrdenCompra, OrdenCompraDetalle, PedidoCompraDetalle, PlanActividadZafraDetalle, VentaDetalle
from .forms import AcopioCalificacionForm, AcopioDetalleForm, ActividadAgricolaItemDetalleForm, ActividadAgricolaMaquinariaDetalleForm, AjusteStockDetalleForm, CierreZafraDetalleForm, CobroDetalleForm, CobroMedioForm, CompraDetalleForm, CuotaCompraForm, CuotaVentaForm, LiquidacionAgricolaDetalleForm, NotaCreditoEmitidaDetalleForm, NotaCreditoRecibidaDetalleForm, NotaCreditoRecibidaForm, NotaDebitoEmitidaDetalleForm, NotaDebitoRecibidaDetalleForm, OrdenCompraDetalleForm, PedidoCompraDetalleForm, PlanActividadZafraDetalleForm, VentaDetalleForm
from django import forms
class PlanActividadZafraDetalleInline(InlineFormSetFactory):
    model = PlanActividadZafraDetalle
    form_class = PlanActividadZafraDetalleForm
    factory_kwargs = {'extra':1 }
    fields =  ['fechaActividad', 'finca', 'tipoActividadAgricola','descripcion','costo']

class AcopioDetalleInline(InlineFormSetFactory):
    model = AcopioDetalle
    form_class = AcopioDetalleForm
    factory_kwargs = {'extra':1 }
    fields = ['acopio', 'finca', 'lote', 'peso']

class AcopioCalificacionDetalleInline(InlineFormSetFactory):
    model = AcopioCalificacion
    form_class = AcopioCalificacionForm
    factory_kwargs = {'extra':1 }
    fields = ['acopio', 'calificacionAgricola', 'grado', 'porcentaje','peso']

class PedidoCompraDetalleInline(InlineFormSetFactory):
    model = PedidoCompraDetalle
    form_class = PedidoCompraDetalleForm
    factory_kwargs = {'extra':1 }
    fields =  ['item','cantidad']

class OrdenCompraDetalleInline(InlineFormSetFactory):
    model = OrdenCompraDetalle
    form_class = OrdenCompraDetalleForm
    factory_kwargs = {'extra':1 }
    fields = ['item', 'cantidad','precio','descuento']

class CompraDetalleInline(InlineFormSetFactory):
    model = CompraDetalle
    form_class = CompraDetalleForm
    factory_kwargs = {'extra':1 }
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
    factory_kwargs = {'extra':1 }
    fields = ['item', 'cantidad',]

class ActividadAgricolaMaquinariaDetalleInline(InlineFormSetFactory):
    model = ActividadAgricolaMaquinariaDetalle
    form_class = ActividadAgricolaMaquinariaDetalleForm
    factory_kwargs = {'extra':1 }
    fields = ['maquinaria', 'haTrabajada','precio','subtotalMaquinaria']

class ActividadAgricolaItemDetalleInline(InlineFormSetFactory):
    model = ActividadAgricolaItemDetalle
    form_class = ActividadAgricolaItemDetalleForm
    factory_kwargs = {'extra':1 }
    fields = ['item', 'deposito','dosis','costo','cantidad','porcentajeImpuesto','subtotalItem']

class VentaDetalleInline(InlineFormSetFactory):
    model = VentaDetalle
    form_class = VentaDetalleForm
    factory_kwargs = {'extra':1 }
    fields = ['item', 'cantidad','precio','porcentajeImpuesto',]

class NotaCreditoRecibidaDetalleInline(InlineFormSetFactory):
    model = NotaCreditoRecibidaDetalle
    form_class = NotaCreditoRecibidaDetalleForm
    factory_kwargs = {'extra':1 }
    fields = ['esDevolucion','item', 'cantidad','valor','porcentajeImpuesto',]

class NotaCreditoEmitidaDetalleInline(InlineFormSetFactory):
    model = NotaCreditoEmitidaDetalle
    form_class = NotaCreditoEmitidaDetalleForm
    factory_kwargs = {'extra':1 }
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
    factory_kwargs = {'extra':1 }
    fields = ['item', 'cantidad','valor','porcentajeImpuesto',]


class NotaDebitoEmitidaDetalleInline(InlineFormSetFactory):
    model = NotaDebitoEmitidaDetalle
    form_class = NotaDebitoEmitidaDetalleForm
    factory_kwargs = {'extra':1 }
    fields = ['item', 'cantidad','valor','porcentajeImpuesto',]

class CierreZafraDetalleInline(InlineFormSetFactory):
    model = CierreZafraDetalle
    form_class = CierreZafraDetalleForm
    factory_kwargs = {'extra':1 }
    fields = ['check','finca','haCultivada','cantidadAcopioNeto','rendimiento','costoTotal','costoHA','costoUnit',]