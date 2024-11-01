from django.views.generic import TemplateView, CreateView

from users.forms import UserRegisterForm
from users.models import CustomUser


class BaseView(TemplateView):
    extra_context = {'title': 'Главная'}
    template_name = 'main/base.html'


class UserCreateView(CreateView):
    model = CustomUser
    form_class = UserRegisterForm
    template_name = 'main/user_form.html'
