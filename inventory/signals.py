from django.db.models.signals import post_save,pre_save,pre_delete
from .models import AcopioDetalle, ActividadAgricolaItemDetalle, AjusteStockDetalle, AperturaCaja, CierreZafra, CierreZafraDetalle, Cobro, CobroDetalle, CompraDetalle, CuotaVenta, Item,ItemMovimiento, NotaCreditoEmitidaDetalle, NotaCreditoRecibidaDetalle, TransferenciaCuenta, Venta, VentaDetalle, Zafra
from django.dispatch import receiver


@receiver(pre_save, sender = CompraDetalle)
def signalCompraDetallePreGuardado(sender, instance, **kwargs):
   pass

@receiver(post_save, sender = CompraDetalle)
def signalCompraGuardado(sender, instance, created, **kwargs):
    if created:
        itMov = ItemMovimiento()
        itMov.item = instance.item
        itMov.deposito = instance.compra.deposito
        itMov.cantidad = instance.cantidad
        itMov.costo = instance.costo
        itMov.precio = 0
        itMov.fechaDocumento = instance.compra.fechaDocumento
        itMov.secuenciaOrigen = instance.compra.pk
        itMov.detalleSecuenciaOrigen = instance.pk
        itMov.esVigente = True
        itMov.tipoMovimiento = 'CM'
        itMov.save()

        item = Item.objects.get(pk=instance.item.pk)
        item.ultimoCosto = instance.costo
        item.costo = instance.costo
        item.save()

@receiver(post_save, sender = AjusteStockDetalle)
def signalAjusteStockGuardado(sender, instance, created, **kwargs):
    if created:
        itMov = ItemMovimiento()
        itMov.item = instance.item
        itMov.deposito = instance.ajusteStock.deposito
        itMov.cantidad = instance.cantidad
        itMov.costo = 0
        itMov.precio = 0
        itMov.fechaDocumento = instance.ajusteStock.fechaDocumento
        itMov.secuenciaOrigen = instance.ajusteStock.pk
        itMov.detalleSecuenciaOrigen = instance.pk
        itMov.esVigente = True
        tipo = ''
        if instance.cantidad >= 0:
            tipo = 'AJ+'
        else:
             tipo = 'AJ-'
        itMov.tipoMovimiento = tipo
        itMov.save()


@receiver(post_save, sender = AcopioDetalle)
def signalAcopioGuardado(sender, instance, created, **kwargs):
    if created:
        itMov = ItemMovimiento()
        itMov.item = instance.acopio.zafra.item
        itMov.deposito = instance.acopio.deposito
        itMov.cantidad = instance.peso
        itMov.costo = 0
        itMov.precio = 0
        itMov.fechaDocumento = instance.acopio.fecha
        itMov.secuenciaOrigen = instance.acopio.pk
        itMov.detalleSecuenciaOrigen = instance.pk
        itMov.esVigente = True
        itMov.tipoMovimiento = 'AC'
        itMov.save()


@receiver(post_save, sender = ActividadAgricolaItemDetalle)
def signalActividadAgricolaItemGuardado(sender, instance, created, **kwargs):
    if created:
        itMov = ItemMovimiento()
        itMov.item = instance.item
        itMov.deposito = instance.deposito
        itMov.cantidad = instance.cantidad
        itMov.costo = instance.costo
        itMov.precio = 0
        itMov.fechaDocumento = instance.actividadAgricola.fechaDocumento
        itMov.secuenciaOrigen = instance.actividadAgricola.pk
        itMov.detalleSecuenciaOrigen = instance.pk
        itMov.esVigente = True
        itMov.tipoMovimiento = 'AA'
        itMov.save()

@receiver(pre_save, sender = Venta)
def signalVentaPreGuardado(sender, instance, **kwargs):
    aperturaCaja = AperturaCaja.objects.filter(estaCerrado = False).order_by('-pk')[:1].first()
    timbrado = '12332145'
    instance.aperturaCaja = aperturaCaja
    instance.timbrado = timbrado

@receiver(pre_save, sender = TransferenciaCuenta)
def signalTransferenciaCuentaPreGuardado(sender, instance, **kwargs):
    aperturaCaja = AperturaCaja.objects.filter(estaCerrado = False).order_by('-pk')[:1].first()
    instance.aperturaCaja = aperturaCaja

@receiver(pre_save, sender = VentaDetalle)
def signalVentaDetallePreGuardado(sender, instance, **kwargs):
   instance.costo = instance.item.costo

@receiver(post_save, sender = VentaDetalle)
def signalVentaGuardado(sender, instance, created, **kwargs):
    if created:
        itMov = ItemMovimiento()
        itMov.item = instance.item
        itMov.deposito = instance.venta.deposito
        itMov.cantidad = instance.cantidad
        itMov.costo = instance.costo
        itMov.precio = instance.precio
        itMov.fechaDocumento = instance.venta.fechaDocumento
        itMov.secuenciaOrigen = instance.venta.pk
        itMov.detalleSecuenciaOrigen = instance.pk
        itMov.esVigente = True
        itMov.tipoMovimiento = 'VT'
        itMov.save()


@receiver(post_save, sender = NotaCreditoRecibidaDetalle)
def signalNotaCreditoRecibidaGuardado(sender, instance, created, **kwargs):
    if created:
        itMov = ItemMovimiento()
        itMov.item = instance.item
        itMov.deposito = instance.notaCreditoRecibida.deposito
        itMov.cantidad = instance.cantidad
        itMov.costo = instance.valor
        itMov.precio = instance.valor
        itMov.fechaDocumento = instance.notaCreditoRecibida.fechaDocumento
        itMov.secuenciaOrigen = instance.notaCreditoRecibida.pk
        itMov.detalleSecuenciaOrigen = instance.pk
        itMov.esVigente = True
        itMov.tipoMovimiento = 'DC'
        itMov.save()

@receiver(post_save, sender = NotaCreditoEmitidaDetalle)
def signalNotaCreditoEmitidaGuardado(sender, instance, created, **kwargs):
    if created:
        itMov = ItemMovimiento()
        itMov.item = instance.item
        itMov.deposito = instance.notaCreditoEmitida.deposito
        itMov.cantidad = instance.cantidad
        itMov.costo = instance.item.costo
        itMov.precio = instance.valor
        itMov.fechaDocumento = instance.notaCreditoEmitida.fechaDocumento
        itMov.secuenciaOrigen = instance.notaCreditoEmitida.pk
        itMov.detalleSecuenciaOrigen = instance.pk
        itMov.esVigente = True
        itMov.tipoMovimiento = 'DV'
        itMov.save()


@receiver(pre_save, sender = Cobro)
def signalCobroPreGuardado(sender, instance, **kwargs):
    aperturaCaja = AperturaCaja.objects.filter(estaCerrado = False).order_by('-pk')[:1].first()
    instance.aperturaCaja = aperturaCaja


@receiver(pre_save, sender = CuotaVenta)
def signalPreGuardadoCuotaVenta(sender, instance, **kwargs):
    if instance.pk is None:
        instance.saldo =  instance.monto


@receiver(post_save, sender = CobroDetalle)
def signalCobroDetalleSave(sender, instance, created, **kwargs):
    if created:
        cuota = CuotaVenta.objects.get(pk=instance.cuotaVenta.pk)
        cuota.saldo = cuota.saldo - instance.cancelacion
        cuota.save()

@receiver(post_save, sender = Cobro)
def signalCobroAnulado(sender, instance, created, **kwargs):
    print("entra en la señal")
    if created == False:
        cobroDetalle = CobroDetalle.objects.filter(cobro__pk = instance.pk)
        for f in cobroDetalle:
            cuotaVenta = CuotaVenta.objects.get(pk = f.cuotaVenta.pk)
            cuotaVenta.saldo =  cuotaVenta.saldo + f.cancelacion  
            cuotaVenta.save()
    else: 
         print("entra en la señal create true")

@receiver(post_save, sender = CierreZafra)
def signalCierreZafraSave(sender, instance, created, **kwargs):
    if created:
        zafra = Zafra.objects.get(pk=instance.zafra.pk)
        zafra.estaCerrado = True
        zafra.save()

@receiver(post_save, sender = CierreZafraDetalle)
def signalCierreZafraDetalleGuardado(sender, instance, created, **kwargs):
    if created:
        detalleCierreZafra = CierreZafraDetalle.objects.filter(cierreZafra = instance.cierreZafra)
        sumaCantidadAcopiada = 0
        sumaCostoTotal = 0
        costoUnitario = 0
        for x in detalleCierreZafra:
            sumaCantidadAcopiada += x.cantidadAcopioNeto
            sumaCostoTotal += x.costoTotal 

        if sumaCantidadAcopiada > 0 and sumaCostoTotal > 0 :
            costoUnitario = round(sumaCostoTotal / sumaCantidadAcopiada)
            item = Item.objects.get(pk= instance.cierreZafra.zafra.item.pk)
            item.ultimoCosto = costoUnitario
            item.costo = costoUnitario
            item.save()

@receiver(pre_delete, sender = CierreZafra)
def signalCierreZafraBorrar(sender, instance, **kwargs):
    zafra = Zafra.objects.get(pk=instance.zafra.pk)
    zafra.estaCerrado = False
    zafra.save()



        