from queue import Empty
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
    ultimoCosto = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ult. Costo",default=0)
    esActivo = models.BooleanField(verbose_name="Activo?")
    codigoBarra = models.CharField(max_length=20, verbose_name="Cód Barra")
    marca = models.ForeignKey(Marca, on_delete=models.DO_NOTHING, verbose_name="Marca")
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, verbose_name="Categoria")
    tipoItem = models.ForeignKey(TipoItem, on_delete=models.DO_NOTHING, verbose_name="Tipo Item")
    tipoImpuesto = models.ForeignKey(TipoImpuesto, on_delete=models.DO_NOTHING, verbose_name="Tipo Imp.")
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
    esCliente = models.BooleanField(verbose_name="Es Cliente?",default=False,help_text="La persona será tratada como un cliente")
    esProveedor = models.BooleanField(verbose_name="Es Proveedor?",default=False,help_text="La persona será tratada como un proveedor")
    esEmpleado = models.BooleanField(verbose_name="Es Empleado?",default=False,help_text="La persona será tratada como un empleado de la empresa")
    
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
    pBruto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Peso Bruto",default=0)
    pTara = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Peso Tara",default=0)
    pDescuento = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Peso Desc.",default=0)
    pBonificacion = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Peso Bonif.",default=0)
    esTransportadoraPropia = models.BooleanField(verbose_name="Es Transportadora Propia?",default=False)
    esVigente = models.BooleanField(verbose_name="Vigente?",default=True)
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")
    @property
    def total(self):
        pesoBru = self.pBruto
        pesoBon = self.pBonificacion
        pesoTara = self.pTara
        pesoDesc = self.pDescuento
        if pesoBru is None :
            pesoBru = 0
        if pesoBon is None :
            pesoBon = 0
        if pesoTara is None :
            pesoTara = 0
        if pesoDesc is None :
            pesoDesc = 0
        return (pesoBru + pesoBon) - (pesoTara + pesoDesc)

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
    def __str__(self):
        return self.proveedor.razonSocial +" - "+ self.observacion
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
    fechaHoraRegistro = models.DateTimeField(auto_now_add=True,verbose_name="Fec Hr Apertura")
    estaCerrado = models.BooleanField(verbose_name="Esta Cerrado?",default=False)
    montoInicio = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Monto Apertura")
    fechaHoraCierre = models.DateTimeField(auto_now_add=True,null=True, blank=True,verbose_name="Fec Hr Cierre")
    def __str__(self):
        date_time = self.fechaHoraRegistro.strftime("%m/%d/%Y, %H:%M:%S")
        return date_time+" Obs: "+self.observacion

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
    esCredito = models.BooleanField(verbose_name="Es Crédito?",default=True)
    esVigente = models.BooleanField(verbose_name="Vigente?",default=True)
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")
    @property
    def total(self):
        return sum(round(x.costo * x.cantidad)  for x in self.compradetalle_set.all())
    def __str__(self):
        return self.comprobante+" - "+self.timbrado
    @property
    def imponible5(self):
        return sum(x.imponible5 for x in self.compradetalle_set.all())
    @property
    def imponible10(self):
        return sum(x.imponible10 for x in self.compradetalle_set.all())
    @property
    def imponibleExenta(self):
        valor = sum(x.imponibleExenta for x in self.compradetalle_set.all())
        if valor is None:
            valor = 0
        return valor
    @property
    def iva5(self):
        valor = sum(x.iva5 for x in self.compradetalle_set.all())
        if valor is None:
            valor = 0
        return valor
    @property
    def iva10(self):
        valor = sum(x.iva10 for x in self.compradetalle_set.all())
        if valor is None:
            valor = 0
        return valor
    @property
    def totalIva(self):
        return self.iva5+self.iva10

class CompraDetalle(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING,verbose_name="Item")
    cantidad = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Cantidad")
    costo = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Costo")
    porcentajeImpuesto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="% Impuesto")
    @property
    def subtotal(self):
        return round(self.costo * self.cantidad)
    @property
    def imponible5(self):
        if self.porcentajeImpuesto == 5:
            valor = round(self.subtotal)
            if valor is None:
                valor = 0
            return valor
        else:
            return 0
    @property
    def imponible10(self):
        if self.porcentajeImpuesto == 10:
            valor = round(self.subtotal)
            if valor is None:
                valor = 0
            return valor
        else:
            return 0
    @property
    def imponibleExenta(self):
        if self.porcentajeImpuesto == 0:
            valor = round(self.subtotal)
            if valor is None:
                valor = 0
            return valor
        else:
            return 0
    @property
    def iva5(self):
        if self.porcentajeImpuesto == 5:
            valor = round(self.subtotal/22)
            if valor is None:
                valor = 0
            return valor
        else:
            return 0
    @property
    def iva10(self):
        if self.porcentajeImpuesto == 10:
            valor = round(self.subtotal/11)
            if valor is None:
                valor = 0
            return valor
        else:
            return 0
class CuotaCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.DO_NOTHING)
    fechaVencimiento = models.DateField(verbose_name="Fecha Vencimiento")
    monto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Monto")
    saldo = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Saldo",default=0)

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
    cantidadTrabajada = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="HA Trabajada")
    @property
    def totalMaquinaria(self):
        retorno = sum(round(x.precio * x.haTrabajada)  for x in self.actividadagricolamaquinariadetalle_set.all())
        if retorno is None:
            retorno = 0
        return retorno
    @property    
    def totalItem(self):
        retorno = sum(round(x.costo * x.cantidad)  for x in self.actividadagricolaitemdetalle_set.all())
        if retorno is None:
            retorno = 0
        return retorno
    @property    
    def total(self):
        maquinaria = self.totalMaquinaria
        item = self.totalItem
        if maquinaria is None: 
           maquinaria = 0
        if item is None: 
            item = 0
        return maquinaria + item 

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


class Contrato(models.Model):
    zafra = models.ForeignKey(Zafra, on_delete=models.DO_NOTHING,verbose_name="Zafra")
    persona = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Persona")
    costoPactado = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Precio Pactado")
    fecha = models.DateField(verbose_name="Fecha")
    descripcion = models.CharField(max_length=300,verbose_name="Descripción")

class Venta(models.Model):
    cliente = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Cliente")
    cuenta = models.ForeignKey(Cuenta, on_delete=models.DO_NOTHING,verbose_name="Cuenta")
    deposito = models.ForeignKey(Deposito, on_delete=models.DO_NOTHING,verbose_name="Deposito")
    aperturaCaja = models.ForeignKey(AperturaCaja, on_delete=models.DO_NOTHING,verbose_name="AperturaCaja")
    fechaDocumento = models.DateField(verbose_name="Fecha Documento")
    fechaHoraRegistro = models.DateTimeField(auto_now_add=True,verbose_name="Fecha Hora Registro")
    comprobante = models.CharField(max_length=15,verbose_name="Comprobante")
    timbrado = models.CharField(max_length=8,verbose_name="Timbrado")
    esCredito = models.BooleanField(verbose_name="Es Crédito?",default=True)
    esVigente = models.BooleanField(verbose_name="Vigente?",default=True)
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")
    @property
    def total(self):
        return sum(round(x.precio * x.cantidad)  for x in self.ventadetalle_set.all())

    @property
    def imponible5(self):
        return sum(x.imponible5 for x in self.ventadetalle_set.all())
    @property
    def imponible10(self):
        return sum(x.imponible10 for x in self.ventadetalle_set.all())
    @property
    def imponibleExenta(self):
        valor = sum(x.imponibleExenta for x in self.ventadetalle_set.all())
        if valor is None:
            valor = 0
        return valor
    @property
    def iva5(self):
        valor = sum(x.iva5 for x in self.ventadetalle_set.all())
        if valor is None:
            valor = 0
        return valor
    @property
    def iva10(self):
        valor = sum(x.iva10 for x in self.ventadetalle_set.all())
        if valor is None:
            valor = 0
        return valor
    @property
    def totalIva(self):
        return self.iva5+self.iva10

    def __str__(self):
        return self.comprobante+" - "+self.timbrado

class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING,verbose_name="Item")
    cantidad = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Cantidad")
    costo = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Costo")
    precio = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Precio")
    porcentajeImpuesto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="% Impuesto")
    @property
    def subtotal(self):
        return round(self.precio * self.cantidad)
    @property
    def imponible5(self):
        if self.porcentajeImpuesto == 5:
            valor = round(self.subtotal)
            if valor is None:
                valor = 0
            return valor
        else:
            return 0
    @property
    def imponible10(self):
        if self.porcentajeImpuesto == 10:
            valor = round(self.subtotal)
            if valor is None:
                valor = 0
            return valor
        else:
            return 0
    @property
    def imponibleExenta(self):
        if self.porcentajeImpuesto == 0:
            valor = round(self.subtotal)
            if valor is None:
                valor = 0
            return valor
        else:
            return 0
    @property
    def iva5(self):
        if self.porcentajeImpuesto == 5:
            valor = round(self.subtotal/22)
            if valor is None:
                valor = 0
            return valor
        else:
            return 0
    @property
    def iva10(self):
        if self.porcentajeImpuesto == 10:
            valor = round(self.subtotal/11)
            if valor is None:
                valor = 0
            return valor
        else:
            return 0

class CuotaVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING)
    fechaVencimiento = models.DateField(verbose_name="Fecha Vencimiento")
    monto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Monto")
    saldo = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Saldo",default=0)

class ItemMovimiento(models.Model):
    VALORESENUMTIPMOV = (
    ('CM', 'COMPRAS'),
    ('VT', 'VENTAS'),
    ('A+', 'AJUSTES STOCK +'),
    ('A-', 'AJUSTES STOCK -'),
    ('AC', 'ACOPIOS'),
    ('AA', 'ACTIVIDADES AGRICOLAS'),
    ('DC', 'DEVOLUCIONES DE COMPRAS'),
    ('DV', 'DEVOLUCIONES DE VENTAS'),
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
    tipoMovimiento = models.CharField(max_length=50,choices=VALORESENUMTIPMOV,verbose_name="Tipo Mov.") 


class NotaCreditoRecibida(models.Model):
    proveedor = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Proveedor")
    compra = models.ForeignKey(Compra, on_delete=models.DO_NOTHING,verbose_name="Compra")
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
        return sum(round(x.valor * x.cantidad)  for x in self.notacreditorecibidadetalle_set.all())

class NotaCreditoRecibidaDetalle(models.Model):
    notaCreditoRecibida = models.ForeignKey(NotaCreditoRecibida, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING,verbose_name="Item")
    cantidad = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Cantidad")
    valor = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Costo/Descuento")
    esDevolucion = models.BooleanField(verbose_name="Es Devolución?",default=False)
    porcentajeImpuesto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="% Impuesto")


class NotaCreditoEmitida(models.Model):
    cliente = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Cliente")
    venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING,verbose_name="Venta")
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
        return sum(round(x.valor * x.cantidad)  for x in self.notacreditoemitidadetalle_set.all())

class NotaCreditoEmitidaDetalle(models.Model):
    notaCreditoEmitida = models.ForeignKey(NotaCreditoEmitida, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING,verbose_name="Item")
    cantidad = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Cantidad")
    valor = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Costo/Descuento")
    esDevolucion = models.BooleanField(verbose_name="Es Devolución?",default=False)
    porcentajeImpuesto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="% Impuesto")


class TransferenciaCuenta(models.Model):
    cuentaSalida = models.ForeignKey(Cuenta, on_delete=models.DO_NOTHING,verbose_name="Cuenta Salida",related_name='salida')
    cuentaEntrada = models.ForeignKey(Cuenta, on_delete=models.DO_NOTHING,verbose_name="Cuenta Entrada",related_name='entrada')
    aperturaCaja = models.ForeignKey(AperturaCaja, on_delete=models.DO_NOTHING,verbose_name="Cuenta Entrada")
    monto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Monto a Transferir")
    fecha = models.DateField(verbose_name="Fecha")
    esVigente = models.BooleanField(verbose_name="Vigente?",default=True)
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")
    comprobante = models.CharField(max_length=15,verbose_name="Comprobante", default="" )


class LiquidacionAgricola(models.Model):
    VALORESENUMTIPMOV = (
    ('ACOPIOS', 'LIQUIDACION DE ACOPIOS'),
    ('ACTIVIDADES AGRICOLAS', 'LIQUIDACION DE ACTIVIDADES AGRICOLAS'),
    )
    zafra = models.ForeignKey(Zafra, on_delete=models.DO_NOTHING,verbose_name="Zafra")
    fechaDocumento = models.DateField(verbose_name="Fecha")
    proveedor = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Proveedor")
    fechaHoraRegistro = models.DateTimeField(auto_now_add=True,verbose_name="Fecha Hora Registro")
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")
    esVigente = models.BooleanField(verbose_name="Vigente?",default=True)
    precioUnitario = models.DecimalField(max_digits=15, decimal_places=0,verbose_name="Precio")
    tipo = models.CharField(max_length=50,choices=VALORESENUMTIPMOV,verbose_name="Tipo Liquidación") 
    @property
    def total(self):
        return sum(round(self.precioUnitario * x.cantidad)  for x in self.liquidacionagricoladetalle_set.all())
        
class LiquidacionAgricolaDetalle(models.Model):
    liquidacionAgricola = models.ForeignKey(LiquidacionAgricola, on_delete=models.DO_NOTHING)
    cantidad = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Cantidad")
    lote = models.ForeignKey(Lote, on_delete=models.DO_NOTHING,verbose_name="Lote")
    finca = models.ForeignKey(Finca, on_delete=models.DO_NOTHING,verbose_name="Finca")
    secuenciaOrigen = models.IntegerField()

class CierreZafra(models.Model):
    zafra = models.ForeignKey(Zafra, on_delete=models.DO_NOTHING,verbose_name="Zafra")
    fecha = models.DateField(verbose_name="Fecha")
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")
    @property
    def totalCosto(self):
        return sum(round(x.costoTotal)  for x in self.cierrezafradetalle_set.all())
    @property
    def totalCultivado(self):
        return sum(round(x.haCultivada)  for x in self.cierrezafradetalle_set.all())
    @property
    def totalAcopiado(self):
        return sum(round(x.cantidadAcopioNeto)  for x in self.cierrezafradetalle_set.all())
    @property
    def totalHA(self):
        return sum(round(x.haCultivada)  for x in self.cierrezafradetalle_set.all())
    @property
    def totalCostoHa(self):
        return round(self.totalCosto / self.totalHA)
    @property
    def totalCostoUnit(self):
        return round(self.totalCosto / self.totalAcopiado)
    def __str__(self):
        return self.zafra.descripcion

class CierreZafraDetalle(models.Model):
    cierreZafra = models.ForeignKey(CierreZafra, on_delete=models.CASCADE)
    finca = models.ForeignKey(Finca, on_delete=models.DO_NOTHING,verbose_name="Finca")
    haCultivada = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="HA Cultivada")
    cantidadAcopioNeto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="KG Acopiado")
    rendimiento = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Rendimiento")
    costoTotal = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Costo Total")
    costoHA = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Costo HA")
    costoUnit = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Costo Unit.")
   
class Cobro(models.Model):
    cobrador = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Cobrador",related_name='cobrador')
    cuenta = models.ForeignKey(Cuenta, on_delete=models.DO_NOTHING,verbose_name="Cuenta")
    aperturaCaja = models.ForeignKey(AperturaCaja, on_delete=models.DO_NOTHING,verbose_name="Apertura Caja")
    fechaDocumento = models.DateField(verbose_name="Fecha")
    cliente = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Cliente",related_name='cliente')
    fechaHoraRegistro = models.DateTimeField(auto_now_add=True,verbose_name="Fecha Hora Registro")
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")
    esVigente = models.BooleanField(verbose_name="Vigente?",default=True)
    montoASaldar = models.DecimalField(max_digits=15, decimal_places=0,verbose_name="Monto A Saldar")
    comprobante = models.CharField(max_length=15,verbose_name="Comprobante")

class CobroDetalle(models.Model):
    cobro = models.ForeignKey(Cobro, on_delete=models.DO_NOTHING)
    cancelacion = models.DecimalField(max_digits=15, decimal_places=0,verbose_name="Cancelacion")
    cuotaVenta = models.ForeignKey(CuotaVenta, on_delete=models.DO_NOTHING,verbose_name="Cuota Venta",default= None,null=True)

class CobroMedio(models.Model):
    VALORESENUMTIPMOV = (
    ('CHEQUE DIF', 'CHEQUE DIFERIDO'),
    ('CHEQUE DIA', 'CHEQUE AL DIA'),
    ('EFECTIVO', 'EFECTIVO'),
    ('TRANSFERENCIA', 'TRANSFERENCIA BANCARIA'),
    )
    cobro = models.ForeignKey(Cobro, on_delete=models.DO_NOTHING)
    numero = models.CharField(max_length=15,verbose_name="N°")
    comprobante = models.CharField(max_length=15,verbose_name="Comprobante")
    monto = models.DecimalField(max_digits=15, decimal_places=0,verbose_name="Monto")
    observacion = models.CharField(max_length=300, null=True, blank=True,verbose_name="Observación")
    medioCobro = models.CharField(max_length=50,choices=VALORESENUMTIPMOV,verbose_name="Medio Cobro") 

class NotaDebitoRecibida(models.Model):
    proveedor = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Proveedor")
    compra = models.ForeignKey(Compra, on_delete=models.DO_NOTHING,verbose_name="Compra")
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
        return sum(round(x.valor * x.cantidad)  for x in self.notadebitorecibidadetalle_set.all())

class NotaDebitoRecibidaDetalle(models.Model):
    notaDebitoRecibida = models.ForeignKey(NotaDebitoRecibida, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING,verbose_name="Item")
    cantidad = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Cantidad")
    valor = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Precio/Aumento")
    porcentajeImpuesto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="% Impuesto")

class NotaDebitoEmitida(models.Model):
    cliente = models.ForeignKey(Persona, on_delete=models.DO_NOTHING,verbose_name="Cliente")
    venta = models.ForeignKey(Venta, on_delete=models.DO_NOTHING,verbose_name="Venta")
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
        return sum(round(x.valor * x.cantidad)  for x in self.notadebitoemitidadetalle_set.all())

class NotaDebitoEmitidaDetalle(models.Model):
    notaDebitoEmitida = models.ForeignKey(NotaDebitoEmitida, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING,verbose_name="Item")
    cantidad = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Cantidad")
    valor = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="Costo/Descuento")
    porcentajeImpuesto = models.DecimalField(max_digits=15, decimal_places=2,verbose_name="% Impuesto")

# IMPLEMENTAMOS LAS SENAÑES
from .signals import signalCompraGuardado
from .signals import signalAjusteStockGuardado
from .signals import signalAcopioGuardado
from .signals import signalActividadAgricolaItemGuardado
from .signals import signalVentaPreGuardado
from .signals import signalVentaDetallePreGuardado
from .signals import signalVentaGuardado
from .signals import signalNotaCreditoEmitidaGuardado
from .signals import signalTransferenciaCuentaPreGuardado
from .signals import signalCobroPreGuardado
from .signals import signalCobroDetalleSave
from .signals import signalPreGuardadoCuotaVenta
from .signals import signalCobroAnulado
from .signals import signalCierreZafraSave
from .signals import signalCierreZafraDetalleGuardado
#from .signals import signalCierreZafraBorrar

 