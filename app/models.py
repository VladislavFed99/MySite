"""
Definition of models.
"""

from django.db import models

# Create your models here.

from django.contrib import admin #добавляем использование административного модуля
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.models import User


# Модель данных Блога – class Blog
class Blog(models.Model):
    title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
    author = models.ForeignKey(User, null=True, blank=True, on_delete = models.SET_NULL, verbose_name = "Автор")
    description = models.TextField(verbose_name = "Краткое содержание")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")
    content = models.TextField(verbose_name = "Полное содержание")
    posted = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Опубликовано")

    # Методы класса:

    def get_absolute_url(self): # метод возвращает строку с URL-адресом записи
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self): # метод возвращает название, используемое для представления отдельных записей в административном разделе
        return self.title

    # Метаданные – вложенный класс, который задает дополнительные параметры модели:

    class Meta:
        db_table = "Posts" # имя таблицы для модели
        ordering = ["-posted"] # порядок сортировки данных в модели ("-" означает по убыванию)
        verbose_name = "статья блога" # имя, под которым модель будет отображаться в административном разделе (для одной статьи блога)
        verbose_name_plural = "статьи блога"  # тоже для всех статей блога


#Модель комментариев
class Comment(models.Model):
    text = models.TextField(verbose_name = "Комментарий")
    date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата")
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор")
    post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья")

    def __str__(self):
        return 'Комментарий %s к %s' % (self.author, self.post)

    class Meta:
        db_table = "Comments"
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии к статьям блога"
        ordering = ["-date"]

admin.site.register(Comment)

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name = "Название категории")
    slug = models.SlugField(max_length=200, null=True, db_index=True, unique=True, verbose_name = "Алиас категории")

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category',
                        args=[self.slug])

#admin.site.register(Category)

# Модель данных Каталога – class Product
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name = "Категория")
    name = models.CharField(max_length=200, db_index=True, verbose_name = "Название товара")
    image = models.FileField(default = 'temp.jpg', verbose_name = "Путь к картинке")
    slug = models.SlugField(max_length=200, db_index=True, verbose_name = "Алиас", null=True)
    description = models.TextField(blank=True, verbose_name = "Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name = "Цена")
    available = models.BooleanField(default=True, verbose_name = "Доступно")
    created = models.DateTimeField(auto_now_add=True, verbose_name = "Создано")
    updated = models.DateTimeField(auto_now=True, verbose_name = "Обновлено")

    class Meta:
        ordering = ('name',)
        db_table = "Products"
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product',
             args=[self.id, self.slug])

#admin.site.register(Product)

class Order(models.Model):
    name = models.CharField(max_length=50, verbose_name = "Имя")
    email = models.EmailField(verbose_name = "Адрес электронной почты")
    created = models.DateTimeField(auto_now_add=True, verbose_name = "Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name = "Обновлён")
    user = models.ForeignKey(User, null=True, on_delete = models.CASCADE, verbose_name = "Покупатель")

    class Meta:
        db_table = "Orders"
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    #метод get_total_cost(), чтобы получить общую стоимость товаров, купленных в этом заказе.


class OrderItem(models.Model):
    #Модель OrderItem позволяет хранить продукт, количество и цену, уплаченную за каждый товар.
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name = "Заказ")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name = "Товар")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name = "Цена")
    quantity = models.PositiveIntegerField(default=1, verbose_name = "Количество")

    class Meta:
        verbose_name = 'Содержание заказа'
        verbose_name_plural = 'Содержание заказов'
        db_table = "OrderItems"

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

admin.site.register(OrderItem)

