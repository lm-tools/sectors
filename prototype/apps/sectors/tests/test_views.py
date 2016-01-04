from unittest.mock import patch, PropertyMock

from django.core.urlresolvers import reverse

from sectors import models
from prototype.testing import BaseCase


class TestShowView(BaseCase):

    def test_get_with_populated_report(self):
        report = models.SectorsReport.objects.create(soc_codes='3114,5330')
        with patch('sectors.models.SectorsReport.is_populated',
                   new_callable=PropertyMock) as mock_is_populated:
            mock_is_populated.return_value = True

            response = self.client.get(
                reverse(
                    'sectors:report',
                    kwargs={
                        'report_id': report.pk
                    }
                )
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "sectors/report.html")


class TestSendReport(BaseCase):
    def test_post(self):
        report = models.SectorsReport.objects.create(soc_codes='3114,5330')
        with patch('sectors.models.SectorsReport.send_to') as send_to:
            with patch('sectors.models.SectorsReport.is_populated',
                       new_callable=PropertyMock) as mock_is_populated:
                mock_is_populated.return_value = True
                response = self.client.post(
                    reverse(
                        'sectors:report',
                        kwargs={
                            'report_id': report.pk
                        }
                    ),
                    data={'email': 'test@example.org'},
                    follow=True
                )
                send_to.assert_called_with('test@example.org')
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, 'sectors/report.html')
            self.assertEqual(int(response.context['report_id']), report.pk)
            self.assertContains(response, 'test@example.org')
