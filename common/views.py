from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect


from .forms import SignUpForm, UserForm, ProfileForm, FormLogin

# Create your views here.


class HomeView(TemplateView):
    """ just Home View class """
    template_name = 'common/home.html'


class SignUpView(CreateView):
    """ SignUpView class to render the Registration Form """
    form_class = SignUpForm
    success_url = reverse_lazy('home')
    template_name = 'common/register.html'


class LoginViewManual(TemplateView):
    """ LoginView class to render the Login Form """
    def get(self, *args, **kwargs):
        form = FormLogin()
        return render(self.request, 'common/login_manual.html', {'form': form})

    def post(self, *args, **kwargs):
        form = FormLogin(self.request.POST)
        # check if username and password are not empty(by default required=True)
        if form.is_valid():
            # check if credentials are valid
            user = authenticate(
                username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(self.request, user)
                    return HttpResponseRedirect(reverse('profile'))
            else:
                return render(self.request, 'common/login_manual.html', {
                    'error_message': 'invalid credentials',
                    'form': form
                })
        return render(self.request, 'common/login_manual.html')


class ProfileView(LoginRequiredMixin, TemplateView):
    """ ProfileView class to Show the profile Form """
    template_name = 'common/profile.html'


class ProfileUpdateView(LoginRequiredMixin, TemplateView):
    """ ProfileView class to render the user and profile Form to update the user details """
    user_form = UserForm
    profile_form = ProfileForm
    template_name = 'common/profile-update.html'

    def post(self, request):
        post_data = request.POST or None
        file_data = request.FILES or None

        # Showing the created user and profile instances with the existing data
        user_form = UserForm(post_data, instance=request.user)
        profile_form = ProfileForm(
            post_data, file_data, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.error(request, 'Your profile is updated successfully!')
            return HttpResponseRedirect(reverse_lazy('profile'))

        context = self.get_context_data(
            user_form=user_form,
            profile_form=profile_form
        )
        return self.render_to_response(context)

    # to get the update form with post data
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
