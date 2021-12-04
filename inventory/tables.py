import django_tables2 as tables
from inventory.models import Item, Marca, Categoria, TipoActividadAgricola, Finca, TipoMaquinariaAgricola, TipoImpuesto, Zafra

class BaseTable(tables.Table):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_name = "django_tables2/bootstrap4.html"


class SingleTable(BaseTable):
    def __init__(self, *args, **kwargs):
        kwargs['empty_text']  =  "Sin resultados." 
        super().__init__(*args, **kwargs) 

class EditableTable(BaseTable):
    def __init__(self, *args, **kwargs):
        kwargs['empty_text']  =  "Sin resultados."
        kwargs['extra_columns'] = [('editar', tables.TemplateColumn(template_name="includes/edit_button.html", verbose_name="Editar", orderable=False))]
        super().__init__(*args, **kwargs)

class EditableDeleteTable(BaseTable):
    def __init__(self, *args, **kwargs):
        kwargs['empty_text']  =  "Sin resultados."
        kwargs['extra_columns'] = [('editar', tables.TemplateColumn(template_name="includes/edit_button.html", verbose_name="Editar", orderable=False)),
                                   ('eliminar', tables.TemplateColumn(template_name="includes/delete_button.html", verbose_name="Eliminar", orderable=False))]
        super().__init__(*args, **kwargs)
        


## definiciones

class TipoActividadAgricolaTable(EditableDeleteTable):
    class Meta:
        model = TipoActividadAgricola
        fields = ("descripcion","esCosecha","esSiembra","esResiembra")

class FincaTable(EditableDeleteTable):
    class Meta:
        model = Finca
        fields = ("descripcion","dimensionHa","ubicacion")

class TipoMaquinariaAgricolaTable(EditableDeleteTable):
    class Meta:
        model = TipoMaquinariaAgricola
        fields = ("descripcion",)

class MarcaTable(EditableDeleteTable):
    class Meta:
        model = Marca
        fields = ("descripcion",)

class CategoriaTable(EditableDeleteTable):
    class Meta:
        model = Categoria
        fields = ("descripcion",)

class TipoImpuestoTable(EditableDeleteTable):
    class Meta:
        model = TipoImpuesto
        fields = ("descripcion", "porcentaje", "esIva")

class ItemTable(EditableDeleteTable):
    class Meta:
        model = Item
        fields = ("codigoBarra","descripcion","tipoImpuesto", "marca","categoria","precio", "esActivo")

class ZafraTable(EditableDeleteTable):
    class Meta:
        model = Zafra
        fields = ("descripcion","item", "esZafrinha","anho","estaCerrado")

class LoteTable(EditableDeleteTable):
    class Meta:
        model = Zafra
        fields = ("descripcion","zafra", "finca")


