import django_tables2 as tables

from inventory.models import (Acopio, ActividadAgricola, AjusteStock, AperturaCaja, Arqueo, Banco, CalificacionAgricola, Categoria, Cobro, Compra, Contrato,
                              Cuenta, Deposito, Finca, Item, ItemMovimiento, Marca, NotaCreditoEmitida, NotaCreditoRecibida, NotaDebitoRecibida, OrdenCompra,
                              PedidoCompra, Persona, PlanActividadZafra,
                              TipoActividadAgricola, TipoImpuesto,
                              TipoMaquinariaAgricola, TransferenciaCuenta, Venta, Zafra)

from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth.models import User

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

class VentaTable(BaseTable):
    def __init__(self, *args, **kwargs):
        kwargs['empty_text']  =  "Sin resultados."
        kwargs['extra_columns'] = [('anular', tables.TemplateColumn(template_name="includes/anular_button.html", verbose_name="Anular", orderable=False)),
                                   ('descargar', tables.TemplateColumn(template_name="includes/descargar_venta_button.html", verbose_name="Descargar Factura", orderable=False))]
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
    def render_precio(self,value):
        return intcomma(value)
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
    def render_precio(self,value):
        return intcomma(value)
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
    def render_total(self,value):
        return intcomma(value)
    class Meta:
        model = PlanActividadZafra
        fields = ("fecha","zafra","observacion","total")

class AcopioTable(AnulableTable):

    def render_pBruto(self,value):
        return intcomma(value)
    
    def render_pTara(self,value):
        return intcomma(value)

    def render_pDescuento(self,value):
        return intcomma(value)

    class Meta:
        model = Acopio
        fields = ("fecha","comprobante","zafra","deposito","pBruto","pTara","pDescuento","esVigente")
        row_attrs = {
        "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fecha"

class AcopioCalificacionTable(EditableTable):
    class Meta:
        model = Acopio
        fields = ("acopio","calificacionAgricola","grado","porcentaje","peso",)

class PedidoCompraTable(EditableTable):
    class Meta:
        model = PedidoCompra
        fields = ("proveedor","fechaDocumento","fechaVencimiento","esVigente",)

class OrdenCompraTable(AnulableTable):
    def render_total(self,value):
        return intcomma(value)
    class Meta:
        model = OrdenCompra
        fields = ("proveedor","fechaDocumento","total","esVigente")
        row_attrs = {
            "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fechaDocumento"

class AperturaCajaTable(CerrarAperturaCajaTable):
    def render_montoInicio(self,value):
        return intcomma(value)
    class Meta:
        model = AperturaCaja
        fields = ("empleado","fechaHoraApertura","fechaHoraCiere","montoInicio","estaCerrado")

class ArqueoTable(DeleteTable):
    def render_monto(self,value):
        return intcomma(value)
    class Meta:
        model = Arqueo
        fields = ("empleado","aperturaCaja","observacion","fechaHoraRegistro","monto")

class CompraTable(AnulableTable):
    def render_total(self,value):
        return intcomma(value)
    class Meta:
        model = Compra
        fields = ("fechaDocumento","comprobante","proveedor","total","esVigente",)
        row_attrs = {
            "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fechaDocumento"

class AjusteStockTable(EditableDeleteTable):
    class Meta:
        model = AjusteStock
        fields = ("fechaDocumento","comprobante","empleado","deposito","observacion",)

class ActividadAgricolaTable(AnulableTable):
    def render_cantidadTrabajada(self,value):
        return intcomma(value)
    def render_cantidadTrabajada(self,value):
        return intcomma(value)
    class Meta:
        model = ActividadAgricola
        fields = ("fechaDocumento","tipoActividadAgricola","zafra","finca","lote","cantidadTrabajada","esServicioContratado","esVigente")
        row_attrs = {
            "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fechaDocumento"

class ContratoTable(DeleteTable):
    def render_costoPactado(self,value):
        return intcomma(value)
    class Meta:
        model = Contrato
        fields = ("fecha","zafra","persona","costoPactado","descripcion")


class VentaTable(VentaTable):
    def render_total(self,value):
        return intcomma(value)
    class Meta:
        model = Venta
        fields = ("fechaDocumento","comprobante","cliente","total","esVigente",)
        row_attrs = {
            "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fechaDocumento"

class NotaCreditoRecibidaTable(AnulableTable):
    def render_total(self,value):
        return intcomma(value)
    class Meta:
        model = NotaCreditoRecibida
        fields = ("fechaDocumento","comprobante","proveedor","total","esVigente",)
        row_attrs = {
            "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fechaDocumento"

class NotaCreditoEmitidaTable(AnulableTable):
    def render_total(self,value):
        return intcomma(value)
    class Meta:
        model = NotaCreditoEmitida
        fields = ("fechaDocumento","comprobante","cliente","total","esVigente",)
        row_attrs = {
            "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fechaDocumento"

class TransferenciaCuentaTable(AnulableTable):
    def render_monto(self,value):
        return intcomma(value)
    class Meta:
        model = TransferenciaCuenta
        fields = ("fecha","cuentaSalida","cuentaEntrada","monto","esVigente",)
        row_attrs = {
            "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fecha"

class LibroCompraTable(BaseTable):
    def render_iva5(self,value):
        return intcomma(value)
    def render_iva10(self,value):
        return intcomma(value)
    def render_imponibleExenta(self,value):
        return intcomma(value)
    def render_imponible5(self,value):
        return intcomma(value)
    def render_imponible10(self,value):
        return intcomma(value)
    def render_total(self,value):
        return intcomma(value)
    class Meta:
        model = Compra
        fields = ("fechaDocumento","esCredito","comprobante","proveedor","iva5","iva10","imponibleExenta","imponible5","imponible10","total",)

class LibroVentaTable(BaseTable):
    def render_iva5(self,value):
        return intcomma(value)
    def render_iva10(self,value):
        return intcomma(value)
    def render_imponibleExenta(self,value):
        return intcomma(value)
    def render_imponible5(self,value):
        return intcomma(value)
    def render_imponible10(self,value):
        return intcomma(value)
    def render_total(self,value):
        return intcomma(value)
    class Meta:
        model = Venta
        fields = ("fechaDocumento","esCredito","comprobante","cliente","iva5","iva10","imponibleExenta","imponible5","imponible10","total",)

class CompraInformeTable(BaseTable):
    def render_total(self,value):
        return intcomma(value)
    class Meta:
        model = Compra
        fields = ("fechaDocumento","esCredito","comprobante","proveedor","total",)

class VentaInformeTable(BaseTable):
    def render_total(self,value):
        return intcomma(value)
    class Meta:
        model = Venta
        fields = ("fechaDocumento","esCredito","comprobante","cliente","total",)

class ProduccionAgricolaInformeTable(BaseTable):   
    def render_totalItem(self,value):
        return intcomma(value)
    
    def render_total(self,value):
        return intcomma(value)

    def render_totalMaquinaria(self,value):
        return intcomma(value)
    class Meta:
        model = ActividadAgricola
        fields = ("fechaDocumento","tipoActividadAgricola","zafra","finca","lote","totalMaquinaria","totalItem","total")


class InventarioDepositoInformeTable(BaseTable):   
    def render_cantidad(self,value):
        return intcomma(value)
    class Meta:
        model = ItemMovimiento
        fields = ("fechaDocumento","deposito","item","tipoMovimiento","cantidad")

class UserTable(EditableTable):
    class Meta:
        model = User
        fields = ("username", "first_name", "Last_name", "is_active",)

class CobroTable(AnulableTable):
    def render_montoASaldar(self,value):
        return intcomma(value)
    class Meta:
        model = Cobro
        fields = ("fechaDocumento","comprobante","cuenta","cliente",'cobrador',"montoASaldar","esVigente")
        row_attrs = {
            "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fechaDocumento"

class LiquidacionAgricolaTable(AnulableTable):
    def render_total(self,value):
        return intcomma(value)
    class Meta:
        model = Cobro
        fields = ("fechaDocumento","tipo","zafra","proveedor","esVigente")
        row_attrs = {
            "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fechaDocumento"

class NotaDebitoRecibidaTable(AnulableTable):
    def render_total(self,value):
        return intcomma(value)
    class Meta:
        model = NotaDebitoRecibida
        fields = ("fechaDocumento","comprobante","proveedor","total","esVigente",)
        row_attrs = {
            "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fechaDocumento"

class NotaDebitoEmitidaTable(AnulableTable):
    def render_total(self,value):
        return intcomma(value)
    class Meta:
        model = NotaDebitoRecibida
        fields = ("fechaDocumento","comprobante","cliente","total","esVigente",)
        row_attrs = {
            "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fechaDocumento"
