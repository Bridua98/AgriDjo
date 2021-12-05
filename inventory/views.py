from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_tables2 import SingleTableMixin

from inventory.mixins import SearchViewMixin
from inventory.models import Banco, Categoria, Deposito, Item, Lote, MaquinariaAgricola, Marca, TipoActividadAgricola, Finca, TipoImpuesto, TipoMaquinariaAgricola, Zafra
from inventory.tables import BancoTable, CategoriaTable, DepositoTable, ItemTable, LoteTable, MaquinariaAgricolaTable, MarcaTable, TipoActividadAgricolaTable,FincaTable, TipoImpuestoTable, TipoMaquinariaAgricolaTable, ZafraTable


def main(request):
    return render(request, template_name='home.html', context={})


def menu(request):
    return render(request, template_name="menu_dummy.html", context={})

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


