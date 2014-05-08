from django.views.generic import DetailView, TemplateView
from tt_dataviews.views import base

from . import models


class EmployeeView(DetailView):
    template_name = 'tx_salaries/employee.html'
    queryset = (models.Employee.objects.all()
                .select_related('position__person', 'compensation_type',
                                'position__organization__parent', 'title',)
                .prefetch_related('position__person__races'))
    context_object_name = 'employee'


    def get_context_data(self, **kwargs):
        context = super(EmployeeView, self).get_context_data(**kwargs)
        context['highest_salaries_in_department'] = (
                self.get_queryset().filter(
                            position__post__organization=context['employee'].position.post.organization)
                            .order_by('-compensation')[:5])
        context['highest_salaries_peers'] = (
            self.get_queryset().filter(
                position__post=context['employee'].position.post)
                .order_by('-compensation')[:5])

        return context


class OrganizationView(DetailView):
    template_name = 'tx_salaries/organization.html'
    model = models.Organization
    queryset = (models.Organization.objects
                .select_related('parent__name',
                                'stats__median_paid__compensation',
                                'stats__male__distribution__slices',
                                'stats__female__distribution__slices',
                                'stats__male__median_paid___compensation',
                                'stats__female__median_paid__compensation',
                                'stats__time_employed'))
    context_object_name = 'org'

    def get_top_salaries(self):
        return (models.Employee.objects
                .filter(position__post__organization__pk=self.kwargs['pk'])
                .select_related('position__person', 'position__organization',
                                'position__stats__median_paid__compensation',
                                'title__name')
                .order_by('-compensation')[:10])

    def get_top_jobs(self):
        return (models.PositionStats.objects
                .filter(position__organization__pk=self.kwargs['pk'])
                .select_related('position__label', 'median_paid__compensation')
                .order_by('-median_paid__compensation')[:10])

    def get_context_data(self, **kwargs):
        context = super(OrganizationView, self).get_context_data(**kwargs)
        context['top_salaries'] = self.get_top_salaries()
        context['top_jobs'] = self.get_top_jobs()
        return context


class PositionView(DetailView):
    template_name = 'tx_salaries/position.html'
    model = models.Post
    queryset = (models.Post.objects
                .select_related('stats__median_paid__compensation',
                                'stats__female__total_number',
                                'stats__male__total_number',
                                'organization__parent__name'))
    context_object_name = 'position'

    def get_top_salaries(self):
        return (models.Employee.objects.filter(position__post=self.kwargs['pk'])
                .select_related('position__person', 'position__organization',
                                'position__stats__median_paid__compensation')
                .order_by('-compensation')[:10]
                .select_related('title'))

    def get_context_data(self, **kwargs):
        context = super(PositionView, self).get_context_data(**kwargs)
        context['top_salaries'] = self.get_top_salaries()
        return context


class LandingView(base.LandingView):
    app_title = "Government Employee Salaries"
    app_tagline = "FOIA-ing all the things"
    data_app_name = "tx_salaries"

    def get_top_salaries(self, **kwargs):
        return (models.Employee.objects.all()
                .select_related('position__person', 'position__organization',
                                'title__name')
                .order_by('-compensation')[:10])

    def get_recent_orgs(self, **kwargs):
        return (models.Organization.objects.all()
                .select_related('stats__median_paid__compensation')
                .order_by('-updated_at')[:10])

    def get_context_data(self, **kwargs):
        context = super(LandingView, self).get_context_data(**kwargs)
        context['org_count'] = models.Organization.objects.count()
        context['employee_count'] = models.Employee.objects.count()
        context['top_salaries'] = self.get_top_salaries()
        context['recent_orgs'] = self.get_recent_orgs()
        return context
