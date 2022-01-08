from extra_views.advanced import InlineFormSetFactory

from .models import AcopioCalificacion, AcopioDetalle, AjusteStockDetalle, CompraDetalle, OrdenCompra, OrdenCompraDetalle, PedidoCompraDetalle, PlanActividadZafraDetalle
from .forms import AcopioCalificacionForm, AcopioDetalleForm, AjusteStockDetalleForm, CompraDetalleForm, OrdenCompraDetalleForm, PedidoCompraDetalleForm, PlanActividadZafraDetalleForm

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

class AjusteStockDetalleInline(InlineFormSetFactory):
    model = AjusteStockDetalle
    form_class = AjusteStockDetalleForm
    factory_kwargs = {'extra':1 }
    fields = ['item', 'cantidad',]