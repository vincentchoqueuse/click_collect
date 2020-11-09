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
        total_price = 0
        market = Market.objects.get(pk=market_pk)
        for form in formset:
            product_pk = form.cleaned_data["product_pk"]
            quantity = form.cleaned_data["quantity"]
            product = Product.objects.get(pk=product_pk)
            total_product_price = float(quantity)*product.price
            total_price += total_product_price
            data.append({"product_pk":product_pk,"name":product.name,"quantity":quantity,"unit":product.unit,"price":product.price,"total_price":total_product_price})

        self.cart[str(market_pk)] = {"name": market.name,"products":data,"total_price": total_price}
        self.session.update({"cart":self.cart})

    def get_market(self,market_pk):
        if self.cart.get(str(market_pk)) is None:
            market = Market.objects.get(pk=market_pk)
            products = []
            for item in Item.objects.filter(market=market):
                products.append({'product_pk':item.product.pk,'quantity':0})
            data = {"name": market.name,"products":products,"total_price": 0}
        else:
            data = self.cart[str(market_pk)]
        return data

    def total_price(self):
        price = 0
        for market_id,market_data in self.cart.items() :
            price +=  float(market_data["total_price"])
        return price

    def save(self,form):
        for market_id,market_data in self.cart.items() :
            bucket = Bucket(market_id = market_id,client_name=form.cleaned_data["name"],email=form.cleaned_data["email"])
            bucket.save()
            for item in market_data["product"]:
                bucket_item = BucketItem(bucket=bucket,product_id=item["product_pk"],quantity=item["quantity"],price=item["price"])
                bucket_item.save()
        self.cart = {}
        self.session.pop("cart")
