import base64
import datetime
import hashlib
import imghdr
import logging
import os
import pathlib
import uuid
from io import BytesIO
from os import path

from django.conf import settings
from django.contrib.admin.utils import NestedObjects
from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models, transaction
from django.forms.formsets import all_valid
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.encoding import force_text
from django.utils.text import capfirst
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_tables2 import SingleTableMixin
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from num2words import num2words
from xhtml2pdf import pisa
from inventory.filters import CompraInformeFilter, InventarioDepositoInformeFilter, LibroCompraFilter, LibroVentaFilter, ProduccionAgricolaInformeFilter, VentaInformeFilter
from django_filters.views import FilterView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django_tables2 import SingleTableMixin

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from inventory.mixins import FormsetInlinesMetaMixin, SearchViewMixin
from inventory.tables import CierreZafraTable, CobroTable, LiquidacionAgricolaTable, NotaDebitoEmitidaTable, NotaDebitoRecibidaTable, UserTable

from .forms import CierreZafraForm, CobroForm, CustomUserChangeForm, CustomUserCreationForm, LiquidacionAgricolaForm, NotaDebitoEmitidaForm, NotaDebitoRecibidaForm

from inventory.forms import (AcopioForm, ActividadAgricolaForm,
                             AjusteStockForm, CompraForm, ContratoForm, CuotaCompraForm, CuotaVentaForm,
                             NotaCreditoEmitidaForm, NotaCreditoRecibidaForm,
                             OrdenCompraForm, PedidoCompraForm,
                             PlanActividadZafraForm, TransferenciaCuentaForm, VentaForm)
from inventory.inlines import (AcopioCalificacionDetalleInline,
                               AcopioDetalleInline,
                               ActividadAgricolaItemDetalleInline,
                               ActividadAgricolaMaquinariaDetalleInline,
                               AjusteStockDetalleInline, CierreZafraDetalleInline, CobroDetalleInline, CobroMedioInline, CompraDetalleInline, CuotaCompraInline, CuotaVentaInline, LiquidacionAgricolaDetalleInline,
                               NotaCreditoEmitidaDetalleInline,
                               NotaCreditoRecibidaDetalleInline, NotaDebitoEmitidaDetalleInline, NotaDebitoRecibidaDetalleInline,
                               OrdenCompraDetalleInline,
                               PedidoCompraDetalleInline,
                               PlanActividadZafraDetalleInline,
                               VentaDetalleInline)
from inventory.mixins import FormsetInlinesMetaMixin, SearchViewMixin
from inventory.models import (Acopio, ActividadAgricola, AjusteStock,
                              AperturaCaja, Arqueo, Banco,
                              CalificacionAgricola, Categoria, CierreZafra, Cobro, CobroDetalle, Compra,
                              Contrato, Cuenta, CuotaVenta, Deposito, Finca, Item, ItemMovimiento, LiquidacionAgricola, Lote,
                              MaquinariaAgricola, Marca, NotaCreditoEmitida,
                              NotaCreditoRecibida, NotaDebitoEmitida, NotaDebitoRecibida, OrdenCompra, PedidoCompra,
                              Persona, PlanActividadZafra,
                              TipoActividadAgricola, TipoImpuesto,
                              TipoMaquinariaAgricola, TransferenciaCuenta, Venta, Zafra)
from inventory.tables import (AcopioTable, ActividadAgricolaTable,
                              AjusteStockTable, AperturaCajaTable, ArqueoTable,
                              BancoTable, CalificacionAgricolaTable,
                              CategoriaTable, CompraInformeTable, CompraTable, ContratoTable,
                              CuentaTable, DepositoTable, FincaTable, InventarioDepositoInformeTable,
                              ItemTable, LibroCompraTable, LibroVentaTable, LoteTable, MaquinariaAgricolaTable,
                              MarcaTable, NotaCreditoEmitidaTable,
                              NotaCreditoRecibidaTable, OrdenCompraTable,
                              PedidoCompraTable, PersonaTable,
                              PlanActividadZafraTable, ProduccionAgricolaInformeTable,
                              TipoActividadAgricolaTable, TipoImpuestoTable,
                              TipoMaquinariaAgricolaTable, TransferenciaCuentaTable, VentaInformeTable, VentaTable,
                              ZafraTable)
from inventory.utils import link_callback

from django.db.models import Q

from .widgets import DateInput

@login_required
def main(request):
    template_path = "home.html"
    context_p = {
        'invoice_css_dir': settings.INVOICE_CSS_DIR,
        'invoice_img_dir': settings.INVOICE_IMG_DIR,
    }
    return render(request, template_name=template_path, context=context_p)


def menu(request):
    return render(request, template_name="menu_dummy.html", context={})

class CustomDeleteView(DeleteView):
    error = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error'] = self.error
        return context

    def before_delete(self):
        pass

    def delete(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            success_url = self.get_success_url()
            self.before_delete()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        except Exception as e:
            self.error = e
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)

def get_deleted_objects(objs):
    """
    get related objects to delete
    """
    collector = NestedObjects(using='default')
    collector.collect(objs)

    def format_callback(obj):
        opts = obj._meta
        no_edit_link = '%s: %s' % (capfirst(opts.verbose_name),
                                   force_text(obj))
        return no_edit_link

    to_delete = collector.nested(format_callback)
    protected = [format_callback(obj) for obj in collector.protected]
    model_count = {model._meta.verbose_name_plural: len(
        objs) for model, objs in collector.model_objs.items()}
    return to_delete, model_count, protected

class CreateWithFormsetInlinesView(FormsetInlinesMetaMixin, CreateWithInlinesView):
    """
    Create view con soporte para formset inlines
    """
    def run_form_extra_validation(self, form, inlines):
        """ ejecutar validaciones adicionales de formularios """

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #initial_object = self.object
        inlines = self.construct_inlines()
        try:
            with transaction.atomic():
                if form.is_valid():
                    self.object = form.save(commit=False)
                    form_validated = True
                else:
                    form_validated = False
                # Loop through inlines to set master instance
                for inline in inlines:
                    inline.instance = form.instance

                if all_valid(inlines) and form_validated:
                    response = self.forms_valid(form, inlines)
                    self.run_form_extra_validation(form, inlines)
                    if not form.errors and response:
                        return response
                raise ValidationError('Error')
        except ValidationError:
            pass
        #self.object = initial_object
        return self.forms_invalid(form, inlines)


class UpdateWithFormsetInlinesView(FormsetInlinesMetaMixin, UpdateWithInlinesView):
    """
    Update view con soporte para formset inlines
    """

    def run_form_extra_validation(self, form, inlines):
        """ ejecutar validaciones adicionales de formularios """

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        initial_object = self.object
        inlines = self.construct_inlines()
        try:
            with transaction.atomic():
                if form.is_valid():
                    self.object = form.save(commit=False)
                    form_validated = True
                else:
                    form_validated = False
                # Loop through inlines to set master instance
                for inline in inlines:
                    inline.instance = form.instance

                if all_valid(inlines) and form_validated:
                    response = self.forms_valid(form, inlines)
                    self.run_form_extra_validation(form, inlines)
                    if not form.errors and response:
                        return response
                raise ValidationError('Error')
        except ValidationError:
            pass
        self.object = initial_object
        return self.forms_invalid(form, inlines)


# TIPO DE ACTIVIDAD AGRICOLA
class TipoActividadAgricolaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = TipoActividadAgricola
    table_class = TipoActividadAgricolaTable
    paginate_by = 6
    search_fields = ['descripcion']
    template_name = 'inventory/tipo_actividad_agricola_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'tipo_actividad_agricola_update'
        context['delete_url'] = 'tipo_actividad_agricola_delete'
        return context

class TipoActividadAgricolaCreateView(LoginRequiredMixin,CreateView):
    model = TipoActividadAgricola
    template_name = 'inventory/tipo_actividad_agricola_create.html'
    fields = ['descripcion','esCosecha','esSiembra','esResiembra']

    def get_success_url(self):
        return reverse_lazy("tipo_actividad_agricola_list")

class TipoActividadAgricolaUpdateView(LoginRequiredMixin,UpdateView):
    model = TipoActividadAgricola
    template_name = 'inventory/tipo_actividad_agricola_update.html'
    fields = ['descripcion','esCosecha','esSiembra','esResiembra']

    def get_success_url(self):
        return reverse_lazy("tipo_actividad_agricola_list")

class TipoActividadAgricolaDeleteView(LoginRequiredMixin,DeleteView):
    model = TipoActividadAgricola
    template_name = 'inventory/tipo_actividad_agricola_delete.html'

    def get_success_url(self):
        return reverse_lazy("tipo_actividad_agricola_list")


# FINCA
class FincaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Finca
    table_class = FincaTable
    paginate_by = 6
    search_fields = ['descripcion','ubicacion']
    template_name = 'inventory/finca_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'finca_update'
        context['delete_url'] = 'finca_delete'
        return context

class FincaCreateView(LoginRequiredMixin,CreateView):
    model = Finca
    template_name = 'inventory/finca_create.html'
    fields = ['descripcion','dimensionHa','ubicacion']

    def get_success_url(self):
        return reverse_lazy("finca_list")

class FincaUpdateView(LoginRequiredMixin,UpdateView):
    model = Finca
    template_name = 'inventory/finca_update.html'
    fields = ['descripcion','dimensionHa','ubicacion']

    def get_success_url(self):
        return reverse_lazy("finca_list")

class FincaDeleteView(LoginRequiredMixin,DeleteView):
    model = Finca
    template_name = 'inventory/finca_delete.html'

    def get_success_url(self):
        return reverse_lazy("finca_list")


# TIPO IMPUESTO
class TipoImpuestoListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = TipoImpuesto
    table_class = TipoImpuestoTable
    paginate_by = 6
    search_fields = ['descripcion']
    template_name = 'inventory/tipo_impuesto_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'tipo_impuesto_update'
        context['delete_url'] = 'tipo_impuesto_delete'
        return context

class TipoImpuestoCreateView(LoginRequiredMixin,CreateView):
    model = TipoImpuesto
    template_name = 'inventory/tipo_impuesto_create.html'
    fields = ['descripcion','porcentaje','esIva']

    def get_success_url(self):
        return reverse_lazy("tipo_impuesto_list")

class TipoImpuestoUpdateView(LoginRequiredMixin,UpdateView):
    model = TipoImpuesto
    template_name = 'inventory/tipo_impuesto_update.html'
    fields = ['descripcion','porcentaje','esIva']

    def get_success_url(self):
        return reverse_lazy("tipo_impuesto_list")

class TipoImpuestoDeleteView(LoginRequiredMixin,DeleteView):
    model = TipoImpuesto
    template_name = 'inventory/tipo_impuesto_delete.html'

    def get_success_url(self):
        return reverse_lazy("tipo_impuesto_list")

# TIPO MAQUINARIA AGRICOLA

class TipoMaquinariaAgricolaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = TipoMaquinariaAgricola
    table_class = TipoMaquinariaAgricolaTable
    paginate_by = 6
    search_fields = ['descripcion']
    template_name = 'inventory/tipo_maquinaria_agricola_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'tipo_maquinaria_agricola_update'
        context['delete_url'] = 'tipo_maquinaria_agricola_delete'
        return context

class TipoMaquinariaAgricolaCreateView(LoginRequiredMixin,CreateView):
    model = TipoMaquinariaAgricola
    template_name = 'inventory/tipo_maquinaria_agricola_create.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("tipo_maquinaria_agricola_list")

class TipoMaquinariaAgricolaUpdateView(LoginRequiredMixin,UpdateView):
    model = TipoMaquinariaAgricola
    template_name = 'inventory/tipo_maquinaria_agricola_update.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("tipo_maquinaria_agricola_list")

class TipoMaquinariaAgricolaDeleteView(LoginRequiredMixin,DeleteView):
    model = TipoMaquinariaAgricola
    template_name = 'inventory/tipo_maquinaria_agricola_delete.html'

    def get_success_url(self):
        return reverse_lazy("tipo_maquinaria_agricola_list")


# MARCA
class MarcaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Marca
    table_class = MarcaTable
    paginate_by = 6
    search_fields = ['descripcion']
    template_name = 'inventory/marca_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'marca_update'
        context['delete_url'] = 'marca_delete'
        return context

class MarcaCreateView(LoginRequiredMixin,CreateView):
    model = Marca
    template_name = 'inventory/marca_create.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("marca_list")

class MarcaUpdateView(LoginRequiredMixin,UpdateView):
    model = Marca
    template_name = 'inventory/marca_update.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("marca_list")

class MarcaDeleteView(LoginRequiredMixin,DeleteView):
    model = Marca
    template_name = 'inventory/marca_delete.html'

    def get_success_url(self):
        return reverse_lazy("marca_list")


# BANCO
class BancoListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Banco
    table_class = BancoTable
    paginate_by = 6
    search_fields = ['descripcion']
    template_name = 'inventory/banco_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'banco_update'
        context['delete_url'] = 'banco_delete'
        return context

class BancoCreateView(LoginRequiredMixin,CreateView):
    model = Banco
    template_name = 'inventory/banco_create.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("banco_list")

class BancoUpdateView(LoginRequiredMixin,UpdateView):
    model = Banco
    template_name = 'inventory/banco_update.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("banco_list")

class BancoDeleteView(LoginRequiredMixin,DeleteView):
    model = Banco
    template_name = 'inventory/banco_delete.html'

    def get_success_url(self):
        return reverse_lazy("banco_list")
# CUENTA
class CuentaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Cuenta
    table_class = CuentaTable
    paginate_by = 6
    search_fields = ['descripcion','banco__descripcion','nroCuenta']
    template_name = 'inventory/cuenta_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'cuenta_update'
        context['delete_url'] = 'cuenta_delete'
        return context

class CuentaCreateView(LoginRequiredMixin,CreateView):
    model = Cuenta
    template_name = 'inventory/cuenta_create.html'
    fields = ['descripcion','esBanco','banco','nroCuenta']

    def get_success_url(self):
        return reverse_lazy("cuenta_list")

class CuentaUpdateView(LoginRequiredMixin,UpdateView):
    model = Cuenta
    template_name = 'inventory/cuenta_update.html'
    fields = ['descripcion','esBanco','banco','nroCuenta']

    def get_success_url(self):
        return reverse_lazy("cuenta_list")

class CuentaDeleteView(LoginRequiredMixin,DeleteView):
    model = Cuenta
    template_name = 'inventory/cuenta_delete.html'

    def get_success_url(self):
        return reverse_lazy("cuenta_list")

# DEPOSITO
class DepositoListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Deposito
    table_class = DepositoTable
    paginate_by = 6
    search_fields = ['descripcion']
    template_name = 'inventory/deposito_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'deposito_update'
        context['delete_url'] = 'deposito_delete'
        return context

class DepositoCreateView(LoginRequiredMixin,CreateView):
    model = Deposito
    template_name = 'inventory/deposito_create.html'
    fields = ['descripcion','esPlantaAcopiadora']

    def get_success_url(self):
        return reverse_lazy("deposito_list")

class DepositoUpdateView(LoginRequiredMixin,UpdateView):
    model = Deposito
    template_name = 'inventory/deposito_update.html'
    fields = ['descripcion','esPlantaAcopiadora']

    def get_success_url(self):
        return reverse_lazy("deposito_list")

class DepositoDeleteView(LoginRequiredMixin,DeleteView):
    model = Deposito
    template_name = 'inventory/deposito_delete.html'

    def get_success_url(self):
        return reverse_lazy("deposito_list")

# CATEGORIA 
class CategoriaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Categoria
    table_class = CategoriaTable
    search_fields = ['descripcion']
    template_name = 'inventory/categoria_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'categoria_update'
        context['delete_url'] = 'categoria_delete'
        return context

class CategoriaCreateView(LoginRequiredMixin,CreateView):
    model = Categoria
    template_name = 'inventory/categoria_create.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("categoria_list")

class CategoriaUpdateView(LoginRequiredMixin,UpdateView):
    model = Categoria
    template_name = 'inventory/categoria_update.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("categoria_list")

class CategoriaDeleteView(LoginRequiredMixin,DeleteView):
    model = Categoria
    template_name = 'inventory/categoria_delete.html'

    def get_success_url(self):
        return reverse_lazy("categoria_list")

# PERSONA 
class PersonaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Persona
    table_class = PersonaTable
    search_fields = ['documento','razonSocial','localidad__descripcion']
    template_name = 'inventory/persona_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'persona_update'
        context['delete_url'] = 'persona_delete'
        return context

class PersonaCreateView(LoginRequiredMixin,CreateView):
    model = Persona
    template_name = 'inventory/persona_create.html'
    fields = ['razonSocial','documento','pais','localidad','direccion','celular','esCliente','esProveedor','esEmpleado']

    def get_success_url(self):
        return reverse_lazy("persona_list")

class PersonaUpdateView(LoginRequiredMixin,UpdateView):
    model = Persona
    template_name = 'inventory/persona_update.html'
    fields = ['razonSocial','documento','pais','localidad','direccion','celular','esCliente','esProveedor','esEmpleado']

    def get_success_url(self):
        return reverse_lazy("persona_list")

class PersonaDeleteView(LoginRequiredMixin,DeleteView):
    model = Persona
    template_name = 'inventory/persona_delete.html'

    def get_success_url(self):
        return reverse_lazy("persona_list")


#ITEM
class ItemListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Item
    table_class = ItemTable
    search_fields = ['descripcion', 'codigoBarra','marca__descripcion','"categoria__descripcion','tipo_item__descripcion','tipo_impuesto__descripcion']
    template_name = 'inventory/item_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'item_update'
        context['delete_url'] = 'item_delete'
        return context

class ItemCreateView(LoginRequiredMixin,CreateView):
    model = Item
    template_name = 'inventory/item_create.html'
    fields = ['codigoBarra','descripcion','tipoItem','tipoImpuesto','categoria','marca','precio','esActivo']

    def get_success_url(self):
        return reverse_lazy("item_list")

class ItemUpdateView(LoginRequiredMixin,UpdateView):
    model = Item
    template_name = 'inventory/item_update.html'
    fields = ['codigoBarra','descripcion','tipoImpuesto','categoria','marca','precio','esActivo']

    def get_success_url(self):
        return reverse_lazy("item_list")

class ItemDeleteView(LoginRequiredMixin,DeleteView):
    model = Item
    template_name = 'inventory/item_delete.html'

    def get_success_url(self):
        return reverse_lazy("item_list")


#ZAFRA
class ZafraListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Zafra
    table_class = ZafraTable
    search_fields = ['descripcion', 'item__descripcion']
    template_name = 'inventory/zafra_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'zafra_update'
        context['delete_url'] = 'zafra_delete'
        return context

class ZafraCreateView(LoginRequiredMixin,CreateView):
    model = Zafra
    template_name = 'inventory/zafra_create.html'
    fields = ['descripcion','item','anho','esZafrinha','kgEstimado']

    def get_success_url(self):
        return reverse_lazy("zafra_list")

class ZafraUpdateView(LoginRequiredMixin,UpdateView):
    model = Zafra
    template_name = 'inventory/zafra_update.html'
    fields = ['descripcion','item','anho','esZafrinha','kgEstimado']
    def get_success_url(self):
        return reverse_lazy("zafra_list")

class ZafraDeleteView(LoginRequiredMixin,DeleteView):
    model = Zafra
    template_name = 'inventory/zafra_delete.html'

    def get_success_url(self):
        return reverse_lazy("zafra_list")

# FINCA
class LoteListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Lote
    table_class = LoteTable
    paginate_by = 6
    search_fields = ['descripcion','zafra__descripcion','finca__descripcion']
    template_name = 'inventory/lote_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'lote_update'
        context['delete_url'] = 'lote_delete'
        return context

class LoteCreateView(LoginRequiredMixin,CreateView):
    model = Lote
    template_name = 'inventory/lote_create.html'
    fields = ['descripcion','zafra','finca','dimension']

    def get_success_url(self):
        return reverse_lazy("lote_list")

class LoteUpdateView(LoginRequiredMixin,UpdateView):
    model = Lote
    template_name = 'inventory/lote_update.html'
    fields = ['descripcion','zafra','finca','dimension']

    def get_success_url(self):
        return reverse_lazy("lote_list")

class LoteDeleteView(LoginRequiredMixin,DeleteView):
    model = Lote
    template_name = 'inventory/lote_delete.html'

    def get_success_url(self):
        return reverse_lazy("lote_list")


# MAQUINARIA AGRICOLA
class MaquinariaAgricolaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = MaquinariaAgricola
    table_class = MaquinariaAgricolaTable
    paginate_by = 6
    search_fields = ['descripcion','tipoMaquinariaAgricola__descripcion']
    template_name = 'inventory/maquinaria_agricola_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'maquinaria_agricola_update'
        context['delete_url'] = 'maquinaria_agricola_delete'
        return context

class MaquinariaAgricolaCreateView(LoginRequiredMixin,CreateView):
    model = MaquinariaAgricola
    template_name = 'inventory/maquinaria_agricola_create.html'
    fields = ['descripcion','tipoMaquinariaAgricola','esImplemento','admiteImplemento','precio']

    def get_success_url(self):
        return reverse_lazy("maquinaria_agricola_list")

class MaquinariaAgricolaUpdateView(LoginRequiredMixin,UpdateView):
    model = MaquinariaAgricola
    template_name = 'inventory/maquinaria_agricola_update.html'
    fields = ['descripcion','tipoMaquinariaAgricola','esImplemento','admiteImplemento','precio']

    def get_success_url(self):
        return reverse_lazy("maquinaria_agricola_list")

class MaquinariaAgricolaDeleteView(LoginRequiredMixin,DeleteView):
    model = MaquinariaAgricola
    template_name = 'inventory/maquinaria_agricola_delete.html'

    def get_success_url(self):
        return reverse_lazy("maquinaria_agricola_list")

# CALIFICACION AGRICOLA
class CalificacionAgricolaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = CalificacionAgricola
    table_class = CalificacionAgricolaTable
    paginate_by = 6
    search_fields = ['descripcion',]
    template_name = 'inventory/calificacion_agricola_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'calificacion_agricola_update'
        context['delete_url'] = 'calificacion_agricola_delete'
        return context

class CalificacionAgricolaCreateView(LoginRequiredMixin,CreateView):
    model = CalificacionAgricola
    template_name = 'inventory/calificacion_agricola_create.html'
    fields = ['descripcion',]

    def get_success_url(self):
        return reverse_lazy("calificacion_agricola_list")

class CalificacionAgricolaUpdateView(LoginRequiredMixin,UpdateView):
    model = CalificacionAgricola
    template_name = 'inventory/calificacion_agricola_update.html'
    fields = ['descripcion',]

    def get_success_url(self):
        return reverse_lazy("calificacion_agricola_list")

class CalificacionAgricolaDeleteView(LoginRequiredMixin,DeleteView):
    model = CalificacionAgricola
    template_name = 'inventory/calificacion_agricola_delete.html'

    def get_success_url(self):
        return reverse_lazy("calificacion_agricola_list")

#PLAN ACTIVIDAD ZAFRA
class PlanActividadZafraListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = PlanActividadZafra
    table_class = PlanActividadZafraTable
    search_fields = ['zafra__descripcion', 'observacion']
    template_name = 'inventory/plan_actividad_zafra_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'plan_actividad_zafra_update'
        return context


class PlanActividadZafraCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = PlanActividadZafra
    form_class = PlanActividadZafraForm
    template_name = 'inventory/plan_actividad_zafra_create.html'
    inlines = [PlanActividadZafraDetalleInline]

    def get_success_url(self):
        return reverse_lazy('plan_actividad_zafra_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class PlanActividadZafraUpdateView(LoginRequiredMixin,UpdateWithFormsetInlinesView):
    model = PlanActividadZafra
    form_class = PlanActividadZafraForm
    template_name = 'inventory/plan_actividad_zafra_update.html'
    inlines = [PlanActividadZafraDetalleInline]

    def get_success_url(self):
        return reverse_lazy('plan_actividad_zafra_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

#ACOPIOS
class AcopioListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Acopio
    table_class = AcopioTable
    search_fields = ['zafra__descripcion', 'comprobante','deposito__descripcion']
    template_name = 'inventory/acopio_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'acopio_update'
        context['anular_url'] = 'acopio_anular'
        return context


class AcopioCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = Acopio
    form_class = AcopioForm
    template_name = 'inventory/acopio_create.html'
    inlines = [AcopioDetalleInline,AcopioCalificacionDetalleInline]

    def get_success_url(self):
        return reverse_lazy('acopio_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def run_form_extra_validation(self, form, inlines):
        """ ejecutar validaciones adicionales de formularios """

        acopioDetalle = inlines[0]
        totalPeso = 0
        existeRegistro = False
        pesoEncabezado =  (form.cleaned_data.get('pBruto') + form.cleaned_data.get('pBonificacion')) - (form.cleaned_data.get('pTara') + form.cleaned_data.get('pDescuento'))
        for f in acopioDetalle:
            totalPeso = f.cleaned_data.get('peso')
            existeRegistro = True
                       
        if existeRegistro == False or totalPeso == 0 or totalPeso is None:
            form.add_error(None, 'Registre al menos un detalle del acopio')
        if pesoEncabezado != totalPeso:  
            form.add_error('pBruto', 'El neto (Peso Bruto + Peso Bonificacion ) - ( Peso Tara + Peso Descuento) no es igual a los detalles cargados')

class AcopioUpdateView(LoginRequiredMixin,UpdateWithFormsetInlinesView):
    model = Acopio
    form_class = AcopioForm
    template_name = 'inventory/acopio_update.html'
    inlines = [AcopioDetalleInline,AcopioCalificacionDetalleInline]

    def get_success_url(self):
        return reverse_lazy('acopio_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class AcopioAnularView(LoginRequiredMixin,DeleteView):
    model = Acopio
    template_name = 'inventory/anular.html'
    success_url = reverse_lazy("acopio_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        try:
            self.object = self.get_object()
            if self.object.esVigente == False:
                print('entro en exepcion para anulado')
                raise Exception("El Acopio ya fue anulado.")
            else:
                self.object.esVigente = False
                self.object.save()
        except  Exception as e:
            self.error = e
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = 'acopio_list'
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        context['title']="Anular Acopio"
        context['description']="Está seguro de anular el Acopio?"
        return context
    def get_success_url(self):
        return reverse_lazy("acopio_list")

#PEDIDOS DE COMPRAS
class PedidoCompraListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = PedidoCompra
    table_class = PedidoCompraTable
    search_fields = ['proveedor__razonSocial',]
    template_name = 'inventory/pedido_compra_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'pedido_compra_update'
        return context


class PedidoCompraCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = PedidoCompra
    form_class = PedidoCompraForm
    template_name = 'inventory/pedido_compra_create.html'
    inlines = [PedidoCompraDetalleInline]

    def get_success_url(self):
        return reverse_lazy('pedido_compra_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class PedidoCompraUpdateView(LoginRequiredMixin,UpdateWithFormsetInlinesView):
    model = PedidoCompra
    form_class = PedidoCompraForm
    template_name = 'inventory/pedido_compra_update.html'
    inlines = [PedidoCompraDetalleInline]

    def get_success_url(self):
        return reverse_lazy('pedido_compra_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

#ORDENES DE COMPRAS
class OrdenCompraListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = OrdenCompra
    table_class = OrdenCompraTable
    search_fields = ['proveedor__razonSocial',]
    template_name = 'inventory/orden_compra_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'orden_compra_update'
        context['anular_url'] = 'orden_compra_anular'
        return context


class OrdenCompraCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = OrdenCompra
    form_class = OrdenCompraForm
    template_name = 'inventory/orden_compra_create.html'
    inlines = [OrdenCompraDetalleInline]

    def get_success_url(self):
        return reverse_lazy('orden_compra_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class OrdenCompraUpdateView(LoginRequiredMixin,UpdateWithFormsetInlinesView):
    model = OrdenCompra
    form_class = OrdenCompraForm
    template_name = 'inventory/orden_compra_update.html'
    inlines = [OrdenCompraDetalleInline]

    def get_success_url(self):
        return reverse_lazy('orden_compra_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class OrdenCompraAnularView(LoginRequiredMixin,DeleteView):
    model = OrdenCompra
    template_name = 'inventory/anular.html'
    success_url = reverse_lazy("orden_compra_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        self.object = self.get_object()
        self.object.esVigente = False
        self.object.save()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        context['title']="Anular Orden Compra"
        context['description']="Está seguro de anular la Orden de Compra?"
        context['list_url'] = 'orden_compra_list'
        return context
    def get_success_url(self):
        return reverse_lazy("orden_compra_list")

#APERTURA CIERRE DE CAJAS
class AperturaCajaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = AperturaCaja
    table_class = AperturaCajaTable
    paginate_by = 6
    search_fields = ['empleado__razonSocial','observacion']
    template_name = 'inventory/apertura_caja_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cerrar_url'] = 'apertura_caja_cerrar'
        return context

class AperturaCajaCreateView(LoginRequiredMixin,CreateView):
    model = AperturaCaja
    template_name = 'inventory/apertura_caja_create.html'
    fields = ['empleado','observacion','montoInicio']

    def get_success_url(self):
        return reverse_lazy("apertura_caja_list")

class AperturaCajaCerrarView(LoginRequiredMixin,DeleteView):
    model = AperturaCaja
    template_name = 'inventory/cerrar.html'
    success_url = reverse_lazy("apertura_caja_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        self.object = self.get_object()
        self.object.estaCerrado = True
        self.object.fechaHoraCierre = datetime.datetime.now()
        self.object.save()
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        context['title']="Cierre de Caja"
        context['description']="Está seguro de cerrar la Caja?"
        context['list_url'] = 'apertura_caja_list'
        return context
    def get_success_url(self):
        return reverse_lazy("apertura_caja_list")

# ARQUEO
class ArqueoListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Arqueo
    table_class = ArqueoTable
    paginate_by = 6
    search_fields = ['empleado__razonSocial','observacion']
    template_name = 'inventory/arqueo_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_url'] = 'arqueo_delete'
        return context

class ArqueoCreateView(LoginRequiredMixin,CreateView):
    model = Arqueo
    template_name = 'inventory/arqueo_create.html'
    fields = ['empleado','aperturaCaja','observacion','monto']

    def get_success_url(self):
        return reverse_lazy("arqueo_list")

class ArqueoDeleteView(LoginRequiredMixin,DeleteView):
    model = Arqueo
    template_name = 'inventory/arqueo_delete.html'

    def get_success_url(self):
        return reverse_lazy("arqueo_list")


#COMPRAS
class CompraListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Compra
    table_class = CompraTable
    search_fields = ['proveedor__razonSocial','comprobante','timbrado','observacion']
    template_name = 'inventory/compra_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anular_url'] = 'compra_anular'
        return context


class CompraCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = Compra
    form_class = CompraForm
    template_name = 'inventory/compra_create.html'
    inlines = [CompraDetalleInline,CuotaCompraInline]

    def get_success_url(self):
        return reverse_lazy('compra_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class CompraAnularView(LoginRequiredMixin,DeleteView):
    model = Compra
    template_name = 'inventory/anular.html'
    success_url = reverse_lazy("compra_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        try:
            self.object = self.get_object()
            if self.object.esVigente == False:
                print('entro en exepcion para anulado')
                raise Exception("La factura ya fue anulado.")
            else:
                self.object.esVigente = False
                self.object.save()
        except  Exception as e:
            self.error = e
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return HttpResponseRedirect(success_url)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        context['title']="Anular Compra"
        context['description']="Está seguro de anular la Compra?"
        context['list_url'] = 'compra_list'
        return context
    def get_success_url(self):
        return reverse_lazy("compra_list")

# AJUSTE DE STOCK
class AjusteStockListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = AjusteStock
    table_class = AjusteStockTable
    paginate_by = 6
    search_fields = ['comprobante','empleado__razonSocial','deposito__descripcion']
    template_name = 'inventory/ajuste_stock_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'ajuste_stock_update'
        context['delete_url'] = 'ajuste_stock_delete'
        return context

class AjusteStockCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = AjusteStock
    form_class = AjusteStockForm
    template_name = 'inventory/ajuste_stock_create.html'
    inlines = [AjusteStockDetalleInline]
    def get_success_url(self):
        return reverse_lazy('ajuste_stock_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class AjusteStockUpdateView(LoginRequiredMixin,UpdateWithFormsetInlinesView):
    model = AjusteStock
    form_class = AjusteStockForm
    template_name = 'inventory/ajuste_stock_update.html'
    inlines = [AjusteStockDetalleInline]
    def get_success_url(self):
        return reverse_lazy('ajuste_stock_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class AjusteStockDeleteView(DeleteView):
    model = CalificacionAgricola
    template_name = 'inventory/ajuste_stock_delete.html'

    def get_success_url(self):
        return reverse_lazy("ajuste_stock_list")


#ACTIVIDAD AGRICOLA
class ActividadAgricolaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = ActividadAgricola
    table_class = ActividadAgricolaTable
    search_fields = ['zafra__descripcion','finca__descripcion','lote__descripcion', 'empleado__razonSocial','deposito__descripcion']
    template_name = 'inventory/actividad_agricola_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anular_url'] = 'actividad_agricola_anular'
        return context


class ActividadAgricolaCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = ActividadAgricola
    form_class = ActividadAgricolaForm
    template_name = 'inventory/actividad_agricola_create.html'
    inlines = [ActividadAgricolaMaquinariaDetalleInline,ActividadAgricolaItemDetalleInline]

    def get_success_url(self):
        return reverse_lazy('actividad_agricola_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class ActividadAgricolaAnularView(LoginRequiredMixin,DeleteView):
    model = ActividadAgricola
    template_name = 'inventory/anular.html'
    success_url = reverse_lazy("actividad_agricola_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        try:
            self.object = self.get_object()
            if self.object.esVigente == False:
                print('entro en exepcion para anulado')
                raise Exception("La Actividad Agrícola ya fue anulado.")
            else:
                self.object.esVigente = False
                self.object.save()
        except  Exception as e:
            self.error = e
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return HttpResponseRedirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_url'] = 'actividad_agricola_list'
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        context['title']="Anular Actividad Agrícola"
        context['description']="Está seguro de anular la Actividad Agrícola?"
        return context
    def get_success_url(self):
        return reverse_lazy("actividad_agricola_list")

# CONTRATO 
class ContratoListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Contrato
    table_class = ContratoTable
    paginate_by = 6
    search_fields = ['descripcion','persona__razonSocial','zafra__descripcion']
    template_name = 'inventory/contrato_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_url'] = 'contrato_delete'
        return context

class ContratoCreateView(LoginRequiredMixin,CreateView):
  
    model = Contrato
    template_name = 'inventory/contrato_create.html'
    form_class = ContratoForm
    def get_success_url(self):
        return reverse_lazy("contrato_list")

class ContratoDeleteView(LoginRequiredMixin,DeleteView):
    model = Contrato
    template_name = 'inventory/contrato_delete.html'

    def get_success_url(self):
        return reverse_lazy("contrato_list")

#VENTAS
class VentaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Venta
    table_class = VentaTable
    search_fields = ['cliente__razonSocial','comprobante','timbrado','observacion']
    template_name = 'inventory/venta_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anular_url'] = 'venta_anular'
        context['descargar_venta_url'] = 'venta_descargar'
        return context


class VentaCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = Venta
    form_class = VentaForm
    template_name = 'inventory/venta_create.html'
    inlines = [VentaDetalleInline,CuotaVentaInline]

    def get_success_url(self):
        return reverse_lazy('venta_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class VentaAnularView(LoginRequiredMixin,DeleteView):
    model = Venta
    template_name = 'inventory/anular.html'
    success_url = reverse_lazy("venta_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        try:
            self.object = self.get_object()
            if self.object.esVigente == False:
                print('entro en exepcion para anulado')
                raise Exception("La factura ya fue anulado.")
            else:
                self.object.esVigente = False
                self.object.save()
        except  Exception as e:
            self.error = e
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return HttpResponseRedirect(success_url)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        context['title']="Anular Venta"
        context['description']="Está seguro de anular la Venta?"
        context['list_url'] = 'venta_list'
        return context
    def get_success_url(self):
        return reverse_lazy("venta_list")


#@method_decorator(subscriber_required, name="dispatch")
# class FacturVentaDetailView(DetailView):
#     template_name = "venta/factura_detalle.html"
#     model = Venta

#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         context['list_url'] = 'invoice_list'
#         context['invoice_code'] = str(self.object.payment.subscriber.current_plan.id)[0:8]
#         context['number_to_words'] = str(num2words(self.object.amount, lang="es")).capitalize
#         context['invoice_img_dir'] = "/static/site/images/logo_compy"
#         context['only_detail'] = True
#         context['subscriberplan'] = self.object.payment.subscriber.subscriberplan_set.all().filter(is_active = True).first()
#         return context



def download_view(request, pk):
    """"""
    template_path = "descargar_factura_venta.html"
    object = Venta.objects.get(pk=pk)
    detalles = object.ventadetalle_set.all()

    context = {
        'object':object,
        'number_to_words': str(num2words(object.total, lang="es")).capitalize,
        'invoice_css_dir': settings.INVOICE_CSS_DIR,
        'invoice_img_dir': settings.INVOICE_IMG_DIR,
        'detalles': detalles
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf') 
    response['Content-Disposition'] = f'attachment; filename="{object.pk}.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view

    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


#NOTAS CREDITOS RECIBIDAS
class NotaCreditoRecibidaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = NotaCreditoRecibida
    table_class = NotaCreditoRecibidaTable
    search_fields = ['proveedor__razonSocial','comprobante','timbrado','compra__comprobante']
    template_name = 'inventory/nota_credito_recibida_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anular_url'] = 'nota_credito_recibida_anular'
        return context


class NotaCreditoRecibidaCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = NotaCreditoRecibida
    form_class = NotaCreditoRecibidaForm
    template_name = 'inventory/nota_credito_recibida_create.html'
    inlines = [NotaCreditoRecibidaDetalleInline]

    def get_success_url(self):
        return reverse_lazy('nota_credito_recibida_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class NotaCreditoRecibidaAnularView(LoginRequiredMixin,DeleteView):
    model = NotaCreditoRecibida
    template_name = 'inventory/anular.html'
    success_url = reverse_lazy("nota_credito_recibida_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        try:
            self.object = self.get_object()
            if self.object.esVigente == False:
                print('entro en exepcion para anulado')
                raise Exception("La Nota de Crédito ya fue anulado.")
            else:
                self.object.esVigente = False
                self.object.save()
        except  Exception as e:
            self.error = e
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return HttpResponseRedirect(success_url)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        context['title']="Anular Nota de Crédito Recibida"
        context['description']="Está seguro de anular la Nota de Crédito?"
        context['list_url'] = 'nota_credito_recibida_list'
        return context
    def get_success_url(self):
        return reverse_lazy("nota_credito_recibida_list")



#NOTAS CREDITOS EMITIDAS
class NotaCreditoEmitidaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = NotaCreditoEmitida
    table_class = NotaCreditoEmitidaTable
    search_fields = ['cliente__razonSocial','comprobante','timbrado','venta__comprobante']
    template_name = 'inventory/nota_credito_emitida_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anular_url'] = 'nota_credito_emitida_anular'
        return context


class NotaCreditoEmitidaCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = NotaCreditoEmitida
    form_class = NotaCreditoEmitidaForm
    template_name = 'inventory/nota_credito_emitida_create.html'
    inlines = [NotaCreditoEmitidaDetalleInline]

    def get_success_url(self):
        return reverse_lazy('nota_credito_emitida_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class NotaCreditoEmitidaAnularView(LoginRequiredMixin,DeleteView):
    model = NotaCreditoEmitida
    template_name = 'inventory/anular.html'
    success_url = reverse_lazy("nota_credito_emitida_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        try:
            self.object = self.get_object()
            if self.object.esVigente == False:
                print('entro en exepcion para anulado')
                raise Exception("La Nota de Crédito ya fue anulado.")
            else:
                self.object.esVigente = False
                self.object.save()
        except  Exception as e:
            self.error = e
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return HttpResponseRedirect(success_url)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        context['title']="Anular Nota de Crédito Emitida"
        context['description']="Está seguro de anular la Nota de Crédito?"
        context['list_url'] = 'nota_credito_emitida_list'
        return context
    def get_success_url(self):
        return reverse_lazy("nota_credito_emitida_list")



#TRANSFERENCIA ENTRE CUENTAS
class TransferenciaCuentaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = TransferenciaCuenta
    table_class = TransferenciaCuentaTable
    search_fields = ['cuentaSalida__descripcion','cuentaEntrada__descripcion','comprobante']
    template_name = 'inventory/transferencia_cuenta_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anular_url'] = 'transferencia_cuenta_anular'
        return context


class TransferenciaCuentaCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = TransferenciaCuenta
    form_class = TransferenciaCuentaForm
    template_name = 'inventory/transferencia_cuenta_create.html'
    def get_success_url(self):
        return reverse_lazy('transferencia_cuenta_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class TransferenciaCuentaAnularView(LoginRequiredMixin,DeleteView):
    model = TransferenciaCuenta
    template_name = 'inventory/anular.html'
    success_url = reverse_lazy("transferencia_cuenta_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        try:
            self.object = self.get_object()
            if self.object.esVigente == False:
                print('entro en exepcion para anulado')
                raise Exception("La Transferencia ya fue anulado.")
            else:
                self.object.esVigente = False
                self.object.save()
        except  Exception as e:
            self.error = e
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return HttpResponseRedirect(success_url)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        context['title']="Anular Transferencia entre cuentas"
        context['description']="Está seguro de anular la Transferencia?"
        context['list_url'] = 'transferencia_cuenta_list'
        return context
    def get_success_url(self):
        return reverse_lazy("transferencia_cuenta_list")

# LIBRO DE COMPRA
class LibroCompraListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin,FilterView):
    model = Compra
    filterset_class = LibroCompraFilter
    table_class = LibroCompraTable
    paginate_by = 10
    search_fields = ['comprobante','proveedor__razonSocial','deposito__descripcion'] #context?
    template_name = 'inventory/libro_compra_list.html'
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_defecto'] = 'libro_compra_list'
        return context

# LIBRO DE VENTA
class LibroVentaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, FilterView):
    model = Venta
    filterset_class = LibroVentaFilter
    table_class = LibroVentaTable
    paginate_by = 10
    search_fields = ['comprobante','cliente__razonSocial','deposito__descripcion'] #context?
    template_name = 'inventory/libro_venta_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_defecto'] = 'libro_venta_list'
        return context

# COMPRA INFORE
class CompraInformeListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, FilterView):
    model = Compra
    filterset_class = CompraInformeFilter
    table_class = CompraInformeTable
    paginate_by = 10
    search_fields = ['comprobante','proveedor__razonSocial','deposito__descripcion'] #context?
    template_name = 'inventory/compra_informe_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_defecto'] = 'compra_informe_list'
        return context

# INFORME VENTA
class VentaInformeListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, FilterView):
    model = Venta
    filterset_class = VentaInformeFilter
    table_class = VentaInformeTable
    paginate_by = 10
    search_fields = ['comprobante','cliente__razonSocial','deposito__descripcion'] #context?
    template_name = 'inventory/venta_informe_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_defecto'] = 'venta_informe_list'
        return context

# PRODUCCION AGRICOLA
class ProduccionAgricolaInformeListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, FilterView):
    model = ActividadAgricola
    filterset_class = ProduccionAgricolaInformeFilter
    table_class = ProduccionAgricolaInformeTable
    paginate_by = 10
    search_fields = ['tipoActividadAgricola__descripcion','zafra__descripcion','finca__descripcion'] #context?
    template_name = 'inventory/produccion_agricola_informe_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_defecto'] = 'produccion_agricola_informe_list'
        return context

# INVENTARIO DEPOSITO
class InventarioDepositoInformeListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, FilterView):
    model = ItemMovimiento
    filterset_class = InventarioDepositoInformeFilter
    table_class = InventarioDepositoInformeTable
    paginate_by = 10
    search_fields = ['item__descripcion'] #context?
    template_name = 'inventory/inventario_deposito_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list_defecto'] = 'inventario_deposito_list'
        return context

class UserListView(LoginRequiredMixin, SearchViewMixin, SingleTableMixin, ListView):
    model = User
    table_class = UserTable
    search_fields = ['username', 'first_name']
    template_name = 'registration/user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'user_update'
        return context

class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'registration/user_create.html'

    def get_success_url(self):
        return reverse_lazy('user_list')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'registration/user_update.html'

    def get_success_url(self):
        return reverse_lazy("user_list")


#COBROS
class CobroListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = Cobro
    table_class = CobroTable
    search_fields = ['cliente__razonSocial','comprobante','cobrador__razonSocial']
    template_name = 'inventory/cobro_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anular_url'] = 'cobro_anular'
        return context

class CobroCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = Cobro
    form_class = CobroForm
    template_name = 'inventory/cobro_create.html'
    inlines = [CobroDetalleInline,CobroMedioInline]

    def get_success_url(self):
        return reverse_lazy('cobro_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
        
    def run_form_extra_validation(self, form, inlines):
        """ ejecutar validaciones adicionales de formularios """

        cobrodetalleinline = inlines[0]
        mediocobrodetalleinline = inlines[1]

        existeUnSeleccionado = False
        totalCuota = 0
        for f in cobrodetalleinline:
            if f.cleaned_data.get('check'):
                totalCuota = f.cleaned_data.get('cancelacion')
                existeUnSeleccionado = True
                
        totalMedioCobro = 0
        for f in mediocobrodetalleinline:
            totalMedioCobro = f.cleaned_data.get('monto')
        montoASaldarValor = form.cleaned_data['montoASaldar']
        if existeUnSeleccionado == False:
            form.add_error(None, 'Seleccione al menos un detalle a cobrar')
        if totalCuota != montoASaldarValor:  
            form.add_error('montoASaldar', 'El Monto A Saldar difiere de la suma de las cancelaciones de las cuotas')
        if totalMedioCobro != montoASaldarValor:    
            form.add_error('montoASaldar', 'El Monto A Saldar difiere de la suma de los medios de cobros')

    def get_inlines(self):
        initial = [ {'cuotaVenta': x,'check': False, 'comprobante': x.venta.comprobante, 'monto': x.monto, 'saldo': x.saldo, 'cancelacion': 0} for x in CuotaVenta.objects.filter(venta__esVigente = True).exclude(saldo = 0) ]
        cobrodetalleinline = self.inlines[0]
        cobrodetalleinline.initial = initial
        cobrodetalleinline.factory_kwargs['extra'] = len(initial)
        cobrodetalleinline.factory_kwargs['can_delete'] = False
        return self.inlines
    

class CobroAnularView(LoginRequiredMixin,DeleteView):
    model = Cobro
    template_name = 'inventory/anular.html'
    success_url = reverse_lazy("cobro_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        try:
            self.object = self.get_object()
            if self.object.esVigente == False:
                print('entro en exepcion para anulado')
                raise Exception("El cobro ya fue anulado.")
            else:
                self.object.esVigente = False
                self.object.save()
        except  Exception as e:
            self.error = e
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return HttpResponseRedirect(success_url)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        context['title']="Anular Cobro"
        context['description']="Está seguro de anular el cobro?"
        context['list_url'] = 'cobro_list'
        return context
    def get_success_url(self):
        return reverse_lazy("cobro_list")


#LIQUIDACION AGRICOLA
class LiquidacionAgricolaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = LiquidacionAgricola
    table_class = LiquidacionAgricolaTable
    search_fields = ['proveedor__razonSocial','zafra__descripcion','tipo']
    template_name = 'inventory/liquidacion_agricola_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anular_url'] = 'liquidacion_agricola_anular'
        return context

class LiquidacionAgricolaCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = LiquidacionAgricola
    form_class = LiquidacionAgricolaForm
    template_name = 'inventory/liquidacion_agricola_create.html'
    inlines = [LiquidacionAgricolaDetalleInline]

    def get_success_url(self):
        return reverse_lazy('liquidacion_agricola_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class LiquidacionAgricolaAnularView(LoginRequiredMixin,DeleteView):
    model = LiquidacionAgricola
    template_name = 'inventory/anular.html'
    success_url = reverse_lazy("liquidacion_agricola_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        try:
            self.object = self.get_object()
            if self.object.esVigente == False:
                print('entro en exepcion para anulado')
                raise Exception("La liquidación ya fue anulado.")
            else:
                self.object.esVigente = False
                self.object.save()
        except  Exception as e:
            self.error = e
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return HttpResponseRedirect(success_url)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        context['title']="Anular Liquidación Agrícola"
        context['description']="Está seguro de anular la Liquidación?"
        context['list_url'] = 'liquidacion_agricola_list'
        return context
    def get_success_url(self):
        return reverse_lazy("liquidacion_agricola_list")


#NOTAS DEBITO RECIBIDAS
class NotaDebitoRecibidaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = NotaDebitoRecibida
    table_class = NotaDebitoRecibidaTable
    search_fields = ['proveedor__razonSocial','comprobante','timbrado','compra__comprobante']
    template_name = 'inventory/nota_debito_recibida_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anular_url'] = 'nota_debito_recibida_anular'
        return context


class NotaDebitoRecibidaCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = NotaDebitoRecibida
    form_class = NotaDebitoRecibidaForm
    template_name = 'inventory/nota_debito_recibida_create.html'
    inlines = [NotaDebitoRecibidaDetalleInline]

    def get_success_url(self):
        return reverse_lazy('nota_debito_recibida_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class NotaDebitoRecibidaAnularView(LoginRequiredMixin,DeleteView):
    model = NotaDebitoRecibida
    template_name = 'inventory/anular.html'
    success_url = reverse_lazy("nota_debito_recibida_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        try:
            self.object = self.get_object()
            if self.object.esVigente == False:
                print('entro en exepcion para anulado')
                raise Exception("La Nota de Débito ya fue anulado.")
            else:
                self.object.esVigente = False
                self.object.save()
        except  Exception as e:
            self.error = e
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return HttpResponseRedirect(success_url)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        context['title']="Anular Nota de Débito Recibida"
        context['description']="Está seguro de anular la Nota de Débito?"
        context['list_url'] = 'nota_debito_recibida_list'
        return context
    def get_success_url(self):
        return reverse_lazy("nota_debito_recibida_list")


#NOTAS DEBITO EMITIDAS
class NotaDebitoEmitidaListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = NotaDebitoEmitida
    table_class = NotaDebitoEmitidaTable
    search_fields = ['cliente__razonSocial','comprobante','timbrado','venta__comprobante']
    template_name = 'inventory/nota_debito_emitida_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anular_url'] = 'nota_debito_emitida_anular'
        return context


class NotaDebitoEmitidaCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = NotaDebitoEmitida
    form_class = NotaDebitoEmitidaForm
    template_name = 'inventory/nota_debito_emitida_create.html'
    inlines = [NotaDebitoEmitidaDetalleInline]

    def get_success_url(self):
        return reverse_lazy('nota_debito_emitida_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class NotaDebitoEmitidaAnularView(LoginRequiredMixin,DeleteView):
    model = NotaDebitoEmitida
    template_name = 'inventory/anular.html'
    success_url = reverse_lazy("nota_debito_emitida_list")

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        success_url = self.get_success_url()
        try:
            self.object = self.get_object()
            if self.object.esVigente == False:
                print('entro en exepcion para anulado')
                raise Exception("La Nota de Débito ya fue anulado.")
            else:
                self.object.esVigente = False
                self.object.save()
        except  Exception as e:
            self.error = e
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        return HttpResponseRedirect(success_url)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        deletable_objects, model_count, protected = get_deleted_objects([self.object])
        context['deletable_objects']=deletable_objects
        context['model_count']=dict(model_count).items()
        context['protected']=protected
        context['title']="Anular Nota de Débito Emitida"
        context['description']="Está seguro de anular la Nota de Débito?"
        context['list_url'] = 'nota_debito_emitida_list'
        return context
    def get_success_url(self):
        return reverse_lazy("nota_debito_emitida_list")

# CIERRE ZAFRA
class CierreZafraListView(LoginRequiredMixin,SearchViewMixin, SingleTableMixin, ListView):
    model = CierreZafra
    table_class = CierreZafraTable
    paginate_by = 6
    search_fields = ['zafra__descripcion',]
    template_name = 'inventory/cierre_zafra_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delete_url'] = 'cierre_zafra_delete'
        return context

class CierreZafraCreateView(LoginRequiredMixin,CreateWithFormsetInlinesView):
    model = CierreZafra
    form_class = CierreZafraForm
    template_name = 'inventory/cierre_zafra_create.html'
    inlines = [CierreZafraDetalleInline]

    def get_success_url(self):
        return reverse_lazy('cierre_zafra_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class CierreZafraDeleteView(LoginRequiredMixin,DeleteView):
    model = CierreZafra
    template_name = 'inventory/cierre_zafra_delete.html'

    def get_success_url(self):
        return reverse_lazy("cierre_zafra_list")