"""invsist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url

# importando vistas
from inventory.views import AcopioAnularView, AcopioCreateView, AcopioListView, AcopioUpdateView, ActividadAgricolaAnularView, ActividadAgricolaCreateView, ActividadAgricolaListView, AjusteStockCreateView, AjusteStockDeleteView, AjusteStockListView, AjusteStockUpdateView, AperturaCajaCerrarView, AperturaCajaCreateView, AperturaCajaListView, ArqueoCreateView, ArqueoDeleteView, ArqueoListView, BancoCreateView, BancoDeleteView, BancoListView, BancoUpdateView, CalificacionAgricolaCreateView, CalificacionAgricolaDeleteView, CalificacionAgricolaListView, CalificacionAgricolaUpdateView, CategoriaCreateView, CategoriaDeleteView, CategoriaListView, CategoriaUpdateView, CierreZafraSelectionView, CobroAnularView, CobroCreateView, CobroListView, CompraAnularView, CompraCreateView, CompraInformeListView, CompraListView, ContratoCreateView, ContratoDeleteView, ContratoListView, CuentaCreateView, CuentaDeleteView, CuentaListView, CuentaUpdateView, CustomPasswordChangeDoneView, CustomPasswordChangeView, DepositoCreateView, DepositoDeleteView, DepositoListView, DepositoUpdateView, InventarioDepositoInformeListView, ItemCreateView, LibroCompraListView, LibroVentaListView, LiquidacionAgricolaAnularView, LiquidacionAgricolaCreateView, LiquidacionAgricolaListView, LoteCreateView, LoteDeleteView, LoteListView, LoteUpdateView, MaquinariaAgricolaCreateView, MaquinariaAgricolaDeleteView, MaquinariaAgricolaListView, MaquinariaAgricolaUpdateView, NotaCreditoEmitidaAnularView, NotaCreditoEmitidaCreateView, NotaCreditoEmitidaListView, NotaCreditoRecibidaAnularView, NotaCreditoRecibidaCreateView, NotaCreditoRecibidaListView, NotaDebitoEmitidaAnularView, NotaDebitoEmitidaCreateView, NotaDebitoEmitidaListView, NotaDebitoRecibidaAnularView, NotaDebitoRecibidaCreateView, NotaDebitoRecibidaListView, OrdenCompraAnularView, OrdenCompraCreateView, OrdenCompraListView, OrdenCompraUpdateView, PedidoCompraCreateView, PedidoCompraListView, PedidoCompraUpdateView, PersonaCreateView, PersonaDeleteView, PersonaListView, PersonaUpdateView, PlanActividadZafraCreateView, PlanActividadZafraListView, PlanActividadZafraUpdateView, ProduccionAgricolaInformeListView, TipoImpuestoCreateView, TipoImpuestoDeleteView, TipoImpuestoListView, TipoImpuestoUpdateView, TransferenciaCuentaAnularView, TransferenciaCuentaCreateView, TransferenciaCuentaListView, UserDeleteView, VentaAnularView, VentaCreateView, VentaInformeListView, VentaListView, ZafraCreateView, ZafraDeleteView, ZafraListView, ZafraUpdateView, CierreZafraCreateView, CierreZafraDeleteView, CierreZafraListView
from inventory.views import MarcaCreateView, MarcaDeleteView, MarcaListView, MarcaUpdateView
from inventory.views import TipoMaquinariaAgricolaCreateView, TipoMaquinariaAgricolaDeleteView, TipoMaquinariaAgricolaListView, TipoMaquinariaAgricolaUpdateView
from inventory.views import ItemDeleteView, ItemListView, ItemUpdateView
from inventory.views import TipoActividadAgricolaListView, TipoActividadAgricolaCreateView, TipoActividadAgricolaUpdateView, TipoActividadAgricolaDeleteView
from inventory.views import FincaListView, FincaCreateView, FincaUpdateView, FincaDeleteView
from inventory.views import main, menu, download_view
from inventory.views import UserCreateView, UserListView, UserUpdateView
from inventory.views import PersonaSelectionListView, LiquidacionAgricolaSelectionView

urlpatterns = [
     # personas
    path('inventory/persona/<int:pk>/delete',PersonaDeleteView.as_view(), name="persona_delete"),
    path('inventory/persona/<int:pk>/update',PersonaUpdateView.as_view(), name="persona_update"),
    path('inventory/persona/add',PersonaCreateView.as_view(), name="persona_create"),
    path('inventory/persona', PersonaListView.as_view(), name="persona_list"),
    # item
    path('inventory/item/<int:pk>/delete', ItemDeleteView.as_view(), name="item_delete"),
    path('inventory/item/<int:pk>/update',ItemUpdateView.as_view(), name="item_update"),
    path('inventory/item/add', ItemCreateView.as_view(), name="item_create"),
    path('inventory/item', ItemListView.as_view(), name="item_list"),
    # categoria
    path('inventory/categoria/<int:pk>/delete', CategoriaDeleteView.as_view(), name="categoria_delete"),
    path('inventory/categoria/<int:pk>/update', CategoriaUpdateView.as_view(), name="categoria_update"),
    path('inventory/categoria/add', CategoriaCreateView.as_view(), name="categoria_create"),
    path('inventory/categoria', CategoriaListView.as_view(), name="categoria_list"),
    # marca
    path('inventory/marca/<int:pk>/delete', MarcaDeleteView.as_view(), name="marca_delete"),
    path('inventory/marca/<int:pk>/update', MarcaUpdateView.as_view(), name="marca_update"),
    path('inventory/marca/add', MarcaCreateView.as_view(), name="marca_create"),
    path('inventory/marca', MarcaListView.as_view(), name="marca_list"),
    # tipoActividadAgricola
    path('inventory/tipo_actividad_agricola/<int:pk>/delete', TipoActividadAgricolaDeleteView.as_view(), name="tipo_actividad_agricola_delete"),
    path('inventory/tipo_actividad_agricola/<int:pk>/update',TipoActividadAgricolaUpdateView.as_view(), name="tipo_actividad_agricola_update"),
    path('inventory/tipo_actividad_agricola/add',TipoActividadAgricolaCreateView.as_view(), name="tipo_actividad_agricola_create"),
    path('inventory/tipo_actividad_agricola', TipoActividadAgricolaListView.as_view(), name="tipo_actividad_agricola_list"),
     # finca
    path('inventory/finca/<int:pk>/delete',FincaDeleteView.as_view(), name="finca_delete"),
    path('inventory/finca/<int:pk>/update',FincaUpdateView.as_view(), name="finca_update"),
    path('inventory/finca/add',FincaCreateView.as_view(), name="finca_create"),
    path('inventory/finca', FincaListView.as_view(), name="finca_list"),
    # tipo maquinaria agricola
    path('inventory/tipo_maquinaria_agricola/<int:pk>/delete',TipoMaquinariaAgricolaDeleteView.as_view(), name="tipo_maquinaria_agricola_delete"),
    path('inventory/tipo_maquinaria_agricola/<int:pk>/update',TipoMaquinariaAgricolaUpdateView.as_view(), name="tipo_maquinaria_agricola_update"),
    path('inventory/tipo_maquinaria_agricola/add',TipoMaquinariaAgricolaCreateView.as_view(), name="tipo_maquinaria_agricola_create"),
    path('inventory/tipo_maquinaria_agricola', TipoMaquinariaAgricolaListView.as_view(), name="tipo_maquinaria_agricola_list"),
    # tipo impuesto
    path('inventory/tipo_impuesto/<int:pk>/delete',TipoImpuestoDeleteView.as_view(), name="tipo_impuesto_delete"),
    path('inventory/tipo_impuesto/<int:pk>/update',TipoImpuestoUpdateView.as_view(), name="tipo_impuesto_update"),
    path('inventory/tipo_impuesto/add',TipoImpuestoCreateView.as_view(), name="tipo_impuesto_create"),
    path('inventory/tipo_impuesto', TipoImpuestoListView.as_view(), name="tipo_impuesto_list"),
    # bancos
    path('inventory/banco/<int:pk>/delete',BancoDeleteView.as_view(), name="banco_delete"),
    path('inventory/banco/<int:pk>/update',BancoUpdateView.as_view(), name="banco_update"),
    path('inventory/banco/add',BancoCreateView.as_view(), name="banco_create"),
    path('inventory/banco', BancoListView.as_view(), name="banco_list"),
    # cuentas
    path('inventory/cuenta/<int:pk>/delete',CuentaDeleteView.as_view(), name="cuenta_delete"),
    path('inventory/cuenta/<int:pk>/update',CuentaUpdateView.as_view(), name="cuenta_update"),
    path('inventory/cuenta/add',CuentaCreateView.as_view(), name="cuenta_create"),
    path('inventory/cuenta', CuentaListView.as_view(), name="cuenta_list"),
    # deposito
    path('inventory/deposito/<int:pk>/delete',DepositoDeleteView.as_view(), name="deposito_delete"),
    path('inventory/deposito/<int:pk>/update',DepositoUpdateView.as_view(), name="deposito_update"),
    path('inventory/deposito/add',DepositoCreateView.as_view(), name="deposito_create"),
    path('inventory/deposito', DepositoListView.as_view(), name="deposito_list"),
    # zafra
    path('inventory/zafra/<int:pk>/delete',ZafraDeleteView.as_view(), name="zafra_delete"),
    path('inventory/zafra/<int:pk>/update',ZafraUpdateView.as_view(), name="zafra_update"),
    path('inventory/zafra/add',ZafraCreateView.as_view(), name="zafra_create"),
    path('inventory/zafra', ZafraListView.as_view(), name="zafra_list"),
    # lote
    path('inventory/lote/<int:pk>/delete',LoteDeleteView.as_view(), name="lote_delete"),
    path('inventory/lote/<int:pk>/update',LoteUpdateView.as_view(), name="lote_update"),
    path('inventory/lote/add',LoteCreateView.as_view(), name="lote_create"),
    path('inventory/lote', LoteListView.as_view(), name="lote_list"),
   # maquinaria agricola
    path('inventory/maquinaria_agricola/<int:pk>/delete',MaquinariaAgricolaDeleteView.as_view(), name="maquinaria_agricola_delete"),
    path('inventory/maquinaria_agricola/<int:pk>/update',MaquinariaAgricolaUpdateView.as_view(), name="maquinaria_agricola_update"),
    path('inventory/maquinaria_agricola/add',MaquinariaAgricolaCreateView.as_view(), name="maquinaria_agricola_create"),
    path('inventory/maquinaria_agricola', MaquinariaAgricolaListView.as_view(), name="maquinaria_agricola_list"),
    # calificacion agricola
    path('inventory/calificacion_agricola/<int:pk>/delete',CalificacionAgricolaDeleteView.as_view(), name="calificacion_agricola_delete"),
    path('inventory/calificacion_agricola/<int:pk>/update',CalificacionAgricolaUpdateView.as_view(), name="calificacion_agricola_update"),
    path('inventory/calificacion_agricola/add',CalificacionAgricolaCreateView.as_view(), name="calificacion_agricola_create"),
    path('inventory/calificacion_agricola', CalificacionAgricolaListView.as_view(), name="calificacion_agricola_list"),
    # plan actividad zafra
    path('inventory/plan_actividad_zafra/<int:pk>/update',PlanActividadZafraUpdateView.as_view(), name="plan_actividad_zafra_update"),
    path('inventory/plan_actividad_zafra/add',PlanActividadZafraCreateView.as_view(), name="plan_actividad_zafra_create"),
    path('inventory/plan_actividad_zafra', PlanActividadZafraListView.as_view(), name="plan_actividad_zafra_list"),
    # ACOPIO
    path('inventory/acopio/<int:pk>/update',AcopioUpdateView.as_view(), name="acopio_update"),
    path('inventory/acopio/add',AcopioCreateView.as_view(), name="acopio_create"),
    path('inventory/acopio', AcopioListView.as_view(), name="acopio_list"),
    path('inventory/acopio/<int:pk>/anular',AcopioAnularView.as_view(), name="acopio_anular"),
    # PEDIDO COMPRA
    path('inventory/pedido_compra/<int:pk>/update',PedidoCompraUpdateView.as_view(), name="pedido_compra_update"),
    path('inventory/pedido_compra/add',PedidoCompraCreateView.as_view(), name="pedido_compra_create"),
    path('inventory/pedido_compra', PedidoCompraListView.as_view(), name="pedido_compra_list"),
    # ORDEN COMPRA
    path('inventory/orden_compra/<int:pk>/update',OrdenCompraUpdateView.as_view(), name="orden_compra_update"),
    path('inventory/orden_compra/<int:pk>/anular',OrdenCompraAnularView.as_view(), name="orden_compra_anular"),
    path('inventory/orden_compra/add',OrdenCompraCreateView.as_view(), name="orden_compra_create"),
    path('inventory/orden_compra', OrdenCompraListView.as_view(), name="orden_compra_list"),
    # APERTURA CIERRE DE CAJA
    path('inventory/apertura_caja/<int:pk>/cerrar',AperturaCajaCerrarView.as_view(), name="apertura_caja_cerrar"),
    path('inventory/apertura_caja/add',AperturaCajaCreateView.as_view(), name="apertura_caja_create"),
    path('inventory/apertura_caja', AperturaCajaListView.as_view(), name="apertura_caja_list"),
    # arqueos
    path('inventory/arqueo/<int:pk>/delete',ArqueoDeleteView.as_view(), name="arqueo_delete"),
    path('inventory/arqueo/add',ArqueoCreateView.as_view(), name="arqueo_create"),
    path('inventory/arqueo', ArqueoListView.as_view(), name="arqueo_list"),
    # COMPRA
    path('inventory/compra/<int:pk>/anular',CompraAnularView .as_view(), name="compra_anular"),
    path('inventory/compra/add',CompraCreateView.as_view(), name="compra_create"),
    path('inventory/compra', CompraListView.as_view(), name="compra_list"),
    # AJUSTE STOCK
    path('inventory/ajuste_stock/<int:pk>/delete',AjusteStockDeleteView.as_view(), name="ajuste_stock_delete"),
    path('inventory/ajuste_stock/<int:pk>/update',AjusteStockUpdateView.as_view(), name="ajuste_stock_update"),
    path('inventory/ajuste_stock/add',AjusteStockCreateView.as_view(), name="ajuste_stock_create"),
    path('inventory/ajuste_stock', AjusteStockListView.as_view(), name="ajuste_stock_list"),
    # ACTIVIDAD AGRICOLA
    path('inventory/actividad_agricola/<int:pk>/anular',ActividadAgricolaAnularView .as_view(), name="actividad_agricola_anular"),
    path('inventory/actividad_agricola/add',ActividadAgricolaCreateView.as_view(), name="actividad_agricola_create"),
    path('inventory/actividad_agricola', ActividadAgricolaListView.as_view(), name="actividad_agricola_list"),
    # CONTRATO
    path('inventory/contrato/<int:pk>/delete',ContratoDeleteView.as_view(), name="contrato_delete"),
    path('inventory/contrato/add',ContratoCreateView.as_view(), name="contrato_create"),
    path('inventory/contrato', ContratoListView.as_view(), name="contrato_list"),
    # VENTA
    path('inventory/venta/<int:pk>/anular',VentaAnularView.as_view(), name="venta_anular"),
    path('inventory/venta/<int:pk>/descargar',download_view, name="venta_descargar"),
    path('inventory/venta/add',VentaCreateView.as_view(), name="venta_create"),
    path('inventory/venta', VentaListView.as_view(), name="venta_list"),
    # NOTA DE CREDITO RECIBIDA
    path('inventory/nota_credito_recibida/<int:pk>/anular',NotaCreditoRecibidaAnularView.as_view(), name="nota_credito_recibida_anular"),
    path('inventory/nota_credito_recibida/add',NotaCreditoRecibidaCreateView.as_view(), name="nota_credito_recibida_create"),
    path('inventory/nota_credito_recibida', NotaCreditoRecibidaListView.as_view(), name="nota_credito_recibida_list"),
    # NOTA DE CREDITO EMITIDA
    path('inventory/nota_credito_emitida/<int:pk>/anular',NotaCreditoEmitidaAnularView.as_view(), name="nota_credito_emitida_anular"),
    path('inventory/nota_credito_emitida/add',NotaCreditoEmitidaCreateView.as_view(), name="nota_credito_emitida_create"),
    path('inventory/nota_credito_emitida', NotaCreditoEmitidaListView.as_view(), name="nota_credito_emitida_list"),
    # TRANSFERENCIA CUENTA
    path('inventory/transferencia_cuenta/<int:pk>/anular',TransferenciaCuentaAnularView.as_view(), name="transferencia_cuenta_anular"),
    path('inventory/transferencia_cuenta/add',TransferenciaCuentaCreateView.as_view(), name="transferencia_cuenta_create"),
    path('inventory/transferencia_cuenta', TransferenciaCuentaListView.as_view(), name="transferencia_cuenta_list"),
    # LIBRO DE COMPRA 
    path('inventory/libro_compra', LibroCompraListView.as_view(), name="libro_compra_list"),
    # LIBRO DE COMPRA 
    path('inventory/libro_venta', LibroVentaListView.as_view(), name="libro_venta_list"),
    # INFORME DE COMPRA 
    path('inventory/compra_informe', CompraInformeListView.as_view(), name="compra_informe_list"),
    # INFORME DE VENTA 
    path('inventory/venta_informe', VentaInformeListView.as_view(), name="venta_informe_list"),
    # PRODUCCION AGRICOLA
    path('inventory/produccion_agricola_informe', ProduccionAgricolaInformeListView.as_view(), name="produccion_agricola_informe_list"),
    # INVENTARIO DEPOSITO
    path('inventory/c', InventarioDepositoInformeListView.as_view(), name="inventario_deposito_list"),
    # USUARIO
    path("accounts/password_change/done", CustomPasswordChangeDoneView.as_view(), name="password_change_done"),
    path("accounts/password_change/", CustomPasswordChangeView.as_view(), name="password_change"),
    path('accounts/users/<int:pk>/delete', UserDeleteView.as_view(), name="user_remove"),
    path('accounts/users/<int:pk>/update', UserUpdateView.as_view(), name="user_update"),
    path("accounts/users/add", UserCreateView.as_view(), name="user_create"),
    path("accounts/users", UserListView.as_view(), name="user_list"),
    path("accounts/", include("django.contrib.auth.urls")),
    # COBRO
    path('inventory/cobro/<int:pk>/anular',CobroAnularView.as_view(), name="cobro_anular"),
    path('inventory/cobro/add',CobroCreateView.as_view(), name="cobro_create"),
    path('inventory/cobro/seleccionar-persona', PersonaSelectionListView.as_view(), name="cobro_persona_selecction_list"),
    path('inventory/cobro', CobroListView.as_view(), name="cobro_list"),
    # LIQUIDACION AGRICOLA
    path('inventory/liquidacion_agricola/<int:pk>/anular',LiquidacionAgricolaAnularView.as_view(), name="liquidacion_agricola_anular"),
    path('inventory/liquidacion_agricola/add',LiquidacionAgricolaCreateView.as_view(), name="liquidacion_agricola_create"),
    path('inventory/liquidacion_agricola/selection',LiquidacionAgricolaSelectionView.as_view(), name="liquidacion_agricola_select"),
    path('inventory/liquidacion_agricola', LiquidacionAgricolaListView.as_view(), name="liquidacion_agricola_list"),
    # NOTA DE DEBITO RECIBIDA
    path('inventory/nota_debito_recibida/<int:pk>/anular',NotaDebitoRecibidaAnularView.as_view(), name="nota_debito_recibida_anular"),
    path('inventory/nota_debito_recibida/add',NotaDebitoRecibidaCreateView.as_view(), name="nota_debito_recibida_create"),
    path('inventory/nota_debito_recibida', NotaDebitoRecibidaListView.as_view(), name="nota_debito_recibida_list"),
    # NOTA DE DEBITO EMITIDA
    path('inventory/nota_debito_emitida/<int:pk>/anular',NotaDebitoEmitidaAnularView.as_view(), name="nota_debito_emitida_anular"),
    path('inventory/nota_debito_emitida/add',NotaDebitoEmitidaCreateView.as_view(), name="nota_debito_emitida_create"),
    path('inventory/nota_debito_emitida', NotaDebitoEmitidaListView.as_view(), name="nota_debito_emitida_list"),
     # CIERRE ZAFRA
    path('inventory/cierre_zafra/<int:pk>/anular',CierreZafraDeleteView.as_view(), name="cierre_zafra_delete"),
    path('inventory/cierre_zafra/add',CierreZafraCreateView.as_view(), name="cierre_zafra_create"),
    path('inventory/cierre_zafra', CierreZafraListView.as_view(), name="cierre_zafra_list"),
    path('inventory/cierre_zafra/selection',CierreZafraSelectionView.as_view(), name="cierre_zafra_select"),
    # menu tonto
    path('inventory/', menu, name="inventory_menu"),
    path('admin/', admin.site.urls),
    # documentation
    url(r'^docs/', include('inventory.documentation.urls', namespace='documentation')),
    path('', main, name="main"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
