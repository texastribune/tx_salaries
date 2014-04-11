from django.views.generic import TemplateView
from tt_dataviews.views import base

from . import models


class EmployeeView(TemplateView):
    template_name = 'tx_salaries/employee.html'

    def get_context_data(self, **kwargs):
        context = super(EmployeeView, self).get_context_data(**kwargs)
        p = models.Employee.objects.get(id=self.kwargs['employee_id'])
        context['employee'] = {
            'name': p.position.person.name,
            'title': p.title.name,
            'department': p.position.organization.name,
            'agency': p.position.organization.parent.name,
            'gender': p.position.person.gender,
            'hire_date': p.hire_date,
            'salary': p.compensation,
            'ft': p.compensation_type
        }
        return context


class OrganizationView(TemplateView):
    template_name = 'tx_salaries/organization.html'

    def get_context_data(self, **kwargs):
        context = super(OrganizationView, self).get_context_data(**kwargs)
        o = models.Organization.objects.get(id=self.kwargs['org_id'])
        context['org'] = {
            'name': o.name,
            'emp_count': o.members.count(),
            'agency': o.parent.name,
            'stats': o.stats,
            'updated': u"{0}/{1}/{2}".format(o.updated_at.month,
                                            o.updated_at.day, o.updated_at.year)
        }
        return context


class LandingView(base.LandingView):
    app_title = "Government Employee Salaries"
    app_tagline = "FOIA-ing all the things"
    data_app_name = "tx_salaries"

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        context['orgs'] = [o for o in models.Organization.objects.all()]
        return context
