import json
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate, REDIRECT_FIELD_NAME
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.http import is_safe_url
from django.views.generic import FormView, RedirectView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from track.models import Course
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from accounts.tokens import account_activation_token
from django.core.mail import EmailMessage
from accounts.models import Profile
from accounts.forms import (
        LoginForm, 
        UserRegistrationForm,
        UserEditForm,
        ProfileEditForm
    )


@csrf_exempt
def validate_username(request):
    username = request.GET.get('username', None)
    
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }

    if data['is_taken']:
        data['error_message'] = 'This username already exists.'

    return JsonResponse(data)

@csrf_exempt
def validate_email(request):
    email = request.GET.get('email', None)
    
    data = {
        'is_taken': User.objects.filter(email__iexact=email).exists()
    }

    if data['is_taken']:
        data['error_message'] = 'This email already exists.'

    return JsonResponse(data)



class RegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = 'registration/register.html'

    def form_valid(self, form):

        user = form.save(commit=False)
        user.is_active = False
        user.save()

        ## Send confirmation message
        current_site = get_current_site(self.request)
        message = render_to_string('activate/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        # # Sending activation link in terminal
        # user.email_user(subject, message)
        mail_subject = 'Activate your freeLearnAcademy account.'
        to_email = form.cleaned_data.get('email')

        print(f"\n\n {to_email} \n\n")

        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        
        return render(self.request, 'activate/acc_active_sent.html')
        
        # or
        # return redirect('accounts:login')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        messages.success(request,
            "Thank you for your email confirmation. Now you can complete your profile settings.")

        return redirect('accounts:edit_account')
    else:
        return HttpResponse('Activation link is invalid!')


class LoginView(FormView):

    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('track:dashboard')
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form = AuthenticationForm(data=self.request.POST, request=self.request)

        if form.is_valid():
    
            user = form.get_user()
            if not user.is_active:
                return HttpResponse("Your account not active yet. Please active your account first and try again.")
            login(self.request, user)

            # if we need to do anything on user when login success
            # user.profile.loged()
            
            return super(LoginView, self).form_valid(form)

        else:
            return self.render_to_response({
                'form': form
            })

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=[self.request.get_host()]):
            redirect_to = self.success_url
        return redirect_to

class LogoutView(RedirectView):

    url = '/'
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class UserProfileView(View):

    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        if request.user.username == username:
            return render(request, 'accounts/my_profile.html', {})

        profile = get_object_or_404(Profile,
                     user__username__iexact=username)
        profile.viewed()
        context = {
            'profile': profile,
            }
        return render(request, 'accounts/profile.html', context)


class EditAccountView(LoginRequiredMixin, View):

    template_name = 'accounts/edit_account.html'

    def get(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, self.template_name,
                                    {'user_form': user_form,
                                        'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user,
                                    data=request.POST)
        profile_form = ProfileEditForm(
                            instance=request.user.profile,
                            data=request.POST,
                            files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Data has been successfully updated.')
        else:
            messages.error(request, 'Please correct the error below.')

            return reverse('accounts:edit_account')

        return redirect('accounts:users', username=request.user.username)

# User fields
# date_joined, email, first_name, groups, id,
# is_active, is_staff, is_superuser, last_login,
# last_name, logentry, password, profile, user_permissions,
# username