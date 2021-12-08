import calculation
from layout import CancelButton, DeleteButton, Formset
from widgets import DateInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (HTML, Button, ButtonHolder, Column, Div, Fieldset,
                                 Layout, Row, Submit, Field)
from django import forms
from django.db.models import fields

from .models import PlanActividadZafra, PlanActividadZafraDetalle


class PlanActividadZafraForm(forms.ModelForm):
    total = forms.DecimalField(
        widget=calculation.SumInput('costo',   attrs={'readonly':True}),
    )
    class Meta:
        model = PlanActividadZafra
        fields = ['fecha', 'zafra', 'observacion']
        widgets = {'fecha':DateInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.fields['total'].label = False
        self.helper.layout = Layout(
            Column("date"),
            "zafra",
            "observacion",
            Fieldset(
                u'Artículos',
                Formset(
                    "PlanActividadZafraDetalleInline"
                )
            ),
            Row(
                Column(HTML("<div class='w-100'></div>")), Column(HTML('<span class="w-100"> Total: </span>'), css_class="text-right"), Column("total")
            ), 
            Row(
                Div(Submit("submit", "Guardar"), HTML("""<a class="btn btn-secondary" href="{% url 'order_list' %}"> Cancelar</a>""" ))
            ) 
        )

class PlanActividadZafraDetalleForm(forms.ModelForm):
    class Meta:
        model = PlanActividadZafraDetalle
        fields = ['fechaActividad', 'finca', 'tipoActividadAgricola', 'descripcion','costo']
        widgets = { 'fechaActividad':DateInput }