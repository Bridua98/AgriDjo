from django.core.exceptions import ValidationError
from django.db import transaction
from django.forms.formsets import all_valid
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_tables2 import SingleTableMixin
from extra_views import CreateWithInlinesView, UpdateWithInlinesView

from inventory.forms import AcopioForm, OrdenCompraForm, PedidoCompraForm, PlanActividadZafraForm
from inventory.inlines import AcopioDetalleInline, OrdenCompraDetalleInline, PedidoCompraDetalleInline, PlanActividadZafraDetalleInline
from inventory.mixins import FormsetInlinesMetaMixin, SearchViewMixin
from inventory.models import (Acopio, Banco, CalificacionAgricola, Categoria, Cuenta, Deposito, Finca, Item,
                              Lote, MaquinariaAgricola, Marca, OrdenCompra, PedidoCompra, Persona,
                              PlanActividadZafra, TipoActividadAgricola,
                              TipoImpuesto, TipoMaquinariaAgricola, Zafra)
from inventory.tables import (AcopioTable, BancoTable, CalificacionAgricolaTable, CategoriaTable, CuentaTable,
                              DepositoTable, FincaTable, ItemTable, LoteTable,
                              MaquinariaAgricolaTable, MarcaTable, OrdenCompraTable, PedidoCompraTable,
                              PersonaTable, PlanActividadZafraTable,
                              TipoActividadAgricolaTable, TipoImpuestoTable,
                              TipoMaquinariaAgricolaTable, ZafraTable)


def main(request):
    return render(request, template_name='home.html', context={})


def menu(request):
    return render(request, template_name="menu_dummy.html", context={})



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
class TipoActividadAgricolaListView(SearchViewMixin, SingleTableMixin, ListView):
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

class TipoActividadAgricolaCreateView(CreateView):
    model = TipoActividadAgricola
    template_name = 'inventory/tipo_actividad_agricola_create.html'
    fields = ['descripcion','esCosecha','esSiembra','esResiembra']

    def get_success_url(self):
        return reverse_lazy("tipo_actividad_agricola_list")

class TipoActividadAgricolaUpdateView(UpdateView):
    model = TipoActividadAgricola
    template_name = 'inventory/tipo_actividad_agricola_update.html'
    fields = ['descripcion','esCosecha','esSiembra','esResiembra']

    def get_success_url(self):
        return reverse_lazy("tipo_actividad_agricola_list")

class TipoActividadAgricolaDeleteView(DeleteView):
    model = TipoActividadAgricola
    template_name = 'inventory/tipo_actividad_agricola_delete.html'

    def get_success_url(self):
        return reverse_lazy("tipo_actividad_agricola_list")


# FINCA
class FincaListView(SearchViewMixin, SingleTableMixin, ListView):
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

class FincaCreateView(CreateView):
    model = Finca
    template_name = 'inventory/finca_create.html'
    fields = ['descripcion','dimensionHa','ubicacion']

    def get_success_url(self):
        return reverse_lazy("finca_list")

class FincaUpdateView(UpdateView):
    model = Finca
    template_name = 'inventory/finca_update.html'
    fields = ['descripcion','dimensionHa','ubicacion']

    def get_success_url(self):
        return reverse_lazy("finca_list")

class FincaDeleteView(DeleteView):
    model = Finca
    template_name = 'inventory/finca_delete.html'

    def get_success_url(self):
        return reverse_lazy("finca_list")


# TIPO IMPUESTO
class TipoImpuestoListView(SearchViewMixin, SingleTableMixin, ListView):
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

class TipoImpuestoCreateView(CreateView):
    model = TipoImpuesto
    template_name = 'inventory/tipo_impuesto_create.html'
    fields = ['descripcion','porcentaje','esIva']

    def get_success_url(self):
        return reverse_lazy("tipo_impuesto_list")

class TipoImpuestoUpdateView(UpdateView):
    model = TipoImpuesto
    template_name = 'inventory/tipo_impuesto_update.html'
    fields = ['descripcion','porcentaje','esIva']

    def get_success_url(self):
        return reverse_lazy("tipo_impuesto_list")

class TipoImpuestoDeleteView(DeleteView):
    model = TipoImpuesto
    template_name = 'inventory/tipo_impuesto_delete.html'

    def get_success_url(self):
        return reverse_lazy("tipo_impuesto_list")

# TIPO MAQUINARIA AGRICOLA

class TipoMaquinariaAgricolaListView(SearchViewMixin, SingleTableMixin, ListView):
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

class TipoMaquinariaAgricolaCreateView(CreateView):
    model = TipoMaquinariaAgricola
    template_name = 'inventory/tipo_maquinaria_agricola_create.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("tipo_maquinaria_agricola_list")

class TipoMaquinariaAgricolaUpdateView(UpdateView):
    model = TipoMaquinariaAgricola
    template_name = 'inventory/tipo_maquinaria_agricola_update.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("tipo_maquinaria_agricola_list")

class TipoMaquinariaAgricolaDeleteView(DeleteView):
    model = TipoMaquinariaAgricola
    template_name = 'inventory/tipo_maquinaria_agricola_delete.html'

    def get_success_url(self):
        return reverse_lazy("tipo_maquinaria_agricola_list")


# MARCA
class MarcaListView(SearchViewMixin, SingleTableMixin, ListView):
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

class MarcaCreateView(CreateView):
    model = Marca
    template_name = 'inventory/marca_create.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("marca_list")

class MarcaUpdateView(UpdateView):
    model = Marca
    template_name = 'inventory/marca_update.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("marca_list")

class MarcaDeleteView(DeleteView):
    model = Marca
    template_name = 'inventory/marca_delete.html'

    def get_success_url(self):
        return reverse_lazy("marca_list")


# BANCO
class BancoListView(SearchViewMixin, SingleTableMixin, ListView):
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

class BancoCreateView(CreateView):
    model = Banco
    template_name = 'inventory/banco_create.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("banco_list")

class BancoUpdateView(UpdateView):
    model = Banco
    template_name = 'inventory/banco_update.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("banco_list")

class BancoDeleteView(DeleteView):
    model = Banco
    template_name = 'inventory/banco_delete.html'

    def get_success_url(self):
        return reverse_lazy("banco_list")
# CUENTA
class CuentaListView(SearchViewMixin, SingleTableMixin, ListView):
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

class CuentaCreateView(CreateView):
    model = Cuenta
    template_name = 'inventory/cuenta_create.html'
    fields = ['descripcion','esBanco','banco','nroCuenta']

    def get_success_url(self):
        return reverse_lazy("cuenta_list")

class CuentaUpdateView(UpdateView):
    model = Cuenta
    template_name = 'inventory/cuenta_update.html'
    fields = ['descripcion','esBanco','banco','nroCuenta']

    def get_success_url(self):
        return reverse_lazy("cuenta_list")

class CuentaDeleteView(DeleteView):
    model = Cuenta
    template_name = 'inventory/cuenta_delete.html'

    def get_success_url(self):
        return reverse_lazy("cuenta_list")

# DEPOSITO
class DepositoListView(SearchViewMixin, SingleTableMixin, ListView):
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

class DepositoCreateView(CreateView):
    model = Deposito
    template_name = 'inventory/deposito_create.html'
    fields = ['descripcion','esPlantaAcopiadora']

    def get_success_url(self):
        return reverse_lazy("deposito_list")

class DepositoUpdateView(UpdateView):
    model = Deposito
    template_name = 'inventory/deposito_update.html'
    fields = ['descripcion','esPlantaAcopiadora']

    def get_success_url(self):
        return reverse_lazy("deposito_list")

class DepositoDeleteView(DeleteView):
    model = Deposito
    template_name = 'inventory/deposito_delete.html'

    def get_success_url(self):
        return reverse_lazy("deposito_list")

# CATEGORIA 
class CategoriaListView(SearchViewMixin, SingleTableMixin, ListView):
    model = Categoria
    table_class = CategoriaTable
    search_fields = ['descripcion']
    template_name = 'inventory/categoria_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'categoria_update'
        context['delete_url'] = 'categoria_delete'
        return context

class CategoriaCreateView(CreateView):
    model = Categoria
    template_name = 'inventory/categoria_create.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("categoria_list")

class CategoriaUpdateView(UpdateView):
    model = Categoria
    template_name = 'inventory/categoria_update.html'
    fields = ['descripcion']

    def get_success_url(self):
        return reverse_lazy("categoria_list")

class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'inventory/categoria_delete.html'

    def get_success_url(self):
        return reverse_lazy("categoria_list")

# PERSONA 
class PersonaListView(SearchViewMixin, SingleTableMixin, ListView):
    model = Persona
    table_class = PersonaTable
    search_fields = ['documento','razonSocial','localidad__descripcion']
    template_name = 'inventory/persona_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'persona_update'
        context['delete_url'] = 'persona_delete'
        return context

class PersonaCreateView(CreateView):
    model = Persona
    template_name = 'inventory/persona_create.html'
    fields = ['razonSocial','documento','pais','localidad','direccion','celular','esCliente','esProveedor','esEmpleado']

    def get_success_url(self):
        return reverse_lazy("persona_list")

class PersonaUpdateView(UpdateView):
    model = Persona
    template_name = 'inventory/persona_update.html'
    fields = ['razonSocial','documento','pais','localidad','direccion','celular','esCliente','esProveedor','esEmpleado']

    def get_success_url(self):
        return reverse_lazy("persona_list")

class PersonaDeleteView(DeleteView):
    model = Persona
    template_name = 'inventory/persona_delete.html'

    def get_success_url(self):
        return reverse_lazy("persona_list")


#ITEM
class ItemListView(SearchViewMixin, SingleTableMixin, ListView):
    model = Item
    table_class = ItemTable
    search_fields = ['descripcion', 'codigoBarra','marca__descripcion','"categoria__descripcion','tipo_item__descripcion','tipo_impuesto__descripcion']
    template_name = 'inventory/item_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'item_update'
        context['delete_url'] = 'item_delete'
        return context

class ItemCreateView(CreateView):
    model = Item
    template_name = 'inventory/item_create.html'
    fields = ['codigoBarra','descripcion','tipoItem','tipoImpuesto','categoria','marca','precio','esActivo']

    def get_success_url(self):
        return reverse_lazy("item_list")

class ItemUpdateView(UpdateView):
    model = Item
    template_name = 'inventory/item_update.html'
    fields = ['codigoBarra','descripcion','tipoImpuesto','categoria','marca','precio','esActivo']

    def get_success_url(self):
        return reverse_lazy("item_list")

class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'inventory/item_delete.html'

    def get_success_url(self):
        return reverse_lazy("item_list")


#ZAFRA
class ZafraListView(SearchViewMixin, SingleTableMixin, ListView):
    model = Zafra
    table_class = ZafraTable
    search_fields = ['descripcion', 'item__descripcion']
    template_name = 'inventory/zafra_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'zafra_update'
        context['delete_url'] = 'zafra_delete'
        return context

class ZafraCreateView(CreateView):
    model = Zafra
    template_name = 'inventory/zafra_create.html'
    fields = ['descripcion','item','anho','esZafrinha','kgEstimado']

    def get_success_url(self):
        return reverse_lazy("zafra_list")

class ZafraUpdateView(UpdateView):
    model = Zafra
    template_name = 'inventory/zafra_update.html'
    fields = ['descripcion','item','anho','esZafrinha','kgEstimado']
    def get_success_url(self):
        return reverse_lazy("zafra_list")

class ZafraDeleteView(DeleteView):
    model = Zafra
    template_name = 'inventory/zafra_delete.html'

    def get_success_url(self):
        return reverse_lazy("zafra_list")

# FINCA
class LoteListView(SearchViewMixin, SingleTableMixin, ListView):
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

class LoteCreateView(CreateView):
    model = Lote
    template_name = 'inventory/lote_create.html'
    fields = ['descripcion','zafra','finca','dimension']

    def get_success_url(self):
        return reverse_lazy("lote_list")

class LoteUpdateView(UpdateView):
    model = Lote
    template_name = 'inventory/lote_update.html'
    fields = ['descripcion','zafra','finca','dimension']

    def get_success_url(self):
        return reverse_lazy("lote_list")

class LoteDeleteView(DeleteView):
    model = Lote
    template_name = 'inventory/lote_delete.html'

    def get_success_url(self):
        return reverse_lazy("lote_list")


# MAQUINARIA AGRICOLA
class MaquinariaAgricolaListView(SearchViewMixin, SingleTableMixin, ListView):
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

class MaquinariaAgricolaCreateView(CreateView):
    model = MaquinariaAgricola
    template_name = 'inventory/maquinaria_agricola_create.html'
    fields = ['descripcion','tipoMaquinariaAgricola','esImplemento','admiteImplemento','precio']

    def get_success_url(self):
        return reverse_lazy("maquinaria_agricola_list")

class MaquinariaAgricolaUpdateView(UpdateView):
    model = MaquinariaAgricola
    template_name = 'inventory/maquinaria_agricola_update.html'
    fields = ['descripcion','tipoMaquinariaAgricola','esImplemento','admiteImplemento','precio']

    def get_success_url(self):
        return reverse_lazy("maquinaria_agricola_list")

class MaquinariaAgricolaDeleteView(DeleteView):
    model = MaquinariaAgricola
    template_name = 'inventory/maquinaria_agricola_delete.html'

    def get_success_url(self):
        return reverse_lazy("maquinaria_agricola_list")

# CALIFICACION AGRICOLA
class CalificacionAgricolaListView(SearchViewMixin, SingleTableMixin, ListView):
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

class CalificacionAgricolaCreateView(CreateView):
    model = CalificacionAgricola
    template_name = 'inventory/calificacion_agricola_create.html'
    fields = ['descripcion',]

    def get_success_url(self):
        return reverse_lazy("calificacion_agricola_list")

class CalificacionAgricolaUpdateView(UpdateView):
    model = CalificacionAgricola
    template_name = 'inventory/calificacion_agricola_update.html'
    fields = ['descripcion',]

    def get_success_url(self):
        return reverse_lazy("calificacion_agricola_list")

class CalificacionAgricolaDeleteView(DeleteView):
    model = CalificacionAgricola
    template_name = 'inventory/calificacion_agricola_delete.html'

    def get_success_url(self):
        return reverse_lazy("calificacion_agricola_list")

#PLAN ACTIVIDAD ZAFRA
class PlanActividadZafraListView(SearchViewMixin, SingleTableMixin, ListView):
    model = PlanActividadZafra
    table_class = PlanActividadZafraTable
    search_fields = ['zafra__descripcion', 'observacion']
    template_name = 'inventory/plan_actividad_zafra_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'plan_actividad_zafra_update'
        return context


class PlanActividadZafraCreateView(CreateWithFormsetInlinesView):
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

class PlanActividadZafraUpdateView(UpdateWithFormsetInlinesView):
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
class AcopioListView(SearchViewMixin, SingleTableMixin, ListView):
    model = Acopio
    table_class = AcopioTable
    search_fields = ['zafra__descripcion', 'comprobante','deposito__descripcion']
    template_name = 'inventory/acopio_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'acopio_update'
        return context


class AcopioCreateView(CreateWithFormsetInlinesView):
    model = Acopio
    form_class = AcopioForm
    template_name = 'inventory/acopio_create.html'
    inlines = [AcopioDetalleInline]

    def get_success_url(self):
        return reverse_lazy('acopio_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

class AcopioUpdateView(UpdateWithFormsetInlinesView):
    model = Acopio
    form_class = AcopioForm
    template_name = 'inventory/acopio_update.html'
    inlines = [AcopioDetalleInline]

    def get_success_url(self):
        return reverse_lazy('acopio_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        return form
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

#PEDIDOS DE COMPRAS
class PedidoCompraListView(SearchViewMixin, SingleTableMixin, ListView):
    model = PedidoCompra
    table_class = PedidoCompraTable
    search_fields = ['proveedor__razonSocial',]
    template_name = 'inventory/pedido_compra_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'pedido_compra_update'
        return context


class PedidoCompraCreateView(CreateWithFormsetInlinesView):
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

class PedidoCompraUpdateView(UpdateWithFormsetInlinesView):
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
class OrdenCompraListView(SearchViewMixin, SingleTableMixin, ListView):
    model = OrdenCompra
    table_class = OrdenCompraTable
    search_fields = ['proveedor__razonSocial',]
    template_name = 'inventory/orden_compra_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update_url'] = 'orden_compra_update'
        return context


class OrdenCompraCreateView(CreateWithFormsetInlinesView):
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

class OrdenCompraUpdateView(UpdateWithFormsetInlinesView):
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

class OrdenCompraAnularView(DeleteView):
    model = OrdenCompra
    template_name = 'inventory/orden_compra_anular.html'

   # def delete(self):

    def get_success_url(self):
        return reverse_lazy("orden_compra_list")
