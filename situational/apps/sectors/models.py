from django.db import models

from jsonfield import JSONField
from model_utils.models import TimeStampedModel
from templated_email import send_templated_email

import template_to_pdf


class SectorsReport(TimeStampedModel):
    soc_codes = models.CharField(
        blank=False, null=False, unique=True, max_length=200)
    soc_code_data = JSONField()

    RESULT_FIELDS = (
        'soc_code_data',
    )

    def to_pdf(self):
        template = template_to_pdf.Template('sectors/print.html')
        return template.render({'report': self})

    def send_to(self, email):
        subject = "What sort of jobs you could do"
        send_templated_email(
            "sectors/email",
            {"report": self},
            to=[email],
            subject=subject
        )

    @property
    def is_populated(self):
        return all(
            self._is_result_field_populated(f) for f in self.RESULT_FIELDS
        )

    def _is_result_field_populated(self, field):
        return getattr(self, field) != ''
