from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Permission, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views import generic

from .forms import SignUpForm, EditProfileForm, EditUserForm
from .tokens import account_activation_token
from .models import Profile



# redirect user to their own panel after sign in 
@login_required
def home(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, 'user/user_profile.html', {'profile': profile})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            group = Group.objects.get(name='unpaid_user')
            user = form.save(commit=False)
            user.is_active = False
            group.user_set.add(user)
            user.save()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()

    return render(request, 'user/register.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'user/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'user/activation_invalid.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next = request.POST.get('next', '/')
                    print(next)
                    # return redirect(next)
                    return redirect('home')
                else:
                    return redirect('account_activation_invalid')
        else:
            return render(request, 'user/user_invalid.html')

    form = AuthenticationForm()
    return render(request, "user/login.html",{"form":form})



def logout_view(request):
    logout(request)
    return redirect('/')

def terms(request):
    return render(request, "user/userSignUpTerm.html")


@login_required
def edit_profile_view(request):
    args = {}
    if request.method == "POST":
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        form = EditUserForm(request.POST, instance = request.user)
      
        if form.is_valid() and profile_form.is_valid():
            user_form = form.save()
            custom_form = profile_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            print(custom_form)
            return redirect('home')
            
    else:
        form = EditUserForm(instance=request.user.profile)
        profile_form = EditProfileForm(instance = request.user)
        args = {}
        # args.update(csrf(request))
        args['form'] = form
        args['profile_form'] = profile_form
    return render(request, 'user/user_edit_profile.html', args)


