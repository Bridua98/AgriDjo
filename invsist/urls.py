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
from django.urls import path

# importando vistas
from inventory.views import AcopioCreateView, AcopioListView, AcopioUpdateView, BancoCreateView, BancoDeleteView, BancoListView, BancoUpdateView, CalificacionAgricolaCreateView, CalificacionAgricolaDeleteView, CalificacionAgricolaListView, CalificacionAgricolaUpdateView, CategoriaCreateView, CategoriaDeleteView, CategoriaListView, CategoriaUpdateView, CuentaCreateView, CuentaDeleteView, CuentaListView, CuentaUpdateView, DepositoCreateView, DepositoDeleteView, DepositoListView, DepositoUpdateView, ItemCreateView, LoteCreateView, LoteDeleteView, LoteListView, LoteUpdateView, MaquinariaAgricolaCreateView, MaquinariaAgricolaDeleteView, MaquinariaAgricolaListView, MaquinariaAgricolaUpdateView, PedidoCompraCreateView, PedidoCompraListView, PedidoCompraUpdateView, PersonaCreateView, PersonaDeleteView, PersonaListView, PersonaUpdateView, PlanActividadZafraCreateView, PlanActividadZafraListView, PlanActividadZafraUpdateView, TipoImpuestoCreateView, TipoImpuestoDeleteView, TipoImpuestoListView, TipoImpuestoUpdateView, ZafraCreateView, ZafraDeleteView, ZafraListView, ZafraUpdateView
from inventory.views import MarcaCreateView, MarcaDeleteView, MarcaListView, MarcaUpdateView
from inventory.views import TipoMaquinariaAgricolaCreateView, TipoMaquinariaAgricolaDeleteView, TipoMaquinariaAgricolaListView, TipoMaquinariaAgricolaUpdateView
from inventory.views import ItemDeleteView, ItemListView, ItemUpdateView
from inventory.views import TipoActividadAgricolaListView, TipoActividadAgricolaCreateView, TipoActividadAgricolaUpdateView, TipoActividadAgricolaDeleteView
from inventory.views import FincaListView, FincaCreateView, FincaUpdateView, FincaDeleteView
from inventory.views import main, menu

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
    # Acopio
    path('inventory/acopio/<int:pk>/update',AcopioUpdateView.as_view(), name="acopio_update"),
    path('inventory/acopio/add',AcopioCreateView.as_view(), name="acopio_create"),
    path('inventory/acopio', AcopioListView.as_view(), name="acopio_list"),
      # Acopio
    path('inventory/pedido_compra/<int:pk>/update',PedidoCompraUpdateView.as_view(), name="pedido_compra_update"),
    path('inventory/pedido_compra/add',PedidoCompraCreateView.as_view(), name="pedido_compra_create"),
    path('inventory/pedido_compra', PedidoCompraListView.as_view(), name="pedido_compra_list"),
    # menu tonto
    path('inventory/', menu, name="inventory_menu"),

    path('admin/', admin.site.urls),
    path('', main, name="main"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
