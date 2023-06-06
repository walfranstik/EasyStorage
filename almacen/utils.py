def articulosComprados(request):
    cart = request.session.get('cart', {})
    articuloscomprados = {}
    for product_id, item in cart.items():
            articuloscomprados[product_id] = item["quantity"] 
    return articuloscomprados


def dictionari_shopping():
    from .models import Venta
    transactions= Venta.objects.all()

    # Crear un diccionario para almacenar la cantidad total de compras de cada producto
    total_quantities = {}
    for transactions in transactions:

        articles=transactions.articles
        articles_list = articles.split(",")
        for article in articles_list:
            articles = article.replace('{', '')
            articles = articles.replace('}', '')
            articles = articles.replace("'", "")
            article_id, quantity = articles.split(":")
            article_id = article_id.strip()
            quantity = int(quantity.strip())
            if article_id in total_quantities:
                total_quantities[article_id] += quantity
            else:
                total_quantities[article_id] = quantity
    # Devolver el diccionario con la cantidad total de compras de cada producto

    return total_quantities

#crea un diccionario con las fechas y cantidades de productos comprados en esta fecha
def articles_interval_time(transactions,id):
    # Crear un diccionario para almacenar la cantidad total de compras de cada producto
    total_quantities = {}
    dates={}
    quantitis_id=0
    for transaction in transactions:
        articles_list = transaction.articles.split(",")
        date=transaction.date_of_purchase
        for article in articles_list:
            
            articles = article.replace('{', '')
            articles = articles.replace('}', '')
            articles = articles.replace("'", "")
            article_id, quantity = articles.split(":")
            article_id = article_id.strip()
            quantity = int(quantity.strip()) 
            
            if article_id == id:    
                if article_id in total_quantities:
                    quantitis_id=quantity
                    total_quantities[article_id].append(quantity)
                else:
                    quantitis_id=quantity
                    total_quantities[article_id] = [quantity]
       
                if date in dates:
                    
                    dates[date]+= quantitis_id
                else:
                    
                    dates[date] = quantitis_id
            
    # Devolver el diccionario con la cantidad total de compras de cada producto
   
    return total_quantities,dates


#crea un diccionario con las fechas y nos muestra 0 o la cantidad de ventas por dia.
def dias_compras(transactions,numdays,id):
    from datetime import datetime, timedelta
    resultado = articles_interval_time(transactions,id)
    article_cant = resultado[0]
    dates_cant = resultado[1]
    
    date_dict = {}
    today = datetime.now()
    interval = today - timedelta(days=numdays)

    for i in range(1,numdays+1):
        day = interval + timedelta(days=i)
        date_dict[day.date()] = 0

    for date,cant in dates_cant.items():
        if date in date_dict:
            date_dict[date]=cant

    return date_dict
    
#retorna un diccionario que contiene la fecha y ganancias por dia
def amount_interval(transactions):
    # Crear un diccionario para almacenar la cantidad total de compras de cada producto
    dict_dates={}
    for transaction in transactions:
        total_amount = transaction.total_amount
        date=transaction.date_of_purchase
        
        if date in dict_dates:
            dict_dates[date]+= total_amount
        else:
            dict_dates[date] = total_amount
            
    # Devolver el diccionario con la cantidad total de compras de cada producto. para el admin statisc
   
    return dict_dates

#retorna un diccionario que contiene la fecha y ganancias por dia
def amount_id(id):
    from .models import ProductInformation,Venta
    price_product=ProductInformation.objects.get(pk=id)
    price_product=price_product.price_product
    transactions=Venta.objects.all()
    # Crear un diccionario para almacenar la cantidad total de compras de cada producto
    dict_total_shipping = {}
    dict_total_amount={}

    for transaction in transactions:
        articles_list = transaction.articles.split(",")
        
        for article in articles_list:

            articles = article.replace('{', '')
            articles = articles.replace('}', '')
            articles = articles.replace("'", "")
            article_id, quantity = articles.split(":")
            article_id = article_id.strip()
            quantity = int(quantity.strip()) 
            
            if article_id == id:    
                if article_id in dict_total_shipping:
                    dict_total_shipping[article_id]+=quantity
                else:
                    dict_total_shipping[article_id] = quantity
    dict_total_amount[id]=dict_total_shipping[id]*price_product
    

            
    # Devolver el diccionario con la cantidad total de compras de cada producto
   
    return dict_total_amount


#crea un diccionario con las fechas y nos muestra 0 o la cantidad de dinero por dia. para el admin statisc
def dias_amount(transactions,numdays):
    from datetime import datetime, timedelta
    dict_total_amount = amount_interval(transactions)
    date_dict = {}
    today = datetime.now()
    interval = today - timedelta(days=numdays)
    if numdays==365:
        for i in range(1, 365, 30):

            day = interval + timedelta(days=i)
            month=day.strftime('%Y-%m')
            date_dict[month] = 0
        

    else:
        for i in range(1,numdays+1):
            day = interval + timedelta(days=i)
            date_dict[day.date()] = 0



    for date,amount in dict_total_amount.items():
        if numdays==365:
            month_year=date.strftime('%Y-%m')
            print(month_year)
            if month_year in date_dict:
                date_dict[month_year]+=amount

        else:
            if date in date_dict:
                date_dict[date]=amount
    print(date_dict)
    return date_dict


#retorna un diccionario que contiene la cantidad de productos comprados por transferencia 
def cant_product_transaction(transactions):
    # Crear un diccionario para almacenar la cantidad total de compras de cada producto
    cant_product={}

    for transaction in transactions:
        articles_list = transaction.articles.split(",")
        cant=0
        for article in articles_list:

            articles = article.replace('{', '')
            articles = articles.replace('}', '')
            articles = articles.replace("'", "")
            article_id, quantity = articles.split(":")
            article_id = article_id.strip()
            quantity = int(quantity.strip()) 
            
            cant+= quantity
        cant_product[transaction.id] =  cant
            
    # Devolver el diccionario con la cantidad total de compras de cada producto. para el admin statisc
   
    return cant_product

#retorna un diccionario con la cantidad y el id de articulos comprados en una transferencia en especifico
def information_transaction(idtransaction):
    from .models import Venta
    transactions= Venta.objects.get(pk=idtransaction)


    # Crear un diccionario para almacenar la cantidad total de compras de cada producto
    producsShopping = {}
    articles=transactions.articles
    articles_list = articles.split(",")
    for article in articles_list:
        articles = article.replace('{', '')
        articles = articles.replace('}', '')
        articles = articles.replace("'", "")
        article_id, quantity = articles.split(":")
        article_id = int(article_id.strip())
        quantity = int(quantity.strip())
        if article_id in producsShopping:
            producsShopping[article_id] += quantity
        else:
            producsShopping[article_id] = quantity
    # Devolver el diccionario con la cantidad total de compras de cada producto
    print(producsShopping)
    return producsShopping