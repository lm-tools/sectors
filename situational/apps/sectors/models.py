from django.db import models
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import get_template

from jsonfield import JSONField
from model_utils.models import TimeStampedModel

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
        send_mail(
            subject,
            get_template("sectors/email.html").render(
                Context({"report": self})
            ),
            'work-in-progress@lm-tools.com',
            [email]
        )

    @property
    def is_populated(self):
        return all(
            self._is_result_field_populated(f) for f in self.RESULT_FIELDS
        )

    def _is_result_field_populated(self, field):
        return getattr(self, field) != ''
