from django.db.models.signals import post_save,pre_save
from .models import AcopioDetalle, ActividadAgricolaItemDetalle, AjusteStockDetalle, AperturaCaja, CompraDetalle, Item,ItemMovimiento, Venta, VentaDetalle
from django.dispatch import receiver

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

#@receiver(post_save, sender = CompraDetalle)
#def signalCompraGuardado(sender, instance, created, **kwargs):
#    if created:
#        itMov = ItemMovimiento()
#        itMov.item = instance.item
#        itMov.deposito = instance.compra.deposito
#        itMov.cantidad = instance.cantidad
#        itMov.costo = instance.costo
#        itMov.precio = 0
#        itMov.fechaDocumento = instance.compra.fechaDocumento
#        itMov.secuenciaOrigen = instance.compra.pk
##        itMov.detalleSecuenciaOrigen = instance.pk
#        itMov.esVigente = True
#        itMov.tipoMovimiento = 'CM'
#        itMov.save()

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



