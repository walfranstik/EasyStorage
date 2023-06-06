
from django.contrib import admin
from .models import  ProductInformation,ProductImage,Category,GeneralSetting,Provider,Venta

# Register your models here.

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('name_image','image')

@admin.register(Category)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ProductInformation)
class ProductInformationAdmin(admin.ModelAdmin):
    list_display = ('reference_product','name_product','description_product','price_false','price_product')

@admin.register(Provider)
class TypeWalletAdmin(admin.ModelAdmin):
    list_display = ('name','address','phone_number','email')


@admin.register(Venta)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date_of_purchase",'email','total_amount',"first_name","last_name","phone_number","type_pay")

@admin.register(GeneralSetting)
class GeneralSettingAdmin(admin.ModelAdmin):
    list_display = ('primarycolor_page','secundarycolor_page','logo')

    