from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from common.views import HomeView, ProfileUpdateView, ProfileView, SignUpView, LoginViewManual

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Home URL
    path('', HomeView.as_view(), name='home'),

    # Profile URLs
    path('profile-update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/', ProfileView.as_view(), name='profile'),

    # Authentication URLs
    path('register/', SignUpView.as_view(), name="register"),
    path('accounts/login/', LoginViewManual.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # Password Change and Reset related URLs
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='common/change-password.html', success_url='/'),
        name='change-password'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='common/password-reset/password_reset.html',
         ), name='password_reset'),

    path('password-reset-sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='common/password-reset/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='common/password-reset/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='common/password-reset/password_reset_complete.html'),
         name='password_reset_complete'),

    # Social Media Related URLs
    path('accounts/', include('allauth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)