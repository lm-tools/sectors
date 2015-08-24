from django import forms


class HistoryDetailsForm(forms.Form):
    CIRCUMSTANCE_CHOICES = [
        ("full_time", "Full time"),
        ("part_time", "Part time"),
        ("work_programme", "Work programme"),
        ("unemployed", "Unemployed"),
        ("sick", "Off sick"),
        ("training", "In full time training"),
        ("caring", "Caring full time for others"),
        ("none", "None of these"),
    ]
    circumstances = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=CIRCUMSTANCE_CHOICES
    )
    #TODO: date widget with year and month dropdown
    #TODO: different copies for the description label
    description = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(HistoryDetailsForm, self).clean()
        # TODO: check since date is the past
        return cleaned_data
