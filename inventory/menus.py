from django.urls import reverse_lazy
from menu import Menu, MenuItem

# Agregamos los menus al principal
Menu.add_item("main", MenuItem("Inicio",
                               reverse_lazy("main")))

Menu.add_item("main", MenuItem("Usuarios",
                               reverse_lazy("user_list")))

Menu.add_item("main", MenuItem("Items",
                               reverse_lazy("item_list")))

Menu.add_item("main", MenuItem("Personas",
                               reverse_lazy("persona_list")))
                               

hijos_referenciales_agricultura = (
    MenuItem("Calificaciones Agrícolas",reverse_lazy("calificacion_agricola_list")),
    MenuItem("Actividades Agrícolas Tipos",reverse_lazy("tipo_actividad_agricola_list")),
    MenuItem("Máquinarias Agrícolas Tipos", reverse_lazy("tipo_maquinaria_agricola_list")),
    MenuItem("Máquinarias Agrícolas",reverse_lazy("maquinaria_agricola_list")),
    MenuItem("Fincas",reverse_lazy("finca_list")),
    MenuItem("Zafras", reverse_lazy("zafra_list")),
    MenuItem("Lotes",reverse_lazy("lote_list"))
)

hijos_referenciales_gestion = (
    MenuItem("Categorias",reverse_lazy("categoria_list")),
    MenuItem("Marcas",reverse_lazy("marca_list")),
    MenuItem("Tipos de Impuestos",reverse_lazy("tipo_impuesto_list")),
    MenuItem("Bancos",reverse_lazy("banco_list")),
    MenuItem("Depósitos",reverse_lazy("deposito_list")),
    MenuItem("Cuentas",reverse_lazy("cuenta_list")),
)


hijos_movimiento_agricultura = (
    MenuItem("Plan de Actividades Zafras",reverse_lazy("plan_actividad_zafra_list")),
    MenuItem("Acopios",reverse_lazy("acopio_list")),
    MenuItem("Actividades Agrícolas",reverse_lazy("actividad_agricola_list")),
    MenuItem("Contratos",reverse_lazy("contrato_list")),
)

hijos_movimiento_compra = (
    MenuItem("Pedidos de Compras",reverse_lazy("pedido_compra_list")),
    MenuItem("Ordenes de Compras",reverse_lazy("orden_compra_list")),
    MenuItem("Compras",reverse_lazy("compra_list")),
    MenuItem("Ajustes Stock",reverse_lazy("ajuste_stock_list")),
    MenuItem("Notas de Créditos Recibidas",reverse_lazy("nota_credito_recibida_list")),
    MenuItem("Libro de Compras",reverse_lazy("libro_compra_list")),
    MenuItem("Inventario por Deposito",reverse_lazy("inventario_deposito_list")),
)

hijos_movimiento_venta = (
    MenuItem("Apertura/Cierre Cajas",reverse_lazy("apertura_caja_list")),
    MenuItem("Arqueos",reverse_lazy("arqueo_list")),
    MenuItem("Ventas",reverse_lazy("venta_list")),
    MenuItem("Notas de Créditos Emitidas",reverse_lazy("nota_credito_emitida_list")),
    MenuItem("Transferencia entre Cuentas",reverse_lazy("transferencia_cuenta_list")),
    MenuItem("Libro de Ventas",reverse_lazy("libro_venta_list")),
)

hijos_informes = (
    MenuItem("Compra Informe",reverse_lazy("compra_informe_list")),
    MenuItem("Venta Informe",reverse_lazy("venta_informe_list")),
    MenuItem("Producción Agrícola Informe",reverse_lazy("produccion_agricola_informe_list")),
)


Menu.add_item("referencial_agricultura", MenuItem("Referenciales Agricultura",
                            reverse_lazy("inventory_menu"),
                            children = hijos_referenciales_agricultura))

Menu.add_item("referencial_gestion", MenuItem("Referenciales Gestión",
                            reverse_lazy("inventory_menu"),
                            children = hijos_referenciales_gestion))

Menu.add_item("movimientos_agricultura", MenuItem("Movimientos Agricultura",
                            reverse_lazy("inventory_menu"),
                            children = hijos_movimiento_agricultura))

Menu.add_item("movimientos_compras", MenuItem("Movimientos Compras",
                            reverse_lazy("inventory_menu"),
                            children = hijos_movimiento_compra))

Menu.add_item("movimientos_ventas", MenuItem("Movimientos Ventas",
                            reverse_lazy("inventory_menu"),
                            children = hijos_movimiento_venta))
Menu.add_item("informes", MenuItem("Informes",
                            reverse_lazy("inventory_menu"),
                            children = hijos_informes))










