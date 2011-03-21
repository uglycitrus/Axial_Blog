import os
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('myproject.blog.views',
	url(r'^accounts/login/$', 'login_view', name = 'login'),
 	url(r'^accounts/logout/$', 'logout_view', name = 'logout'),
 	url(r'^posts/new/$', 'new_post', name = 'new_post'),
 	url(r'^posts/edit/$', 'edit_posts', name = 'edit_posts'),
 	url(r'^posts/edit/(?P<post_slug>[-\w]+)', 'post_edit', name = 'post_edit'),
 	url(r'^posts/view/(?P<post_slug>[-\w]+)', 'post_view', name = 'post_view'),
 	url(r'^posts/$', 'all_posts', name = 'all_posts'),
 	url(r'^posts/(?P<tag_slug>[-\w]+)', 'post_list', name = 'post_list'),
 	url(r'^$', 'all_posts', name = 'all_posts'),
	# Example:
	# (r'^axial_blog/', include('axial_blog.foo.urls')),

	# Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
	# to INSTALLED_APPS to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),
	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.split(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])[0]+'/static_media'}),
    )

