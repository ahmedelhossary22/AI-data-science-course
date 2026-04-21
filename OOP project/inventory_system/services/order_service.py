from models.order import Order

class OrderService:
    def __init__(self):
        self._orders = []

    def add_order(self, order):
        self._orders.append(order)

    def get_all_orders(self):
        return self._orders.copy()

    def find_order_by_id(self, order_id):
        for order in self._orders:
            if order.id == order_id:
                return order
        return None

    def get_orders_by_client(self, client_id):
        return [
            o for o in self._orders
            if o.client_id == client_id
        ]

    def delete_order(self, order_id):
        original_len = len(self._orders)
        self._orders = [o for o in self._orders if o.id != order_id]
        return len(self._orders) < original_len
    
    def place_order(self, client_id, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        if product.get_quantity() < quantity:
            raise ValueError("Not enough stock")

        total = quantity * product.get_effective_price()

        order = Order(
        client_id=client_id,
        product_id=product.get_id(),
        quantity=quantity,
        total_amount=total
        )

        product.set_quantity(product.get_quantity() - quantity)

        self._orders.append(order)

        return order
