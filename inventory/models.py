from django.db import models


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

