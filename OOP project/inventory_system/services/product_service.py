class ProductService:
    def __init__(self):
        self._products = []

    def add_product(self, product):
        self._products.append(product)
    def get_all_products(self):
        return self._products

    def find_product_by_id(self, id):
        for product in self._products:
            if product.get_id() == id:
                return product
        return None
    
    def delete_product(self, product_id):
        self._products = [p for p in self._products if p.get_id() != product_id]

    def update_quantity(self, product_id, new_quantity):
       product= self.find_product_by_id(product_id)
       if product:
           product.set_quantity(new_quantity)
           return True
       return False
    
    def search_by_name(self, name):
        return [product for product in self._products if name.lower() in product.get_name().lower()]
    
    def search_by_category(self, category):
        return [product for product in self._products if product.get_category().lower() == category.lower()]
    
    
    def assign_offers(self, offers):
   
     for product in self._products:
        product.set_offer(None)

        for offer in offers:
            for product in self._products:
                if product.get_id() == offer.get_product_id():
                    product.set_offer(offer)
