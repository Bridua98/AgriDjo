import django_tables2 as tables

from inventory.models import (Acopio, AcopioCalificacion, ActividadAgricola, AjusteStock, AperturaCaja, Arqueo, Banco, CalificacionAgricola, Categoria, CierreZafra, Cobro, Compra, Contrato,
                              Cuenta, Deposito, Finca, Item, ItemMovimiento, LiquidacionAgricola, Marca, NotaCreditoEmitida, NotaCreditoRecibida, NotaDebitoRecibida, OrdenCompra,
                              PedidoCompra, Persona, PlanActividadZafra,
                              TipoActividadAgricola, TipoImpuesto,
                              TipoMaquinariaAgricola, TransferenciaCuenta, Venta, Zafra)

from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth.models import User

from inventory.widgets import DecimalMaskInput

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


class SelectionTable(BaseTable):
    def __init__(self, *args, **kwargs):
        kwargs['empty_text']  =  "Sin resultados."
        kwargs['extra_columns'] = [('seleccionar', tables.TemplateColumn(template_name="includes/seleccionar_button.html", verbose_name="Seleccionar", orderable=False))]
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
    def render_costo(self,value):
        return intcomma(value)
    def render_ultimoCosto(self,value):
        return intcomma(value)
        
    precio = tables.Column(verbose_name= 'Precio',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    costo = tables.Column(verbose_name= 'Costo',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    ultimoCosto = tables.Column(verbose_name= 'Ult. Costo',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    class Meta:
        model = Item
        fields = ("codigoBarra","descripcion","tipoImpuesto", "marca","categoria","costo","ultimoCosto","precio", "esActivo")

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
        
    precio = tables.Column(verbose_name= 'Precio',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
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
    total = tables.Column(verbose_name= 'Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
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
    
    def render_pBonificacion(self,value):
        return intcomma(value)

    def render_total(self,value):
        return intcomma(value)
    pBruto = tables.Column(verbose_name= 'P Bruto',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    pTara = tables.Column(verbose_name= 'P Tara',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    pDescuento = tables.Column(verbose_name= 'P Desc.',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    total = tables.Column(verbose_name= 'P Neto',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )

    class Meta:
        model = Acopio
        fields = ("fecha","comprobante","zafra","deposito","pBruto","pTara","pDescuento","total","esVigente")
        row_attrs = {
        "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fecha"

class AcopioCalificacionTable(EditableTable):
    class Meta:
        model = AcopioCalificacion
        fields = ("acopio","calificacionAgricola","grado","porcentaje","peso",)

class PedidoCompraTable(EditableTable):
    class Meta:
        model = PedidoCompra
        fields = ("proveedor","fechaDocumento","fechaVencimiento","esVigente",)

class OrdenCompraTable(AnulableTable):
    def render_total(self,value):
        return intcomma(value)
    total = tables.Column(verbose_name= 'Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
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
    montoInicio = tables.Column(verbose_name= 'Monto Inicial',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    class Meta:
        model = AperturaCaja
        fields = ("empleado","fechaHoraRegistro","fechaHoraCierre","montoInicio","estaCerrado")

class ArqueoTable(DeleteTable):
    def render_monto(self,value):
        return intcomma(value)
    monto = tables.Column(verbose_name= 'Monto',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    class Meta:
        model = Arqueo
        fields = ("empleado","aperturaCaja","observacion","fechaHoraRegistro","monto")

class CompraTable(AnulableTable):
    def render_total(self,value):
        return intcomma(value)
    total = tables.Column(verbose_name= 'Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
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
    def render_total(self,value):
        return intcomma(value)
    cantidadTrabajada = tables.Column(verbose_name= 'HA Trabajada',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    total = tables.Column(verbose_name= 'Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    class Meta:
        model = ActividadAgricola
        fields = ("fechaDocumento","tipoActividadAgricola","zafra","finca","lote","cantidadTrabajada","esServicioContratado","total","esVigente")
        row_attrs = {
            "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fechaDocumento"

class ContratoTable(DeleteTable):
    def render_costoPactado(self,value):
        return intcomma(value)
    costoPactado = tables.Column(verbose_name= 'Costo Pactado',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    class Meta:
        model = Contrato
        fields = ("fecha","zafra","persona","costoPactado","descripcion")


class VentaTable(VentaTable):
    def render_total(self,value):
        return intcomma(value)
    total = tables.Column(verbose_name= 'Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
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
    total = tables.Column(verbose_name= 'Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
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
    total = tables.Column(verbose_name= 'Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
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
    monto = tables.Column(verbose_name= 'Monto',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
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

    iva5 = tables.Column(verbose_name= 'Iva 5',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    iva10 = tables.Column(verbose_name= 'Iva 10',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    imponibleExenta = tables.Column(verbose_name= 'Imp. Exenta',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    imponible5 = tables.Column(verbose_name= 'Imp. 5',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    imponible10 = tables.Column(verbose_name= 'Imp. 10',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    total = tables.Column(verbose_name= 'Imp. Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })

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
    iva5 = tables.Column(verbose_name= 'Iva 5',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    iva10 = tables.Column(verbose_name= 'Iva 10',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    imponibleExenta = tables.Column(verbose_name= 'Imp. Exenta',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    imponible5 = tables.Column(verbose_name= 'Imp. 5',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    imponible10 = tables.Column(verbose_name= 'Imp. 10',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    total = tables.Column(verbose_name= 'Imp. Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    class Meta:
        model = Venta
        fields = ("fechaDocumento","esCredito","comprobante","cliente","iva5","iva10","imponibleExenta","imponible5","imponible10","total",)

class CompraInformeTable(BaseTable):
    def render_total(self,value):
        return intcomma(value)
    total = tables.Column(verbose_name= 'Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    class Meta:
        model = Compra
        fields = ("fechaDocumento","esCredito","comprobante","proveedor","total",)

class VentaInformeTable(BaseTable):
    total = tables.Column(verbose_name= 'Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
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

    totalMaquinaria = tables.Column(verbose_name= 'Total Maqui.',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    totalItem = tables.Column(verbose_name= 'Total Item',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    total = tables.Column(verbose_name= 'Total',
    attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })

    class Meta:
        model = ActividadAgricola
        fields = ("fechaDocumento","tipoActividadAgricola","zafra","finca","lote","totalMaquinaria","totalItem","total")

class ProduccionAgricolaTable(BaseTable):   
    def render_totalItem(self,value):
        return intcomma(value)
    
    def render_total(self,value):
        return intcomma(value)

    def render_totalMaquinaria(self,value):
        return intcomma(value)

    totalMaquinaria = tables.Column(verbose_name= 'Total Maqui.',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    totalItem = tables.Column(verbose_name= 'Total Item',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    total = tables.Column(verbose_name= 'Total',
    attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })

    class Meta:
        model = ActividadAgricola
        fields = ("fechaDocumento","tipoActividadAgricola","zafra","finca","lote","totalMaquinaria","totalItem","total")



class InventarioDepositoInformeTable(BaseTable):   
    def render_cantidad(self,value):
        return intcomma(value)
    cantidad = tables.Column(verbose_name= 'Cantidad',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    class Meta:
        model = ItemMovimiento
        fields = ("fechaDocumento","deposito","item","tipoMovimiento","cantidad")

class UserTable(EditableDeleteTable):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "is_active",)

class CobroTable(AnulableTable):
    def render_montoASaldar(self,value):
        return intcomma(value)
    montoASaldar = tables.Column(verbose_name= 'Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
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
    total = tables.Column(verbose_name= 'Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    class Meta:
        model = LiquidacionAgricola
        fields = ("fechaDocumento","tipo","zafra","proveedor","total","esVigente")
        row_attrs = {
            "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fechaDocumento"

class NotaDebitoRecibidaTable(AnulableTable):
    def render_total(self,value):
        return intcomma(value)
    total = tables.Column(verbose_name= 'Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
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
    total = tables.Column(verbose_name= 'Total',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    class Meta:
        model = NotaDebitoRecibida
        fields = ("fechaDocumento","comprobante","cliente","total","esVigente",)
        row_attrs = {
            "registro_esVigente": lambda record: record.esVigente
        }
        order_by = "-fechaDocumento"


class CierreZafraTable(DeleteTable):
    def render_totalCultivado(self,value):
        return intcomma(value)
    def render_totalAcopiado(self,value):
        return intcomma(value)
    def render_totalCosto(self,value):
        return intcomma(value)
    def render_totalCostoHa(self,value):
        return intcomma(value)
    def render_totalCostoUnit(self,value):
        return intcomma(value)

    totalAcopiado = tables.Column(verbose_name= 'KG Acopiado',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    totalCultivado = tables.Column(verbose_name= 'HA Cultivada',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        } )
    totalCostoUnit = tables.Column(verbose_name= 'Costo Unit',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    totalCostoHa = tables.Column(verbose_name= 'Costo HA',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })
    totalCosto = tables.Column(verbose_name= 'Costo',attrs={
            "td": {"align": "right"},
            "th":{
            "class":"text-right"
            },
        })


    class Meta:
        model = CierreZafra
        fields = ("fecha","zafra","totalCultivado","totalAcopiado","totalCosto","totalCostoHa","totalCostoUnit")
        order_by = "-fecha"

class PersonaSelectionTable(SelectionTable):
    class Meta:
        model = Persona
        fields = ("razonSocial", "documento", )
