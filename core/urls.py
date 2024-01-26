from django.urls import include, path
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
from core.views import (
    ContactSupportViewSet,
    ForgotPasswordView,
    LogoutView,
    PasswordResetView,
    RegisterView,
    UserLoginView,
    UserViewSet,
)
from todos.views import TodoViewSet


from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from todos.views import TodoViewSet
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# from messaging.views import ConversationViewSet, MessageViewSet
# from notifications.views import NotificationViewSet

# from properties.views import PropertyViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()

# # Admin Panel text
admin.site.site_header = "Django Admin Panel"
admin.site.site_title = "Django Boilerplate Admin Panel"
admin.site.index_title = "Welcome to Django Boilerplate Admin Panel"

router.register(r"users", UserViewSet, basename="users")
router.register(r"contact-support", ContactSupportViewSet, basename="contact-support")
router.register(r"todos/", TodoViewSet)
# router.register(r"organizations", OrganizationViewSet, basename="organizations")
# router.register(r"teams", TeamViewSet, basename="teams")
# router.register(r"properties", PropertyViewSet, basename="properties")
# router.register(r"conversations", ConversationViewSet, basename="conversations")
# router.register(r"messaging", MessageViewSet, basename="messaging")
# router.register(r"notifications", NotificationViewSet, basename="notifications")

urlpatterns = [
    # auth
    path("api/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/login/", UserLoginView.as_view(), name="login"),
    path("api/register/", RegisterView.as_view(), name="sign_up"),
    path(
        "api/forgot-password/",
        ForgotPasswordView.as_view(),
        name="forgot_password",
    ),
    path("api/password-reset/", PasswordResetView.as_view(), name="password_reset"),
    path("api/logout/", LogoutView.as_view(), name="logout"),
    path("api/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    # swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # below adds api/ prefix to all routes in router
    # router.register
    path("api/", include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
