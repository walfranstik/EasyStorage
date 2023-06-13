from django.db import models
from django.utils.translation import gettext as _
from .choices import StatusChoices,PayChoices
from colorfield.fields import ColorField
import json



# Create your models here.
class ProductImage(models.Model):
    name_image=models.CharField(default='',max_length=100, verbose_name=_('Product name image'), help_text=_('Input name image'), blank=False)
    image= models.ImageField(verbose_name=_('Product image'), help_text=_('Input Product image'),upload_to='imgproduct/',null=False)
 
    def __str__(self):
        return self.name_image

    class Meta:
        verbose_name=_('Product image')
        verbose_name_plural=_('Product images')

class Category(models.Model):
    name = models.CharField(max_length=50,help_text=("Input category name"))
    description= models.CharField(max_length=550,help_text=("Input Description"))

    def __str__(self):
        return self.name
class Provider(models.Model):
    name = models.CharField(max_length=50,help_text=("Input category name"))
    address = models.CharField(max_length=200, verbose_name=_('Address'), help_text=_('Input Address '), blank=True)
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone number'), help_text=_('Input Phone number'), blank=False,default="")
    email = models.EmailField(verbose_name=_("email address"), help_text=_("Input email address."))

    def __str__(self):
        return self.name

class ProductInformation(models.Model):
    
    reference_product= models.CharField(max_length=200, verbose_name=_('Product reference'), help_text=_('Input Product reference'), blank=False)
    name_product = models.CharField(max_length=200, verbose_name=_('Product name'), help_text=_('Input Product name'), blank=False)
    description_product= models.TextField(verbose_name=_('Product description'), help_text=_('Input Product description'), blank=False)
    buy_price = models.DecimalField(max_digits=16, decimal_places=6, verbose_name=_('Buy Price of the product'), help_text=_('Input Buy Price of the product'),
                                           blank=False, default=0)
    price_product = models.DecimalField(max_digits=16, decimal_places=6, verbose_name=_('Price of the product'), help_text=_('Input Price of the product'),
                                           blank=False, default=0)
    price_false= models.DecimalField(max_digits=16, decimal_places=6, verbose_name=_('Price false of the product'), help_text=_('Input Price false of the product'),
                                           blank=False, default=0)
    images= models.ManyToManyField(ProductImage,verbose_name=_('Product image'), help_text=_('Input Product image'),blank=False, related_name='productimg')
    categories=models.ManyToManyField(Category,verbose_name=_('Product category'), help_text=_('Input Product category'),blank=False, related_name='productCategory')
    provider=models.ManyToManyField(Provider,verbose_name=_('Product Provider'), help_text=_('Input Product Provider'),blank=False, related_name='productProvider')
    quantity= models.IntegerField(verbose_name='Quantity of the product', help_text='Input Quantity of the product', blank=False, default=0)

    
    def __str__(self):
        return self.name_product    
    class Meta:
        verbose_name=_('Product Information')
        verbose_name_plural=_('Products Information')


class Venta(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=_('First name'), help_text=_('Input First name'), blank=False,default="")
    last_name = models.CharField(max_length=50, verbose_name=_('Last name'), help_text=_('Input Last name'), blank=False,default="")
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone number'), help_text=_('Input Phone number'), blank=False,default="")
    address = models.CharField(max_length=400, verbose_name=_('Address'), help_text=_('Input Address '), blank=False)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, verbose_name=('Status'), help_text=('Input Status'), default=StatusChoices.WAITING_FOR_APPROVAL, blank=False)
    articles = models.TextField(verbose_name=_('Articles'), help_text=_('Input Articles'), blank=False,default="")
    date_of_purchase = models.DateField(verbose_name=_("Date of purchase"),auto_now_add=True, help_text=_("The date on which the transaction was made."))
    email = models.EmailField(verbose_name=_("email address"), help_text=_("Input email address."))
    total_amount = models.DecimalField(max_digits=16, decimal_places=6, verbose_name=_("Total amount of the purchase"), help_text=_("The total amount of the purchase."))
    type_pay= models.CharField(max_length=25, choices=PayChoices.choices, verbose_name=('Type Pay'), help_text=('Input Type Pay'), default=PayChoices.CASH, blank=False)
    class Meta:
        verbose_name = "Sale"
        verbose_name_plural = "Sales"

    def __str__(self):
        return self.articles
    


class GeneralSetting(models.Model):
    primarycolor_page = ColorField(default='#00234D', verbose_name=_("Primary color of the page"), help_text=_("Input Primary color of the page."))
    secundarycolor_page = ColorField(default='#F76B6A', verbose_name=_("Secundary color of the page"), help_text=_("Input Secundary color of the page."))
    logo = models.ImageField(upload_to='logos/', verbose_name=_("Logo"), help_text=_("Input Logo."))
    url=models.CharField(max_length=500, verbose_name=_('Url para la api de usuarios de GainUp'), help_text=_('Input URL'), blank=False,default="")
    color_footer=ColorField(default='#00234D', verbose_name=_("Color of the footer"), help_text=_("Input color of the footer."))
    
    class Meta:
        verbose_name = "General Setting"
        verbose_name_plural = "General Settings"

