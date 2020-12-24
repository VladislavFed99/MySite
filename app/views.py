"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.decorators.http import require_POST
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from .forms import FeedbackForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import CreateView, ListView, UpdateView, FormView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from django.db import models
from .models import Blog, Comment, Category, Product, OrderItem, Order

from .forms import CommentForm, BlogForm # использование формы ввода комментария
from .forms import CartAddProductForm, OrderCreateForm
from .cart import Cart



def home(request):
    """Renders the home page."""
    posts = Blog.objects.all()[:3] # запрос на выбор 3 статей блога из модели

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домашняя страница',
            'posts': posts,
            'year':datetime.now().year,
        }
    )



@login_required
def account(request):
    my_orders = Order.objects.filter(user=request.user)

    return render(request, "app/myorders.html",
                  {"my_orders": my_orders,
                   'title':'Мои заказы',
                   'year':datetime.now().year,})



@login_required
def accountorder(request, param):
    myorder = OrderItem.objects.get(id=param) # запрос на выбор конкретной статьи по параметру

    if (request.GET.get('DeleteButton')):
        Order.objects.filter(id = request.GET.get('DeleteButton')).delete()
        return redirect('/')

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/myorder.html',
            {
            'myorder': myorder, # передача конкретной статьи в шаблон веб-страницы
            'title':'Мой заказ',
            'year':datetime.now().year,
            }
            )



def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Контактные данные:',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'year':datetime.now().year,
        }
    )

def registration(request):
    """Renders the registration page."""

    if request.method == "POST": # после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных
            return redirect('home') # переадресация на главную страницу после регистрации

    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя

    assert isinstance(request, HttpRequest)
    return render(
    request,
    'app/registration.html',
        {
        'regform': regform, # передача формы в шаблон веб-страницы
        'year':datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
           {
            'title':'Новости',
            'posts': posts, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
            }
    )

def blogpost(request, parametr):
    """Renders the blogpost page."""
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST": # после отправки данных формы на сервер методом POST

        form = CommentForm(request.POST)

        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm() # создание формы для ввода комментария

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
            {
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'title':'Блог',
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
            'year':datetime.now().year,
            }
            )

def newpost(request):
    """Renders the newpost page."""

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user 

            blog_f.save()

            return redirect('blog')
    
    else:
        blogform = BlogForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/newpost.html',
            {
            'title':'Блог',
            'blogform': blogform,
            'year':datetime.now().year,
            }
            )

def catalog(request, category_slug=None):
    """Renders the catalog page."""
    cart = Cart(request)
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                  'app/catalog.html',
                  {'category': category,
                   'categories': categories,
                   'cart': cart,
                   'products': products,
                   'title':'Каталог',
                   'message':'Здесь представлен имеющийся товар',
                   'year':datetime.now().year,
                   })

def product(request, id, slug):
    """Renders the product page."""
    cart = Cart(request)
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)

    cart_product_form = CartAddProductForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/product.html',
            {
            'product': product, # передача конкрет в шаблон веб-страницы
            'cart_product_form': cart_product_form,
            'title':'Товар',
            'cart': cart,
            'year':datetime.now().year,
            }
            )

@require_POST
def cart_add(request, product_id):
    #Это представление для добавления продуктов в корзину или обновления количества для существующих продуктов.

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
       cd = form.cleaned_data
       cart.add(product=product,
                quantity=cd['quantity'],
                update_quantity=cd['update'])
    return redirect('cart_detail')

def cart_remove(request, product_id):
    #Представление cart_remove получает id продукта в качестве параметра. Мы извлекаем экземпляр продукта с заданным id и удаляем продукт из корзины.
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')

def cart_detail(request):
    #Представление для отображения корзины и ее товаров.
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True
                                        })
    return render(request, 'app/cart.html', {'cart': cart, 'title':'Корзина', 'year':datetime.now().year} )

def order_create(request):
    #В представлении order_create мы получаем текущую корзину из сесссии с cart = Cart(request)
    cart = Cart(request)
    if request.method == 'POST':
        #POST request : Проверяет валидность введенных данных. 

        form = OrderCreateForm(request.POST)
        if form.is_valid():
        #Если данные являются допустимыми, то для создания нового экземпляра заказа будет использоваться order = form.save().
            order = form.save()
            order.user = request.user
            order.save()
            #Затем мы сохраняем его в базу данных, а затем храним в переменной order. 
            for item in cart:
                #После создания заказа мы перейдем по товарам корзины и создадим OrderItem для каждого из них.
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'app/created.html',
                          {'order': order})
    else:
        form = OrderCreateForm
        #GET request : Создается экземпляр формы OrderCreateForm и отображается шаблон app/createorder.html
    
    assert isinstance(request, HttpRequest)
    return render(request, 'app/createorder.html',
                  {'cart': cart, 'form': form, 'year':datetime.now().year})
