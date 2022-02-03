import json 
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'

    def __init__(self, attrs=None, format=None):
        super().__init__(attrs, format='%Y-%m-%d' if format is None else format)

class MaskInputMixin:
    mask = {}
    class Media:
        js = [
            'site/js/mask.js',
            'site/js/inputmask.min.js',
        ]
    def __init__(self, *args, **kwargs):
        mask = kwargs.pop('mask', None)
        
        attrs = kwargs.get('attrs', {})
        if attrs is None: attrs={}
        kwargs['attrs'] = attrs
        super().__init__(*args, **kwargs)
        if mask:
            self.mask.update(mask)

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs['data-inputmask'] = json.dumps(self.mask).replace('{', '').replace('}', '')
        rendered = super().render(name, value, attrs=attrs, renderer=None)
        return rendered

    def format_value(self, value):
        """
        Return a value as it should appear when rendered in a template.
        """
        if value == '' or value is None:
            return None
        return str(value)

class MaskInput(MaskInputMixin, forms.TextInput ):
    """ MaskInput """


class InvoiceMaskInput(MaskInputMixin, forms.TextInput):
    mask = {
        'mask': '999-999-9999999'
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DecimalMaskInput(MaskInputMixin, forms.TextInput):
    mask = {
        'alias': 'decimal',
        'autoUnmask': True,
        'unmaskAsNumber': True,
        'clearMaskOnLostFocus': False
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attrs['inputmode'] = 'decimal'
        self.attrs['style'] =  self.attrs.get('style', '')+'text-align:right;'
