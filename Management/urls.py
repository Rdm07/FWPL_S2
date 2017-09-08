
from django.conf.urls import url
# from django.contrib import admin
from Management import views

urlpatterns = [
	url(r'^login/$', views.Login.as_view(), name='login'),
	url(r'^logout/$', views.Logout.as_view(), name='logout'),
	url(r'^register/$', views.Register.as_view(), name='register'),
	url(r'^home/$', views.Home.as_view(), name='home'),
	url(r'^register-confirm/$', views.RegisterConfirm.as_view(), name='register-confirm'),
	url(r'^matchdays/(?P<pk>\d+)/$', views.Matchdays.as_view(), name='matchdays'),
	url(r'^matchdays_user/(?P<pk1>\d+)/(?P<pk2>\d+)/$', views.MatchdaysUser.as_view(), name='matchdays_user'),
	url(r'^leaguetable/$', views.LeagueTable.as_view(), name='leaguetable'),
	url(r'^matchdayperformance/(?P<pk>\d+)/$', views.MatchdayPerformance.as_view(), name='matchdayperformance'),
	url(r'^submitanswer/(?P<pk>\d+)/$', views.SubmitAnswer.as_view(), name='submitanswer'),
	url(r'^updateanswer/(?P<pk>\d+)/$', views.UpdateAnswer.as_view(), name='updateanswer'),
]