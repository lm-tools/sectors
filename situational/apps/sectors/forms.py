from django import forms
from django.forms.forms import BoundField

from .helpers import LMIForAllClient
from .fields import MultiCharField


class FieldSet(object):
    """
    Taken from stackoverflow.com/questions/10366745/django-form-field-grouping

    Helper class to group BoundField objects together.
    """
    def __init__(self, form, fields, legend='', cls=None):
        self.form = form
        self.legend = legend
        self.fields = fields
        self.cls = cls

    def __iter__(self):
        for name in self.fields:
            field = self.form.fields[name]
            yield BoundField(self.form, field, name)


class NoColonForm(forms.Form):
    """
    Removes the default colons from form labels.
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)


class BaseLMIForm(NoColonForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lmi_client = LMIForAllClient()


class SectorForm(NoColonForm):
    SECTOR_INPUT_COUNT = 3

    sector = MultiCharField(
        count=SECTOR_INPUT_COUNT,
        label="Jobs you’re interested in",
        require_all_fields=False,
        error_messages={'required': 'Enter at least one job role', },
    )


class JobDescriptionsForm(BaseLMIForm):
    def __init__(self, *args, **kwargs):
        keywords = kwargs['keywords']
        del kwargs['keywords']
        super().__init__(*args, **kwargs)
        self.fieldsets = []
        self._add_fields_from_keywords(keywords)

    def _add_fields_from_keywords(self, keywords):
        for keyword in keywords:
            if keyword:
                soc_codes = []
                lmi_data = self.lmi_client.keyword_search(keyword)
                count = 6
                for item in lmi_data[:count]:
                    soc_code = str(item['soc'])
                    if soc_code not in soc_codes:
                        soc_codes.append(soc_code)
                        field = forms.BooleanField(
                            widget=forms.CheckboxInput,
                            label=item['title'],
                            help_text=item['description'],
                            required=False,
                        )
                        self.fields[soc_code] = field
                self.fieldsets.append(FieldSet(
                    self, list(soc_codes), keyword))

    def clean(self):
        cleaned_data = super().clean()
        if not any(cleaned_data.values()):
            raise forms.ValidationError(
                "Please select at least one job title",
                code='invalid'
            )
        return cleaned_data


class EmailForm(forms.Form):
    email = forms.EmailField(
        error_messages={
            'required': 'Please provide an email address.',
            'invalid': 'Please provide a valid email address.'
        },
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
