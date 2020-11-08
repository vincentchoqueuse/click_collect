from stock.models import Item, Product, Market
from .models import Bucket, BucketItem

class Cart():

    def __init__(self,session):

        if session.get("cart") is None:
            session["cart"]={}  
        self.session = session
        self.cart = self.session["cart"]

    def set_market(self,market_pk,formset):
        data = []
        market = Market.objects.get(pk=market_pk)
        for form in formset:
            product_pk = form.cleaned_data["product_pk"]
            quantity = form.cleaned_data["quantity"]
            product = Product.objects.get(pk=product_pk)
            total_price = float(quantity)*product.price
            data.append({"product_pk":product_pk,"name":product.name,"quantity":quantity,"unit":product.unit,"price":product.price,"total_price":total_price,"market_name":market.name})

        self.cart[str(market_pk)] = data
        self.session.update({"cart":self.cart})

    def get_market(self,market_pk):
        if self.cart.get(str(market_pk)) is None:
            data = []
            for item in Item.objects.filter(market_id=market_pk):
                data.append({'product_pk':item.product.pk,'quantity':0})
        else:
            data = self.cart[str(market_pk)]
        return data

    def total_price(self):
        price = 0
        for market_id,market_data in self.cart.items() :
            for item in market_data:
                price +=  float(item["total_price"])
        return price

    def save(self,form):
        for market_id,market_data in self.cart.items() :
            bucket = Bucket(market_id = market_id,client_name=form.cleaned_data["name"],email=form.cleaned_data["email"])
            bucket.save()
            for item in market_data:
                bucket_item = BucketItem(bucket=bucket,product_id=item["product_pk"],quantity=item["quantity"],price=item["price"])
                bucket_item.save()
        self.cart = {}
        self.session.pop("cart")