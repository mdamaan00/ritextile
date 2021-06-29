from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    search_fields = ('email','first_name','last_name')
    filter_horizontal = ()
    ordering = ('-date_joined',)
    list_display = ('email','first_name','last_name','is_active','is_admin',)
    list_filter = ('email','first_name','last_name','is_active','is_staff',)

    fieldsets = (
        (None , {'fields': ('email','password',)}),
        ('Personal Information',{'fields':('first_name','last_name',)}),
        ('Permissions',{'fields':('is_admin','is_active','is_staff',)}),
        ('Important Dates',{'fields':('date_joined','last_login')}),
        
    )
    add_fieldsets = (
        (None ,{
            
            'fields': ('email','password1','password2',),
        }),
    )

# Register your models here.



class Items(admin.ModelAdmin):
    search_fields = ('order',)
    list_display = ['id','order','product','quantity']
    
class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5
class AdminProduct(admin.ModelAdmin):
    list_display = ['name','category','image','available','stock']
    list_filter = ['category']
    inlines = [ProductImageInline]

class Addresses(admin.ModelAdmin):
    search_fields = ('id',)
    list_display = ['id','customer','first_name','address','phonenumber']
class allorder(admin.ModelAdmin):
    search_fields = ('id',)
    list_filter=['complete']
    list_display = ['id','customer','complete','date_orderd','address']

admin.site.register(User, UserAdminConfig)
admin.site.register(Reviews)
admin.site.register(Product,AdminProduct)
admin.site.register(Categories)
admin.site.register(ContactUs)
admin.site.register(Material)
admin.site.register(Order,allorder)
admin.site.register(OrderItem,Items)
admin.site.register(ShippingAddress,Addresses)
admin.site.register(AllAddresses,Addresses)
admin.site.register(Images)