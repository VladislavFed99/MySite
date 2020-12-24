"""
Definition of forms.
"""

from django.contrib.auth.models import User
from django import forms
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from django.db import models
from .models import Comment, Blog, Category, Product, Order
from .cart import Cart

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Логин'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))

class FeedbackForm(forms.Form):
    """Класс для формы обратной связи"""
    name = forms.CharField(label='Ваше имя', min_length=2, max_length=40)
    rating = forms.ChoiceField(label='Оцените наш сайт',
                               choices=[('1','Плохо'), ('2','Нормально'), ('3','Хорошо')],
                               widget=forms.RadioSelect, initial=2)
    type = forms.ChoiceField(label='Выберите тип обращения',
                             choices=(('1','Отзыв'),
                                      ('2','Предложение'),
                                      ('3','Претензия')), initial = 1)
    message = forms.CharField(label='Ваш отзыв',
                              widget=forms.Textarea(attrs={'rows':10,'cols':50}))
    email = forms.CharField(label='Ваш адрес электронной почты', min_length=6, max_length=40)
    notice = forms.BooleanField(label='Желаете получить ответ на ваш отзыв через e-mail?',
                                required=False)

class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment # используемая модель
        fields = ('text',) # требуется заполнить только поле text
        labels = {'text': "Комментарий"} # метка к полю формы text

class BlogForm (forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'description', 'content', 'posted', 'image',)
        labels = {'title': "Заголовок", 'description': "Краткое описание", 'content': "Содержание", 'posted': "Дата", 'image': "Изображение"}

#class ProductForm (forms.ModelForm):
#    class Meta:
#        model = Catalog
#        fields = ('title', 'description', 'cost', 'posted', 'image',)
#        labels = {'title': "Заголовок", 'description': "Краткое описание", 'content': "Содержание", 'posted': "Дата", 'author': "Автор", 'image': "Изображение"}

class CartAddProductForm(forms.Form): 
    #Эта форма будет использоваться для добавления продуктов в корзину.
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    #позволяет пользователю выбрать количество между 1-20. Мы используем поле TypedChoiceField с coerce=int для преобразования ввода в целое число.
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    #позволяет указать, следует ли добавлять сумму к любому существующему значению
    #в корзине для данного продукта (False) или если существующее
    #значение должно быть обновлено с заданным значением (True).

class OrderCreateForm(forms.ModelForm):
    
    class Meta:
        model = Order
        fields = ['name', 'email']
        labels = {'name': "Имя", 'email':"Адрес электронной почты"}


