from django.conf.urls import url
from django.urls import path, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import *
from .forms import LoginForm

app_name = 'accounts'

urlpatterns = [
    
    ## Are registered

    path('validate_username', validate_username, name='validate_username'),    
    path('validate_email', validate_email, name='validate_email'),    

    # Manage Accounts

    path('@<username>', UserProfileView.as_view(), name='users'),

    path('account/edit', EditAccountView.as_view(), name='edit_account'),

    ######################################################################
    ## Authentication

    # Activate Account
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),

    # Log in with email or username
    path('accounts/login/', LoginView.as_view(), name='login', 
            kwargs={'authentication_form': LoginForm}),

    # Signup
    path('signup/', RegisterView.as_view(), name='signup'),

    # Logout
    path('logout/', LogoutView.as_view(), name='logout'),

    # Change password
    path('account/change_password/', 
            auth_views.PasswordChangeView.as_view(
            success_url = reverse_lazy("accounts:me")),
            name='password_change'
    ),

    # Password Reset
    path('password_reset/', 
            auth_views.PasswordResetView.as_view(
            success_url = reverse_lazy('accounts:password_reset_done')),
            name = 'password_reset'
    ),
    
    # Password Reset Done
    path('password_reset/done/', 
            auth_views.PasswordResetDoneView.as_view(),
            name = 'password_reset_done',
    ),
    
    # Password Reset Confirmation
    path('reset/<uidb64>/<token>/', 
            auth_views.PasswordResetConfirmView.as_view(
            success_url = reverse_lazy('accounts:password_reset_complete')),
            name="password_reset_confirm"
    ),

    # Reset Done
    path('reset/done/', 
            auth_views.PasswordResetCompleteView.as_view(),
            name="password_reset_complete"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
