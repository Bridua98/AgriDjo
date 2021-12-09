from django.urls import reverse_lazy
from menu import Menu, MenuItem

# Agregamos los menus al principal
Menu.add_item("main", MenuItem("Inicio",
                               reverse_lazy("main")))

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
)

Menu.add_item("referencial_agricultura", MenuItem("Referenciales Agricultura",
                            reverse_lazy("inventory_menu"),
                            children = hijos_referenciales_agricultura))

Menu.add_item("referencial_gestion", MenuItem("Referenciales Gestión",
                            reverse_lazy("inventory_menu"),
                            children = hijos_referenciales_gestion))

Menu.add_item("movimientos_agricultura", MenuItem("Movimientos",
                            reverse_lazy("inventory_menu"),
                            children = hijos_movimiento_agricultura))


#hijos_referenciales= (
#    MenuItem("Gestión",reverse_lazy("inventory_menu"),children= hijos_referenciales_gestion),
#    MenuItem("Agricultura",reverse_lazy("inventory_menu"),children= hijos_referenciales_agricultura)
#)

#Menu.add_item("referenciales", MenuItem("Referenciales",
#                               reverse_lazy("inventory_menu"),
#                               children = hijos_referenciales
#                               ))












