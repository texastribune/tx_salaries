from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.LandingView.as_view(), name='landing'),
    url(r'employee/(?P<employee_id>[^/]+)/$', views.EmployeeView.as_view(), name='employee'),
    url(r'org/(?P<org_id>[^/]+)$', views.OrganizationView.as_view(), name='organization')
)
