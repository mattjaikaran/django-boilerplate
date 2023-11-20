"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from core.views import RegisterView, UserViewSet, LogoutView
from todos.views import TodoViewSet
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

# Admin Panel text
admin.site.site_header = "Django Admin Panel"
admin.site.site_title = "Django Boilerplate Admin Panel"
admin.site.index_title = "Welcome to Django Boilerplate Admin Panel"

router = routers.SimpleRouter()

router.register(r"users/", UserViewSet)
router.register(r"todos/", TodoViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    # auth
    path("api/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/register/", RegisterView.as_view(), name="sign_up"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    # swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

# urlpatterns += router.urls
# this adds the prefix api/ all urls registered via router.register
# ie: url/api/todos/
urlpatterns += (path("api/", include(router.urls)),)
