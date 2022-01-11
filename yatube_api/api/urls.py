from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from api.views import CommentViewSet, GroupViewSet, PostViewSet

app_name = 'api_v1'

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'posts/(?P<post_id>[\d]+)/comments', CommentViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
