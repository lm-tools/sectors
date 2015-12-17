from django.core import mail

from sectors.models import SectorsReport
from situational.testing import BaseCase


class SectorsReportBuilderMixin():

    SOC_TITLES = [
        'Construction and building trades supervisors',
        'Building and civil engineering technicians'
    ]

    def _populated_report(self, without=[]):
        populated_fields = {
            'soc_codes': '3114,5330',
            'soc_code_data': {
                '5330': {
                    'info': {
                        'title': self.SOC_TITLES[0]
                    }
                },
                '3114': {
                    'info': {
                        'title': self.SOC_TITLES[1]
                    }
                }
            }
        }
        for field in without:
            del populated_fields[field]
        return SectorsReport(**populated_fields)


class TestSectorsReportIsPopulated(SectorsReportBuilderMixin, BaseCase):
    def test_new_reports_are_considered_unpopulated(self):
        self.assertFalse(SectorsReport().is_populated)

    def test_reports_with_all_fields_present_are_considered_populated(self):
        self.assertTrue(self._populated_report().is_populated)

    def test_reports_with_missing_fields_are_considered_unpopulated(self):
        for field in (SectorsReport.RESULT_FIELDS):
            with self.subTest(field=field):
                report = self._populated_report(without=[field])
                self.assertFalse(report.is_populated)


class TestSectorsReportSendTo(SectorsReportBuilderMixin, BaseCase):
    def test_send_report_to_provided_mail_address(self):
        report = self._populated_report()
        report.send_to('test-address@example.org')

        self.assertEqual(len(mail.outbox), 1)  # sanity check
        message = mail.outbox[0]

        self.assertIn('test-address@example.org', message.to)
        self.assertIn("Here is your report.", message.body)
