import django_tables2 as tables

from inventory.models import (Acopio, AperturaCaja, Arqueo, Banco, CalificacionAgricola, Categoria, Compra,
                              Cuenta, Deposito, Finca, Item, Marca, OrdenCompra,
                              PedidoCompra, Persona, PlanActividadZafra,
                              TipoActividadAgricola, TipoImpuesto,
                              TipoMaquinariaAgricola, Zafra)


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

class AnulableTable(BaseTable):
    def __init__(self, *args, **kwargs):
        kwargs['empty_text']  =  "Sin resultados."
        kwargs['extra_columns'] = [('anular', tables.TemplateColumn(template_name="includes/anular_button.html", verbose_name="Anular", orderable=False))]
        super().__init__(*args, **kwargs)

class CerrarAperturaCajaTable(BaseTable):
    def __init__(self, *args, **kwargs):
        kwargs['empty_text']  =  "Sin resultados."
        kwargs['extra_columns'] = [('cerrar', tables.TemplateColumn(template_name="includes/cerrar_button.html", verbose_name="Cerrar", orderable=False))]
        super().__init__(*args, **kwargs)

class EditableDeleteTable(BaseTable):
    def __init__(self, *args, **kwargs):
        kwargs['empty_text']  =  "Sin resultados."
        kwargs['extra_columns'] = [('editar', tables.TemplateColumn(template_name="includes/edit_button.html", verbose_name="Editar", orderable=False)),
                                   ('eliminar', tables.TemplateColumn(template_name="includes/delete_button.html", verbose_name="Eliminar", orderable=False))]
        super().__init__(*args, **kwargs)

class DeleteTable(BaseTable):
    def __init__(self, *args, **kwargs):
        kwargs['empty_text']  =  "Sin resultados."
        kwargs['extra_columns'] = [('eliminar', tables.TemplateColumn(template_name="includes/delete_button.html", verbose_name="Eliminar", orderable=False))]
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

class MaquinariaAgricolaTable(EditableDeleteTable):
    class Meta:
        model = Zafra
        fields = ("descripcion","tipoMaquinariaAgricola", "esImplemento","admiteImplemento","precio")

class BancoTable(EditableDeleteTable):
    class Meta:
        model = Zafra
        fields = ("descripcion",)

class DepositoTable(EditableDeleteTable):
    class Meta:
        model = Deposito
        fields = ("descripcion","esPlantaAcopiadora")

class CalificacionAgricolaTable(EditableDeleteTable):
    class Meta:
        model = CalificacionAgricola
        fields = ("descripcion",)

class CuentaTable(EditableDeleteTable):
    class Meta:
        model = Cuenta
        fields = ("descripcion","nroCuenta","banco")

class PersonaTable(EditableDeleteTable):
    class Meta:
        model = Persona
        fields = ("documento","razonSocial","localidad","esCliente","esProveedor","esEmpleado")

class PlanActividadZafraTable(EditableTable):
    class Meta:
        model = PlanActividadZafra
        fields = ("fecha","zafra","observacion","total")

class AcopioTable(AnulableTable):
    class Meta:
        model = Acopio
        fields = ("fecha","comprobante","zafra","deposito","pBruto","pTara","pDescuento","esVigente")

class AcopioCalificacionTable(EditableTable):
    class Meta:
        model = Acopio
        fields = ("acopio","calificaionAgricola","grado","porcentaje","peso",)

class PedidoCompraTable(EditableTable):
    class Meta:
        model = PedidoCompra
        fields = ("proveedor","fechaDocumento","fechaVencimiento","esVigente",)

class OrdenCompraTable(AnulableTable):
    class Meta:
        model = OrdenCompra
        fields = ("proveedor","fechaDocumento","total","esVigente")

class AperturaCajaTable(CerrarAperturaCajaTable):
    class Meta:
        model = AperturaCaja
        fields = ("empleado","fechaHoraApertura","fechaHoraCiere","montoInicio","estaCerrado")

class ArqueoTable(DeleteTable):
    class Meta:
        model = Arqueo
        fields = ("empleado","aperturaCaja","observacion","fechaHoraRegistro","monto")

class CompraTable(AnulableTable):
    class Meta:
        model = Compra
        fields = ("fechaDocumento","comprobante","proveedor","total","esVigente",)