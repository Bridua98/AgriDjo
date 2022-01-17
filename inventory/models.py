from django.db import models
from datetime import datetime



class TipoActividadAgricola(models.Model):
    #  error_messages={'unique': u'My custom message'}
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion",unique=True)
    esCosecha = models.BooleanField(verbose_name="es Cosecha")
    esSiembra = models.BooleanField(verbose_name="es Siembra")
    esResiembra = models.BooleanField(verbose_name="es Resiembra")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descripcion

class Finca(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion",unique=True)
    dimensionHa = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Dimension Ha")
    ubicacion = models.CharField(max_length=200,verbose_name="Ubicacion")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descripcion

class TipoMaquinariaAgricola(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion",unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descripcion

class Marca(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descripcion

class Categoria(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descripcion

class TipoImpuesto(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion",unique=True)
    porcentaje = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="% Impuesto")
    esIva = models.BooleanField(max_length=200,verbose_name="es IVA?")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descripcion


class TipoItem(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion",unique=True)
    def __str__(self):
        return self.descripcion

class Item(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    costo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo",default=0)
    ultimoCosto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Último Costo",default=0)
    esActivo = models.BooleanField(verbose_name="es Activo?")
    codigoBarra = models.CharField(max_length=20, verbose_name="Código de Barra")
    marca = models.ForeignKey(Marca, on_delete=models.DO_NOTHING, verbose_name="Marca")
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, verbose_name="Categoria")
    tipoItem = models.ForeignKey(TipoItem, on_delete=models.DO_NOTHING, verbose_name="Tipo Item")
    tipoImpuesto = models.ForeignKey(TipoImpuesto, on_delete=models.DO_NOTHING, verbose_name="Tipo Impuesto")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descripcion

class Zafra(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion")
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, verbose_name="Item")
    anho = models.IntegerField(verbose_name="Anho")
    kgEstimado = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Kg Estimado")
    esZafrinha = models.BooleanField(verbose_name="Es Zafriña?")
    estaCerrado = models.BooleanField(verbose_name="Está Cerrado?",default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descripcion

class Lote(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion")
    zafra = models.ForeignKey(Zafra, on_delete=models.DO_NOTHING, verbose_name="Zafra")
    finca = models.ForeignKey(Finca, on_delete=models.DO_NOTHING, verbose_name="Finca")
    dimension = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Dimensión HA")
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.descripcion

class MaquinariaAgricola(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion")
    tipoMaquinariaAgricola = models.ForeignKey(TipoMaquinariaAgricola, on_delete=models.DO_NOTHING, verbose_name="Maquinaria Agrícola Tipo")
    esImplemento = models.BooleanField(verbose_name="Es Implemento?")
    admiteImplemento = models.BooleanField(verbose_name="Admite Implemento?")
    precio = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Precio")
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.descripcion

class Banco(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion",unique=True)
    def __str__(self):
        return self.descripcion

class Deposito(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion",unique=True)
    esPlantaAcopiadora = models.BooleanField(verbose_name="Es Planta Acopiadora?",default=False)
    def __str__(self):
        return self.descripcion

class Cuenta(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion",unique=True)
    esBanco = models.BooleanField(verbose_name="Es Banco?",default=False)
    nroCuenta = models.CharField(max_length=200, verbose_name="Nro Cuenta",null=True,blank=True)
    banco = models.ForeignKey(Banco, on_delete=models.DO_NOTHING, verbose_name="Banco",null=True,blank=True)
    def __str__(self):
        return self.descripcion

class Pais(models.Model):
    abreviatura = models.CharField(max_length=200, verbose_name="Descripcion",unique=True)
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion",unique=True)
    def __str__(self):
        return self.descripcion

class Departamento(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion",unique=True)
    def __str__(self):
        return self.descripcion

class Distrito(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion")
    departamento = models.ForeignKey(Departamento, on_delete=models.DO_NOTHING, verbose_name="Departamento")
    def __str__(self):
        return self.descripcion

class Localidad(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion")
    distrito = models.ForeignKey(Distrito, on_delete=models.DO_NOTHING, verbose_name="Distrito")
    def __str__(self):
        return self.descripcion

class Persona(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.DO_NOTHING, verbose_name="Pais")
    localidad = models.ForeignKey(Localidad, on_delete=models.DO_NOTHING, verbose_name="Localidad")
    razonSocial = models.CharField(max_length=200, verbose_name="Razon Social")
    documento = models.CharField(max_length=40, verbose_name="Documento")
    direccion = models.CharField(max_length=200, verbose_name="Direccion")
    celular = models.CharField(max_length=60, verbose_name="Celular / Telefono",null=True,blank=True)
    esCliente = models.BooleanField(verbose_name="Es Cliente?",default=False)
    esProveedor = models.BooleanField(verbose_name="Es Proveedor?",default=False)
    esEmpleado = models.BooleanField(verbose_name="Es Empleado?",default=False)
    
    def __str__(self):
        return self.razonSocial

class PlanActividadZafra(models.Model):
    fecha = models.DateField(verbose_name="Fecha")
    zafra = models.ForeignKey(Zafra, on_delete=models.DO_NOTHING, null=True, blank=True,verbose_name="Zafra")
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")

    @property
    def total(self):
        return sum(round(x.costo)  for x in self.planactividadzafradetalle_set.all())

class PlanActividadZafraDetalle(models.Model):
    planActividadZafra = models.ForeignKey(PlanActividadZafra, on_delete=models.DO_NOTHING)
    fechaActividad = models.DateField(verbose_name="Fecha Act.")
    finca = models.ForeignKey(Finca, on_delete=models.DO_NOTHING,verbose_name="Finca")
    tipoActividadAgricola = models.ForeignKey(TipoActividadAgricola, on_delete=models.DO_NOTHING, null=True, blank=True,verbose_name="Tipo Actividad Agrícola")
    descripcion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Descripción")
    costo = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Costo Estimado")



class Acopio(models.Model):
    zafra = models.ForeignKey(Zafra, on_delete=models.DO_NOTHING,verbose_name="Zafra")
    deposito = models.ForeignKey(Deposito, on_delete=models.DO_NOTHING,verbose_name="Depósito")
    conductor = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Conductor")
    camion = models.ForeignKey(MaquinariaAgricola, on_delete=models.DO_NOTHING,verbose_name="Camión")
    fecha = models.DateField(verbose_name="Fecha")
    comprobante = models.CharField(max_length=30,verbose_name="Comprobante")
    pBruto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Peso Bruto")
    pTara = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Peso Tara")
    pDescuento = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Peso Descuento")
    pBonificacion = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Peso Bonificación")
    esTransportadoraPropia = models.BooleanField(verbose_name="Es Transportadora Propia?",default=False)
    esVigente = models.BooleanField(verbose_name="Vigente?",default=True)
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")

class AcopioDetalle(models.Model):
    acopio = models.ForeignKey(Acopio, on_delete=models.DO_NOTHING)
    finca = models.ForeignKey(Finca, on_delete=models.DO_NOTHING,verbose_name="Finca")
    lote = models.ForeignKey(Lote, on_delete=models.DO_NOTHING,verbose_name="Lote")
    peso = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Peso")

class CalificacionAgricola(models.Model):
    descripcion = models.CharField(max_length=200, verbose_name="Descripcion",unique=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.descripcion

class AcopioCalificacion(models.Model):
    acopio = models.ForeignKey(Acopio, on_delete=models.DO_NOTHING)
    calificacionAgricola = models.ForeignKey(CalificacionAgricola, on_delete=models.DO_NOTHING,verbose_name="Calif. Agrícola")
    grado = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Grado")
    porcentaje = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Porcentaje")
    peso = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Peso")

class PedidoCompra(models.Model):
    proveedor = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Proveedor")
    fechaDocumento = models.DateField(verbose_name="Fecha Documento")
    fechaVencimiento = models.DateField(verbose_name="Fecha Vencimiento")
    esVigente = models.BooleanField(verbose_name="Vigente?",default=True)
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")
    @property
    def total(self):
        return sum(round(x.cantidad)  for x in self.pedidocompradetalle_set.all())
    
class PedidoCompraDetalle(models.Model):
    pedidoCompra = models.ForeignKey(PedidoCompra, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING,verbose_name="Item")
    cantidad = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Cantidad")

class OrdenCompra(models.Model):
    pedidoCompra = models.ForeignKey(PedidoCompra, on_delete=models.DO_NOTHING,verbose_name="Pedido Compra")
    proveedor = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Proveedor")
    fechaDocumento = models.DateField(verbose_name="Fecha Documento")
    esVigente = models.BooleanField(verbose_name="Vigente?",default=True)
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")
    @property
    def total(self):
        return sum(round(x.precio*x.cantidad)  for x in self.ordencompradetalle_set.all())

class OrdenCompraDetalle(models.Model):
    ordenCompra = models.ForeignKey(OrdenCompra, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING,verbose_name="Item")
    cantidad = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Cantidad")
    precio = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Precio")
    descuento = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Descuento")

class AperturaCaja(models.Model):
    empleado = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Empleado")
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")
    fechaHoraRegistro = models.DateTimeField(auto_now_add=True,verbose_name="Fecha Hora Registro")
    estaCerrado = models.BooleanField(verbose_name="Esta Cerrado?",default=False)
    montoInicio = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Monto Apertura")
    fechaHoraCierre = models.DateTimeField(auto_now_add=True,null=True, blank=True,verbose_name="Fecha Hora Cierre")
    def __str__(self):
        return "Fecha: "+self.fechaHoraRegistro.strftime("%m/%d/%Y, %H:%M:%S")+" / Empl: "+self.empleado.razonSocial

class Arqueo(models.Model):
    empleado = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Empleado")
    aperturaCaja = models.ForeignKey(AperturaCaja, on_delete=models.DO_NOTHING,verbose_name="Apertura Caja")
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")
    fechaHoraRegistro = models.DateTimeField(auto_now_add=True,verbose_name="Fecha Hora Registro")
    monto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Monto Retirado")


class Compra(models.Model):
    proveedor = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Proveedor")
    cuenta = models.ForeignKey(Cuenta, on_delete=models.DO_NOTHING,verbose_name="Cuenta")
    deposito = models.ForeignKey(Deposito, on_delete=models.DO_NOTHING,verbose_name="Deposito")
    fechaDocumento = models.DateField(verbose_name="Fecha Documento")
    fechaHoraRegistro = models.DateTimeField(auto_now_add=True,verbose_name="Fecha Hora Registro")
    comprobante = models.CharField(max_length=15,verbose_name="Comprobante")
    timbrado = models.CharField(max_length=8,verbose_name="Timbrado")
    esCredito = models.BooleanField(verbose_name="Es Crédito?",default=False)
    esVigente = models.BooleanField(verbose_name="Vigente?",default=True)
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")
    @property
    def total(self):
        return sum(round(x.costo * x.cantidad)  for x in self.compradetalle_set.all())

class CompraDetalle(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING,verbose_name="Item")
    cantidad = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Cantidad")
    costo = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Costo")
    porcentajeImpuesto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="% Impuesto")

class AjusteStock(models.Model):
    empleado = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Empleado")
    deposito = models.ForeignKey(Deposito, on_delete=models.DO_NOTHING,verbose_name="Deposito")
    fechaDocumento = models.DateField(verbose_name="Fecha")
    fechaHoraRegistro = models.DateTimeField(auto_now_add=True,verbose_name="Fecha Hora Registro")
    comprobante = models.CharField(max_length=15,verbose_name="Comprobante")
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")

class AjusteStockDetalle(models.Model):
    ajusteStock = models.ForeignKey(AjusteStock, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING,verbose_name="Item")
    cantidad = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Cantidad")

class ActividadAgricola(models.Model):
    tipoActividadAgricola = models.ForeignKey(TipoActividadAgricola, on_delete=models.DO_NOTHING,verbose_name="Tipo Act. Agrícola")
    lote = models.ForeignKey(Lote, on_delete=models.DO_NOTHING,verbose_name="Lote")
    zafra = models.ForeignKey(Zafra, on_delete=models.DO_NOTHING,verbose_name="Zafra")
    finca = models.ForeignKey(Finca, on_delete=models.DO_NOTHING,verbose_name="Finca")
    fechaDocumento = models.DateField(verbose_name="Fecha")
    empleado = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Empleado")
    fechaHoraRegistro = models.DateTimeField(auto_now_add=True,verbose_name="Fecha Hora Registro")
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")
    esVigente = models.BooleanField(verbose_name="Vigente?",default=True)
    esServicioContratado = models.BooleanField(verbose_name="Es contratado?",default=False)
    cantidadTrabajada = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Cant HA Trabajada")

class ActividadAgricolaMaquinariaDetalle(models.Model):
    actividadAgricola = models.ForeignKey(ActividadAgricola, on_delete=models.DO_NOTHING)
    maquinaria = models.ForeignKey(MaquinariaAgricola, on_delete=models.DO_NOTHING,verbose_name="Maquinaria")
    haTrabajada = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Ha Trabajada")
    precio = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Precio HA")

class ActividadAgricolaItemDetalle(models.Model):
    actividadAgricola = models.ForeignKey(ActividadAgricola, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING,verbose_name="Item")
    costo = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Costo")
    cantidad = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Cantidad")
    porcentajeImpuesto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="% Impuesto")
    dosis = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Dosis")
    deposito = models.ForeignKey(Deposito, on_delete=models.DO_NOTHING,verbose_name="Deposito",default=1)

class ItemMovimiento(models.Model):
    VALORESENUMTIPMOV = (
    ('CM', 'COMPRAS'),
    ('VT', 'VENTAS'),
    ('A+', 'AJUSTES STOCK +'),
    ('A-', 'AJUSTES STOCK -'),
    ('AC', 'ACOPIOS'),
    ('AA', 'ACTIVIDADES AGRICOLAS'),
    )
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING,verbose_name="Item")
    deposito = models.ForeignKey(Deposito, on_delete=models.DO_NOTHING,verbose_name="Deposito")
    cantidad = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Cantidad")
    costo = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Costo")
    precio = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Precio")
    fechaDocumento = models.DateField(verbose_name="Fecha Documento")
    secuenciaOrigen = models.IntegerField()
    detalleSecuenciaOrigen = models.IntegerField()
    esVigente = models.BooleanField(verbose_name="Vigente?",default=True) 
    tipoMovimiento = models.CharField(max_length=50,choices=VALORESENUMTIPMOV) 

# IMPLEMENTAMOS LA SEÑAL DE COMPRA
from .signals import signalCompraGuardado
from .signals import signalAjusteStockGuardado
from .signals import signalAcopioGuardado
from .signals import signalActividadAgricolaItemGuardado