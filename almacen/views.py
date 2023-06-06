from django.shortcuts import render,redirect
from django.views.generic import ListView,View,TemplateView
from django.shortcuts import get_object_or_404
from .models import ProductInformation,ProductImage,Category,GeneralSetting,Venta
from almacen.utils import articulosComprados,dictionari_shopping,cant_product_transaction,information_transaction,dias_amount,\
amount_id,dias_compras
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.core.paginator import Paginator
from .form import TransactionForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import UserPassesTestMixin
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import base64
import io



def test_func(request):
        print('lllllllll')
        print(request.user.is_superuser)
        return request.user.is_superuser

@method_decorator(login_required, name='dispatch')
class DashboardView(ListView):
   

    template_name = 'core/dashboard_base.html'
    model = ProductInformation
    queryset = ProductInformation.objects.all().order_by('-id')
    paginate_by = 6 # Define la cantidad de elementos por página
    
    def get_queryset(self):
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')

        
        if search:
            name = self.queryset.filter(name_product__icontains=search).order_by('-id')
            idproduct = self.queryset.filter(reference_product__icontains=search).order_by('-id')
            if name:
                self.queryset=name
            else:
                self.queryset=idproduct


        if category:
            self.queryset = self.queryset.filter(categories__name=category).order_by('-id')
        # El ordenamiento se realiza antes de la paginación
        return self.queryset

    def get_context_data(self, **kwargs):
        if(self.request.user.is_superuser):
            redirect('/admin')
        context = super().get_context_data(**kwargs)
        self.category_list = Category.objects.all()
        context['category_list'] = self.category_list
        # Agrega el paginador al contexto
        paginator = Paginator(self.queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

@method_decorator(login_required, name='dispatch')
class DeleteCartView(View):
    template_name='core/components/canvas/shopping_cart.html'
    def get(self,request,*args, **kwargs):
        # Obtener el id del producto que se agrega al carrito
        delete_product_id= request.GET.get('delete_product_id')

        # se obitiene el producto el cual se agrego al carrito
        product= ProductInformation.objects.get(pk=delete_product_id)

        # Obtener el carrito de compras actual del usuario
        cart = request.session.get('cart', {})
        # Agregar el producto al carrito o actualizar la cantidad si ya está en el carrito
        if delete_product_id in cart:
            print('-----------------------------------85----')
            print(cart[delete_product_id]['quantity'])
            product.quantity+=cart[delete_product_id]['quantity']
            product.save()
            cart.pop(delete_product_id, None)
            request.session['cart'] = cart

        cartS= request.GET.get('cart')
        if cartS=='cart':
            return redirect('almacen:body_cart')
        else:
            return redirect('almacen:view-cart')

@method_decorator(login_required, name='dispatch')
class AddCanvasShoppingCart(View):
    template_name = 'core/components/canvas/shopping_cart.html'
    def get(self,request,*args, **kwargs):
        # Obtener el id del producto que se agrega al carrito
        product_id= request.GET.get('product_id')

        

        # Obtener la cantidad de productos
        #quantity= request.GET.get('quantity')

        # se obitiene el producto el cual se agrego al carrito
        product= ProductInformation.objects.get(pk=product_id)

        # Obtener el carrito de compras actual del usuario
        cart = request.session.get('cart', {})
        # Agregar el producto al carrito o actualizar la cantidad si ya está en el carrito
        print(product.quantity)
        if product_id in cart:
            cart[product_id]['quantity'] += 1
            product.quantity-=1
            product.save()
            
        else:
            cart[product_id] = {
                'name': product.name_product,
                'image': product.images.all()[0].image.url,
                'price': float(product.price_product),
                'quantity': 1
            }
            product.quantity-=1
            product.save()
        request.session['cart'] = cart
        print('-----------------22222222-----------')
        print(product.quantity)
        cartS= request.GET.get('cart')
        if cartS=='cart':
            return redirect('almacen:body_cart')
        else:
            return redirect('almacen:view-cart')

@method_decorator(login_required, name='dispatch')        
class DropShoppingCart(View):
    template_name = 'core/components/canvas/shopping_cart.html'
    def get(self,request,*args, **kwargs):
        # Obtener el id del producto que se agrega al carrito
        product_id= request.GET.get('drop_product_id')

        # Obtener la cantidad de productos
        #quantity= request.GET.get('quantity')

        # se obitiene el producto el cual se agrego al carrito
        product= ProductInformation.objects.get(pk=product_id)
        cartS= request.GET.get('cart')
        # Obtener el carrito de compras actual del usuario
        cart = request.session.get('cart', {})
        # Agregar el producto al carrito o actualizar la cantidad si ya está en el carrito
        if product_id in cart:
            if cart[product_id]['quantity'] > 0:
                cart[product_id]['quantity'] -= 1
                product.quantity+=1
                product.save()
            else:
                if cartS=='cart':
                    url = reverse('almacen:delete-cart') + '?delete_product_id=' + str(product_id + '&cart=cart')
                    return HttpResponseRedirect(url)
                else:
                    url = reverse('almacen:delete-cart') + '?delete_product_id=' + str(product_id)
                    return HttpResponseRedirect(url)
                

        request.session['cart'] = cart


        
        if cartS=='cart':
            return redirect('almacen:body_cart')
        else:
            return redirect('almacen:view-cart')

#el carrito que es modal pequeño
@method_decorator(login_required, name='dispatch')
class CartView(View):
    template_name = 'core/components/canvas/shopping_cart.html'

    def get(self, request):
        # Obtener el carrito de compras actual del usuario
        cart = request.session.get('cart', {})
        
        # Calcular el precio total del carrito de compras
        total_price = sum(item['price'] * item['quantity'] for item in cart.values())

        sub_total_price = {}
        for product_id, item in cart.items():
            sub_total_price[product_id] = item['price'] * item['quantity']

        # Renderizar la plantilla con el carrito actual y el precio total
        return render(request, self.template_name , {'cart': cart, 'total_price': total_price,'sub_total_price':sub_total_price})


@method_decorator(login_required, name='dispatch')
class ModalProductView(View):


    template_name = 'core/components/modals/modal_product.html'

    def get(self, request, *args, **kwargs):
        product_id= request.GET.get('product_id')
        product= ProductInformation.objects.get(pk=product_id)
        return render(request, self.template_name, {'product':product})
   
@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    template_name = 'core/checkout.html'
    def get(self, request, *args, **kwargs):
        # Obtener el carrito de compras actual del usuario
        cart = request.session.get('cart', {})
        typedelivery=request.GET.get('typedelivery')
        # Calcular el precio total del carrito de compras
        price = sum(item['price'] * item['quantity'] for item in cart.values())
        
      

        
        context={
            'cart': cart,
            'price': price,
        }
        
        # Renderizar la plantilla con el carrito actual y el precio total
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class CreateTransactionView(View):
    


    def post(self,request):
        
        instance=TransactionForm(request.POST)
        if instance.is_valid():
            transaction=instance.save(commit=False)
            articles=articulosComprados(request)
            transaction.articles=articles
            transaction.save()

            cart = request.session.get('cart', {})
            del request.session['cart']


            return redirect('almacen:successful')
            
        else:
            print(instance.errors)
            print(instance)
            return JsonResponse({'error':'error'})
            
@method_decorator(login_required, name='dispatch')        
class SuccessfulView(TemplateView):
    template_name= 'core/successful.html'


class ErrorView(TemplateView):
    template_name= 'core/error.html'
@method_decorator(login_required, name='dispatch')
class InventarioAlert(TemplateView):
    template_name= 'core/components/modals/dialog.html'
    

class DeliveryView(View):

    template_name = 'core/checkout.html'
    def get(self, request, *args, **kwargs):
        return redirect('almacen:checkout')

@method_decorator(login_required, name='dispatch')    
class TransacitonAdminView(ListView):
    template_name = 'core/transactions.html'
    model = Venta
    paginate_by = 8 # Define la cantidad de elementos por página
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.transaction_list = Venta.objects.all().order_by('-id')
        
        context['transaction_list']= self.transaction_list
        context['productsShopping']= dictionari_shopping()
        context['cantproduct']= cant_product_transaction(self.transaction_list)
        
        # Agrega el paginador al contexto
        paginator = Paginator(self.transaction_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        
        return context

@method_decorator(login_required, name='dispatch')
class DetailVentasView(View):
    template_name = 'core/details_transactions.html'
    def get(self, request, *args, **kwargs):
        idtransaction=request.GET.get('idtransaction')
        producsShopping=information_transaction(idtransaction)
        products_list=ProductInformation.objects.all()
        transaction=Venta.objects.get(pk=idtransaction)
        typePay=transaction.type_pay
        context={
            "producsShopping":producsShopping,
            "products_list":products_list,
            "typePay":typePay,

        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')    
class IndexAdminView(ListView):
    template_name = 'core/index_admin.html'
    model = ProductInformation
    queryset = ProductInformation.objects.all().order_by('-id')
    paginate_by = 6 # Define la cantidad de elementos por página
    
    def get_queryset(self):
        search = self.request.GET.get('search')
        category = self.request.GET.get('category')

        
        if search:
            self.queryset = self.queryset.filter(name_product__icontains=search).order_by('-id')
        if category:
            self.queryset = self.queryset.filter(categories__name=category).order_by('-id')
        # El ordenamiento se realiza antes de la paginación
        return self.queryset

    def get_context_data(self, **kwargs):
        self.request.session['referred'] = self.request.GET.get('user')
        context = super().get_context_data(**kwargs)
        self.category_list = Category.objects.all()
        self.transaction_list = Venta.objects.all()
        context['category_list'] = self.category_list
        context['transaction_list']= self.transaction_list
        context['productsShopping']= dictionari_shopping()
        
        # Agrega el paginador al contexto
        paginator = Paginator(self.queryset, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        print(page_number)
        print(page_obj)
        context['page_obj'] = page_obj
        
        return context


@method_decorator(login_required, name='dispatch')    
 
# session especial para graficos para ver graficamente ganancias,etc 
class AdminGraphicsView(TemplateView):
    template_name = 'core/graphicsforadmin.html'
    
@method_decorator(login_required, name='dispatch')    

# graficador de las estadisticas
class GraphicsStatistView(View):
    def get(self, request, *args, **kwargs):
        timeinterval= request.GET.get('timeinterval')
        id_product= request.GET.get('id')

        today = datetime.now()

        if timeinterval=='week':
            week = today - timedelta(days=7)
            result = Venta.objects.filter(date_of_purchase__range=[week, today]).order_by('date_of_purchase')
            dict_values_graph=dias_amount(result,7)

        elif timeinterval=='month':
            month = today - timedelta(days=30)
            result = Venta.objects.filter(date_of_purchase__range=[month, today]).order_by('date_of_purchase')
            dict_values_graph=dias_amount(result,30)

        elif timeinterval=='year':
            year = today - timedelta(days=365)
            result = Venta.objects.filter(date_of_purchase__range=[year, today]).order_by('date_of_purchase')
            dict_values_graph=dias_amount(result,365)

        
        # Generar la imagen con Matplotlib
        x_values = list(dict_values_graph.keys())  # Crear una lista de los valores de las claves del diccionario dict_values_graph
        y_values = list(dict_values_graph.values())  # Crear una lista de los valores de las entradas del diccionario dict_values_graph
        fig, ax = plt.subplots(figsize=(12, 10))  # Crear una figura y un conjunto de ejes, y especificar el tamaño de la figura
        ax.plot(x_values, y_values)  # Crear una línea en el gráfico con los valores x y y especificados
        ax.set_xlabel('Dates')  # Establecer una etiqueta para el eje x
        ax.set_ylabel('Profits')  # Establecer una etiqueta para el eje y
        ax.set_title('Profits Graph')  # Establecer un título para el gráfico
        ax.set_xticklabels(x_values, rotation=90)  # Establecer etiquetas para las marcas del eje x, y rotarlas 25 grados
        ax.set_xticks(x_values)#modificar los valores de los label individuales del eje x
        # Convertir la imagen en un formato que pueda ser transmitido por HTTP
        buffer = io.BytesIO()  # Crear un objeto BytesIO para guardar los datos de la imagen
        plt.savefig(buffer, format='png')  # Guardar la figura en el objeto BytesIO en formato PNG
        buffer.seek(0)  # Mover el cursor al principio del objeto BytesIO
        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')  # Codificar los datos de la imagen en base64 y convertirlos a una cadena

        # Devolver la imagen como una respuesta JSON
        response_data = {'image': image_data}  # Crear un diccionario con una clave "image" que tiene el valor de la cadena de la imagen codificada en base64
        return JsonResponse(response_data)  # Devolver una respuesta JSON con el diccionario creado anteriormente
    

@method_decorator(login_required, name='dispatch')    

# modal del producto pero para los admin
class AdminProductView(View):
    template_name = 'core/components/modals/admin_product.html'

    def get(self, request, *args, **kwargs):
        product_id= request.GET.get('product_id')
        product= ProductInformation.objects.get(pk=product_id)
        cantProductsShopping=dictionari_shopping()
        cantProducts = int(cantProductsShopping[product_id]) 
        total_amount=amount_id(product_id)
        total_amount=total_amount[product_id]
        return render(request, self.template_name, {'product':product,'cantProducts':cantProducts,'total_amount':total_amount})

@method_decorator(login_required, name='dispatch')    

#graficos de la modal
class GraphProductView(View):

    def get(self, request, *args, **kwargs):
        timeinterval= request.GET.get('timeinterval')
        id_product= request.GET.get('id')

        today = datetime.now()

        if timeinterval=='week':
            week = today - timedelta(days=7)
            result = Venta.objects.filter(date_of_purchase__range=[week, today]).order_by('date_of_purchase')
            dict_values_graph=dias_compras(result,7,id_product)

        elif timeinterval=='month':
            month = today - timedelta(days=30)
            result = Venta.objects.filter(date_of_purchase__range=[month, today]).order_by('date_of_purchase')
            dict_values_graph=dias_compras(result,30,id_product)

        

        
        colorbar=GeneralSetting.objects.first()
        colorbar=colorbar.primarycolor_page
        # Generar la imagen con Matplotlib
        x_values = list(dict_values_graph.keys())
        y_values = list(dict_values_graph.values())
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.bar(x_values, y_values, color= colorbar)
        ax.set_xlabel('Dates')
        ax.set_ylabel('Quantity Sold')
        ax.set_title('Sales Graph')
        ax.set_xticklabels(x_values, rotation=90)
        ax.set_xticks(x_values)
        yval=[i for i in range(1, y_values[-1]+1)]
        ax.set_yticks(yval)


        # Convertir la imagen en un formato que pueda ser transmitido por HTTP
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Devolver la imagen como una respuesta JSON
        response_data = {'image': image_data}
        return JsonResponse(response_data)

@method_decorator(login_required, name='dispatch')    
class TransacitonAdminViewad(ListView):
    template_name = 'core/admin_transactions.html'
    model = Venta
    paginate_by = 8 # Define la cantidad de elementos por página
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.transaction_list = Venta.objects.all().order_by('-id')
        
        context['transaction_list']= self.transaction_list
        context['productsShopping']= dictionari_shopping()
        context['cantproduct']= cant_product_transaction(self.transaction_list)
        
        # Agrega el paginador al contexto
        paginator = Paginator(self.transaction_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        
        return context