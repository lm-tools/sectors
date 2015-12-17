from django import http
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import FormView, View

from formtools.wizard.views import NamedUrlCookieWizardView

from . import forms, helpers, models


class SectorWizardView(NamedUrlCookieWizardView):
    TEMPLATES = {
        'sector_form': 'sectors/sector_form.html',
        'job_descriptions_form': 'sectors/job_descriptions.html',
    }

    def get(self, *args, **kwargs):
        if self.request.path == reverse('sectors:start'):
            self.storage.reset()
        return super().get(*args, **kwargs)

    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    def get_form_kwargs(self, step):
        kwargs = {}
        if step == 'job_descriptions_form':
            sectors = self.get_cleaned_data_for_step('sector_form')['sector']
            kwargs['keywords'] = sectors
        return kwargs

    def done(self, form_list, form_dict, **kwargs):
        discriptions_key = 'job_descriptions_form'
        description_form_data = \
            self.storage.get_step_data(discriptions_key)
        soc_codes = []
        for k, v in description_form_data.items():
            if k.startswith(discriptions_key) and '-' in k:
                soc_codes.append(k.split('-')[1])
        soc_codes_string = ','.join(soc_codes)
        report, _created = models.SectorsReport.objects.get_or_create(
            soc_codes=soc_codes_string)
        url = reverse("sectors:report", kwargs={'report_id': report.pk})
        return HttpResponseRedirect(url)


class ReportView(FormView):
    template_name = "sectors/report.html"
    form_class = forms.EmailForm
    success_url = "#success"

    def get(self, request, *args, **kwargs):
        self.report = get_object_or_404(
            models.SectorsReport,
            pk=int(kwargs['report_id'])
        )

        if not self.report.is_populated:
            soc_codes_list = self.report.soc_codes.split(",")
            lmi_client = helpers.LMIForAllClient()
            soc_code_data = {}
            for soc_code in soc_codes_list:
                soc_code_int = int(soc_code)
                soc_code_data[soc_code_int] = {
                    'pay': lmi_client.pay(soc_code_int),
                    'hours_worked': lmi_client.hours_worked(soc_code_int),
                    'info': lmi_client.soc_code_info(soc_code_int)
                }
            self.report.soc_code_data = soc_code_data
            self.report.save(update_fields=['soc_code_data'])

        status_code = 200
        self.template_name = "sectors/report.html"
        response = super().get(request, *args, **kwargs)
        response.status_code = status_code

        return response

    def get_context_data(self, **kwargs):
        context = kwargs
        report = models.SectorsReport.objects.get(pk=self.kwargs['report_id'])
        context['report'] = report
        context['report_id'] = report.pk
        return context

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        report = models.SectorsReport.objects.get(pk=self.kwargs['report_id'])
        report.send_to(email)
        notice = "Sent to " + email
        messages.success(self.request, notice)
        return super(ReportView, self).form_valid(form)


class IsPopulatedView(View):
    def get(self, request, *args, **kwargs):
        report = get_object_or_404(
            models.SectorsReport,
            pk=int(kwargs['report_id'])
        )
        return http.JsonResponse(
            report.is_populated,
            safe=False
        )


class PDFView(View):
    def get(self, request, *args, **kwargs):
        report = get_object_or_404(
            models.SectorsReport,
            pk=int(kwargs['report_id'])
        )
        response = http.HttpResponse(report.to_pdf(), 'application/pdf')
        response['Content-Disposition'] = "filename=sectors-report.pdf"
        return response


def server_error(request, template_name='500.html'):
    context_instance = RequestContext(request)
    context_instance['start_url'] = '/'

    return render_to_response(
        template_name,
        context_instance=context_instance
    )
