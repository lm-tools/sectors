from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
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
        template_html = 'sectors/email.html'
        template_text = 'sectors/email.txt'
        exp = settings.DEFAULT_FROM_EMAIL,
        subject = 'What sort of jobs you could do'
        text = get_template(template_text)
        html = get_template(template_html)
        email_content = {"report": self}
        text_content = text.render(email_content)
        html_content = html.render(email_content)
        msg = EmailMultiAlternatives(subject, text_content, exp, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    @property
    def is_populated(self):
        return all(
            self._is_result_field_populated(f) for f in self.RESULT_FIELDS
        )

    def _is_result_field_populated(self, field):
        return getattr(self, field) != ''
