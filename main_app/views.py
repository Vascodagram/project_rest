from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.db.models.fields import mixins
from django.http import HttpResponseRedirect
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy
from django.core.mail import EmailMultiAlternatives, send_mail
from django.shortcuts import HttpResponse
from django.utils.encoding import force_text, force_bytes
#wiew
from django.contrib.auth.views import LogoutView
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, View
from django.views.generic.list import ListView
#mixin
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from main_app.models import Comment
#all
from project_restaurant.settings import EMAIL_HOST_USER
from .utils import *
from .forms import AuthUserForm, RegisterUserForm, CommentForm
from .tokens import account_activation_token
from django.core.paginator import Paginator
# Create your views here.


class MainView(ModelCategoryMixin, ListView):
    template_name = 'base.html'


class News(ModelCategoryMixin, ListView):
    queryset = Post.objects.filter(categories__slug='news')
    template_name = 'news.html'


class AllRestaurant(ModelCategoryMixin, ListView):
    queryset = Post.objects.filter(categories__slug='restaurant')
    template_name = 'all_restaurant.html'


class AboutUs(ContactAboutMixin, View):
    template_name = 'about_us.html'


class Contact(ContactAboutMixin, View):
    template_name = 'contact.html'


class NewsDetailView(FormMixin, DetailView):
    model = Post
    template_name = 'detail_post.html'
    context_object_name = 'detail_post'
    form_class = CommentForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('news-detail', kwargs={'pk': self.get_object().id})

    def post(self, request, *arg, **kwargs):
        forms = CommentForm(request.POST)
        if forms.is_valid():
            self.object = forms.save(commit=False)
            self.object.post = self.get_object()
            self.object.user = self.request.user
            self.object.save()
            forms = forms.save(commit=False)
            if request.POST.get('parent', None):
                forms.parent_id = int(request.POST.get('parent'))
                print(forms.parent_id)
                forms.save()
            return self.form_valid(forms)
        else:
            return self.form_invalid(forms)


class AuthUserView(View):

    def get(self, request, *args, **kwargs):
        form = AuthUserForm(request.POST or None)
        context = {'form': form}
        return render(request, 'registration/login.html', context)

    def post(self, request, *args, **kwargs ):
        form = AuthUserForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'registration/login.html', context)


class RegisterUserView(View):

    def get(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST or None)
        context = {'form': form}
        return render(request, 'registration/register.html', context)

    def post(self, request, *args, **kwargs):
        form = RegisterUserForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            # send email token
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Активація акаунту'
            message = render_to_string('registration/template_email.html',
                                       {'domain': current_site.domain,
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': account_activation_token.make_token(user),
                                        })
            msg = EmailMultiAlternatives(mail_subject, message, EMAIL_HOST_USER, [new_user.email])
            msg.send()
            #
            return render(request, 'registration/email_activate.html')
        context = {
            'form': form
        }
        return render(request, 'registration/register.html', context)


class UserLogout(LogoutView):
    next_page = reverse_lazy('base')


class SearchPost(ListView):
    template_name = 'search_result.html'
    model = Post
    context_object_name = 'search-result'

    def get_queryset(self):
        query = self.request.GET.get('search', '')
        if query:
            object_list = self.model.objects.filter(Q(title__icontains=query) | Q(full_text__icontains=query)).order_by('-date')
        else:
            object_list = self.model.objects.none()
        return object_list


@csrf_exempt
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64).decode())
        print(uid)
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return render(request, 'registration/done_activated_email.html')
    else:
        return render(request, 'registration/error_activate_email.html')
