from django.contrib import admin
from .models import Category, Product, Blog, Order, OrderItem

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price','available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Product, ProductAdmin)

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'posted']
    list_filter = ['author', 'posted']
admin.site.register(Blog, BlogAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email',
                    'created', 'updated']
    list_filter = ['created', 'updated']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)

class FilterUserAdmin(admin.ModelAdmin): 
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def get_queryset(self, request): 
        # For Django < 1.6, override queryset instead of get_queryset
        qs = super(FilterUserAdmin, self).get_queryset(request) 
        return qs.filter(created_by=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            # the changelist itself
            return True
        return obj.user == request.user

