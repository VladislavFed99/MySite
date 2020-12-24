from decimal import Decimal
from django.conf import settings
from .models import Product

class Cart(object):
    def __init__(self, request):
        """
        Инициализируем корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохранение пустой корзины
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """
        Добавить продукт в корзину или обновить его количество.
        """
        product_id = str(product.id)

        #Экземпляр Product для добавления или обновления в корзине
        
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                 'price': str(product.price)}
        if update_quantity: 
       
        #Это логическое значение, которое указывает, 
        #требуется ли обновление количества с заданным количеством (True),
        #или же новое количество должно быть добавлено к существующему количеству (False).
        
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        #Метод save() сохраняет все изменения в корзине в сессии и помечает
        #сессию как modified с помощью session.modified = True. 
        #Это говорит о том, что сессия modified и должна быть сохранена.

        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True
    
    def remove(self, product):
        #Метод remove() удаляет заданный продукт из словаря корзины и вызывает метод save()
        #для обновления корзины в сессии.

        """
        Удаление товара из корзины.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):

        #В методе __iter__() мы извлекаем экземпляры продукта,
        #присутствующие в корзине, чтобы включить их в номенклатуры корзины. 
        #Наконец, мы проходим по элементам корзины, преобразуя цену номенклатуры обратно 
        #в десятичное число и добавляя атрибут total_price к каждому элементу.

        """
        Перебор элементов в корзине и получение продуктов из базы данных.
        """
        product_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Подсчет всех товаров в корзине.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Подсчет стоимости товаров в корзине.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True