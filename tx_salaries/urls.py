from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.LandingView.as_view(), name='landing'),
    url(r'employee/(?P<employee_id>[^/]+)/$', views.EmployeeView.as_view(), name='employee'),
    url(r'org/(?P<org_id>[^/]+)$', views.OrganizationView.as_view(), name='organization')
)


# urlpatterns = patterns('dataapps.payroll.views',
#     url(r'^$', 'index', name='payroll_index'),
#     url(r'^search/$', 'search', name='payroll_search'),
#     url(r'^search/(?P<kind>\w+)/$', 'search', name='payroll_search_kind'),
#     url(r'^agencies/$', 'entity_index', name='payroll_entity_index'),
#     url(r'^titles/$', 'title_index', name='payroll_title_index'),
#     url(r'^titles/(?P<slug>[-\w]*)/(?P<id>\d+)/$', 'title', name='payroll_title'),
#     url(r'^titles/(?P<id>\d+)/$', 'title', name='payroll_title_by_id'),
#     url(r'^(?P<slug>[-\w]+)/$', 'entity', name='payroll_entity'),
#     url(r'^(?P<entity_slug>[-\w]+)/departments/$', 'department_index', name='payroll_department_index'),
#     url(r'^(?P<entity_slug>[-\w]+)/departments/(?P<department_slug>[-\w]*)/(?P<id>\d+)/$', 'department', name='payroll_department'),
#     url(r'^(?P<entity_slug>[-\w]+)/departments/(?P<id>\d+)/$', 'department', name='payroll_department_by_id'),
#     url(r'^(?P<entity_slug>[-\w]+)/titles/$', 'entity_title_index', name='payroll_entity_titles_index'),
#     url(r'^(?P<entity_slug>[-\w]+)/titles/(?P<title_slug>[-\w]*)/(?P<id>\d+)/$', 'entity_title', name='payroll_entity_title'),
#     url(r'^(?P<entity_slug>[-\w]+)/titles/(?P<id>\d+)/$', 'entity_title', name='payroll_entity_title_by_id'),
#     url(r'^(?P<entity_slug>[-\w]+)/(?P<employee_slug>[-\w]*)/(?P<id>\d+)/$', 'employee', name='payroll_employee'),
# )
