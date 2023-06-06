from django.forms import ModelForm
from .models import Venta

class TransactionForm(ModelForm):


    class Meta:
        model= Venta
        fields= "__all__"
        exclude=('articles','status')
