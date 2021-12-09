from extra_views.advanced import InlineFormSetFactory

from .models import AcopioDetalle, PlanActividadZafraDetalle
from .forms import AcopioDetalleForm, PlanActividadZafraDetalleForm

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