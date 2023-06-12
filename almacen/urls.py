from django.urls import include, path
from rest_framework import routers
from .views import DashboardView,ModalProductView,AddCanvasShoppingCart,DropShoppingCart,CartView,\
    DeleteCartView,CheckoutView,CreateTransactionView,SuccessfulView,ErrorView,DeliveryView,\
    InventarioAlert,IndexAdminView,TransacitonAdminView,DetailVentasView,AdminProductView,\
    AdminGraphicsView,GraphProductView,GraphicsStatistView,TransacitonAdminViewad,custom_login
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'almacen'



urlpatterns = [

    path('', DashboardView.as_view(), name='dashboard'),
    path('admingraph/', IndexAdminView.as_view(), name='index_admin'),
    path('ventas/', TransacitonAdminView.as_view(), name='ventas'),
    path('ventasadmin/', TransacitonAdminViewad.as_view(), name='ventasadmin'),

    path('detailventas/',DetailVentasView.as_view(),name="detailventas"),#retornamos a la template de transactionsadmin el detalle de la transaccion seleccionada

    path('get-admin-product-modal/', AdminProductView.as_view(), name="get_admin_product"),   #modal del producto en el admin
    path('admins-tatistics/', AdminGraphicsView.as_view(), name="get_admin_graphics"),#template con las estadisticas de las ventas
    path('graphadmin/',GraphProductView.as_view(),name="graphproduct"),#graficadora del modal
    path('graphicsstatistics/',GraphicsStatistView.as_view(),name="graphics_statistics"),#graficadora del template de estadisticas

    path('alert/', InventarioAlert.as_view(), name='alert'),
    path('login/', custom_login, name='login'),
	path('logout/',LogoutView.as_view(), name='logout'),
    path('get-product-modal/', ModalProductView.as_view(), name='get_product_modal'),
    path('add-shopping-cart/',AddCanvasShoppingCart.as_view(), name='add-shopping-cart'),
    path('drop-shopping-cart/',DropShoppingCart.as_view(), name='drop-shopping-cart'),
    path('view-cart/', CartView.as_view() ,name='view-cart'),
    path('delete-cart/', DeleteCartView.as_view() ,name='delete-cart'),
    path('checkout/', CheckoutView.as_view() ,name='checkout'),
    path('transaction/', CreateTransactionView.as_view() ,name='transaction'),
    path('successful/', SuccessfulView.as_view() ,name='successful'),
    path('error/', ErrorView.as_view() ,name='errorview'),
    path('delivery/', DeliveryView.as_view(),name="delivery"),

]



