from django.urls import path
from . import views

app_name = "myapp"   
urlpatterns = [
    path("", views.HomeView.as_view(), name="homepage"),
    path("register", views.register_request, name="register"),
    path("login", views.login, name="login"),
    path('logout', views.logout, name = 'logout'),
    path("addmember", views.MemberCreateView.as_view(), name='addmember'),
    path("addcompany", views.CompanyCreateView.as_view(), name='addcompany'),
    path('addskill', views.MemberSkillView.as_view(), name='addskill'),
    path('addjob', views.JobCreateView.as_view(), name='addjob'),
    path('makeconnection', views.ConnectionCreateView.as_view(), name='makeconnection'),
    path('updateprofile', views.UpdateProfileView.as_view(), name='updateprofile'),
    path('updatecompany', views.UpdateCompanyView.as_view(), name='updatecompany'),
    path('addeducation', views.EducationCreateView.as_view(), name='addeducation'),
    path('confirmconnection', views.ConnectionConfirmView.as_view(), name='confirmconnection'),
    path('connected/<int:connection_id>', views.connect, name='connected'),
    path('endorseskill/<int:member_id>', views.EndorsementView.as_view(), name='endorseskill'),
    path('viewconnections', views.DisplayConnections.as_view(), name='viewconnections')
]
