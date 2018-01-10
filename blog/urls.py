from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),	
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
	url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
	url(r'^email/$',views.contact,name='email'),
	url(r'^rohitvermajaipur.wixsite.com/rohit/$',views.aboutme, name='ab_me'),
    url(r'^accounts/update/$', views.edit_user, name='account_update'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^password/$', views.change_password, name='change_password'),
]
