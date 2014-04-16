from django.views.generic import TemplateView
from tt_dataviews.views import base

from . import models


class EmployeeView(TemplateView):
    template_name = 'tx_salaries/employee.html'

    gender_map = {'M': 'Male', 'F': 'Female'}

    def get_top_peers(self, employee):
        return (models.Employee.objects
                                .filter(position__post=employee.position.post)
                                .order_by('-compensation')[:5])

    def get_top_dept(self, employee):
        return (models.Employee.objects
                                .filter(position__post__organization=employee.position.post.organization)
                                .order_by('-compensation')[:5])

    def get_context_data(self, **kwargs):
        context = super(EmployeeView, self).get_context_data(**kwargs)
        p = models.Employee.objects.get(id=self.kwargs['employee_id'])
        context['employee'] = {
            'name': p.position.person.name,
            'title': p.title.name,
            'department': p.position.organization.name,
            'agency': p.position.organization.parent.name,
            'gender': self.gender_map[p.position.person.gender],
            'hire_date': p.hire_date,
            'salary': p.compensation,
            'ft': p.compensation_type,
        }
        context['peers'] = self.get_top_peers(p)
        context['top_dept'] = self.get_top_dept(p)
        return context


class OrganizationView(TemplateView):
    template_name = 'tx_salaries/organization.html'

    def get_top_salaries(self, org):
        return (models.Employee.objects
                                .filter(position__post__organization=org)
                                .order_by('-compensation')[:10])

    def get_top_jobs(self, org):
        return (models.PositionStats.objects.filter(position__organization=org)
                                            .order_by('-median_paid__compensation')
                                            [:10])

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
        context['top_salaries'] = self.get_top_salaries(o)
        context['top_jobs'] = self.get_top_jobs(o)
        return context


class LandingView(base.LandingView):
    app_title = "Government Employee Salaries"
    app_tagline = "FOIA-ing all the things"
    data_app_name = "tx_salaries"

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        context['orgs'] = [o for o in models.Organization.objects.all()]
        return context
