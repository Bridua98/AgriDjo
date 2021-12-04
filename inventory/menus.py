from django.urls import reverse_lazy
from menu import Menu, MenuItem

# Agregamos los menus al principal
Menu.add_item("main", MenuItem("Inicio",
                               reverse_lazy("main")))

hijos_referenciales = (
    MenuItem("Categorias",reverse_lazy("categoria_list")),
    MenuItem("Marcas",reverse_lazy("marca_list")),
    MenuItem("Tipos de Impuestos",reverse_lazy("tipo_impuesto_list")),
    MenuItem("Actividades Agrícolas Tipos",reverse_lazy("tipo_actividad_agricola_list")),
    MenuItem("Máquinarias Agrícolas Tipos", reverse_lazy("tipo_maquinaria_agricola_list")),
    MenuItem("Fincas",reverse_lazy("finca_list")),
    MenuItem("Zafras", reverse_lazy("zafra_list")),
    MenuItem("Lotes",reverse_lazy("lote_list")),
)

Menu.add_item("referenciales", MenuItem("Referenciales",
                             reverse_lazy("inventory_menu"),
                             children= hijos_referenciales))

Menu.add_item("main", MenuItem("Items",
                               reverse_lazy("item_list")))










