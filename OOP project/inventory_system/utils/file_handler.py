import json
from datetime import date
from models.product import Product
from models.offer import Offer
from models.client import Client
from models.order import Order
def save_products(products, filename="data/products.json"):
    data = []
    for p in products:
        data.append({
            "id": p.get_id(),
            "name": p.get_name(),
            "category": p.get_category(),
            "production_date": str(p.get_production_date()),
            "expiration_date": str(p.get_expiration_date()),
            "quantity": p.get_quantity(),
            "price": p.get_price()
        })

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_products(filename="data/products.json"):
    products = []
    try:
        with open(filename, "r") as f:
            data = json.load(f)

            for item in data:
                product = Product(
                    id=item["id"],
                    name=item["name"],
                    category=item["category"],
                    productionDate=date.fromisoformat(item["production_date"]),
                    expirationDate=date.fromisoformat(item["expiration_date"]),
                    quantity=item["quantity"],
                    price=item["price"]
                )
                products.append(product)

    except FileNotFoundError:
        pass

    return products


def save_clients(clients, filename="data/clients.json"):
    data = []
    for c in clients:
        data.append({
            "id": c.id,
            "name": c.name,
            "email": c.email,
            "phone": c.phone
        })

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)



def load_clients(filename="data/clients.json"):
    clients = []
    try:
        with open(filename, "r") as f:
            data = json.load(f)

            for item in data:
                client = Client(
                    name=item["name"],
                    email=item["email"],
                    phone=item["phone"],
                    id=item["id"]
                )
                clients.append(client)

    except FileNotFoundError:
        pass

    return clients

def save_orders(orders, filename="data/orders.json"):
    data = []
    for o in orders:
        data.append({
            "id": o.id,
            "client_id": o.client_id,
            "product_id": o.product_id,
            "quantity": o.quantity,
            "date": str(o.date),
            "total": o.total
        })

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)



def load_orders(filename="data/orders.json"):
    orders = []
    try:
        with open(filename, "r") as f:
            data = json.load(f)

            for item in data:
                order = Order(
                    client_id=item["client_id"],
                    product_id=item["product_id"],
                    quantity=item["quantity"],
                    total_amount=item["total"],
                    order_date=date.fromisoformat(item["date"]),
                    id=item["id"]
                )
                orders.append(order)

    except FileNotFoundError:
        pass

    return orders

def save_categories(categories, filename="data/categories.json"):
    data = []
    for c in categories:
        data.append({
            "id": c.id,
            "name": c.get_name()
        })

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

from models.category import Category

def load_categories(filename="data/categories.json"):
    categories = []
    try:
        with open(filename, "r") as f:
            data = json.load(f)

            for item in data:
                category = Category(
                    name=item["name"],
                    id=item["id"]
                )
                categories.append(category)

    except FileNotFoundError:
        pass

    return categories

def save_offers(offers, filename="data/offers.json"):
    data = []
    for o in offers:
        data.append({
            "product_id": o.get_product_id(),
            "discount": o.get_discount(),
            "start_date": str(o.get_start_date()),
            "end_date": str(o.get_end_date())
        })

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


from models.offer import Offer

def load_offers(filename="data/offers.json"):
    offers = []
    try:
        with open(filename, "r") as f:
            data = json.load(f)

            for item in data:
                offer = Offer(
                    product_id=item["product_id"],
                    discount=item["discount"],
                    start_date=date.fromisoformat(item["start_date"]),
                    end_date=date.fromisoformat(item["end_date"])
                )
                offers.append(offer)

    except FileNotFoundError:
        pass

    return offers