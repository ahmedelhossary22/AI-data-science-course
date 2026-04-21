import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
import json
import os
import sys

# Add inventory_system folder to path so 'models' package is found
_HERE = os.path.dirname(os.path.abspath(__file__))          # .../inventory_system/GUI
_ROOT = os.path.dirname(_HERE)                               # .../inventory_system
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from models.product import Product
from models.category import Category
from models.supplier import Supplier
from models.client import Client
from models.order import Order
from models.offer import Offer

DATA_DIR = os.path.join(_ROOT, "data")


# ─── FILE HELPERS ────────────────────────────────────────────────────────────

def _path(filename):
    return os.path.join(DATA_DIR, filename)

def save_products(products):
    data = [{"id": p.get_id(), "name": p.get_name(), "category": p.get_category(),
             "production_date": str(p.get_production_date()),
             "expiration_date": str(p.get_expiration_date()),
             "quantity": p.get_quantity(), "price": p.get_price()} for p in products]
    with open(_path("products.json"), "w") as f:
        json.dump(data, f, indent=4)

def load_products():
    products = []
    try:
        with open(_path("products.json")) as f:
            for item in json.load(f):
                products.append(Product(
                    id=item["id"], name=item["name"], category=item["category"],
                    productionDate=date.fromisoformat(item["production_date"]),
                    expirationDate=date.fromisoformat(item["expiration_date"]),
                    quantity=item["quantity"], price=item["price"]))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return products

def save_clients(clients):
    data = [{"id": c.id, "name": c.name, "email": c.email, "phone": c.phone} for c in clients]
    with open(_path("clients.json"), "w") as f:
        json.dump(data, f, indent=4)

def load_clients():
    clients = []
    try:
        with open(_path("clients.json")) as f:
            for item in json.load(f):
                clients.append(Client(name=item["name"], email=item["email"],
                                      phone=item["phone"], id=item["id"]))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return clients

def save_orders(orders):
    data = [{"id": o.id, "client_id": o.client_id, "product_id": o.product_id,
             "quantity": o.quantity, "date": str(o.date), "total": o.total} for o in orders]
    with open(_path("orders.json"), "w") as f:
        json.dump(data, f, indent=4)

def load_orders():
    orders = []
    try:
        with open(_path("orders.json")) as f:
            for item in json.load(f):
                orders.append(Order(client_id=item["client_id"], product_id=item["product_id"],
                                    quantity=item["quantity"], total_amount=item["total"],
                                    order_date=date.fromisoformat(item["date"]), id=item["id"]))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return orders

def save_categories(categories):
    data = [{"id": c.id, "name": c.get_name()} for c in categories]
    with open(_path("categories.json"), "w") as f:
        json.dump(data, f, indent=4)

def load_categories():
    categories = []
    try:
        with open(_path("categories.json")) as f:
            for item in json.load(f):
                categories.append(Category(name=item["name"], id=item["id"]))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return categories

def save_suppliers(suppliers):
    data = [{"id": s.id, "name": s.name, "email": s.email} for s in suppliers]
    with open(_path("suppliers.json"), "w") as f:
        json.dump(data, f, indent=4)

def load_suppliers():
    suppliers = []
    try:
        with open(_path("suppliers.json")) as f:
            for item in json.load(f):
                suppliers.append(Supplier(name=item["name"], email=item["email"], id=item["id"]))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return suppliers

def save_offers(offers):
    data = [{"product_id": o.get_product_id(), "discount": o.get_discount(),
             "start_date": str(o.get_start_date()), "end_date": str(o.get_end_date())} for o in offers]
    with open(_path("offers.json"), "w") as f:
        json.dump(data, f, indent=4)

def load_offers():
    offers = []
    try:
        with open(_path("offers.json")) as f:
            for item in json.load(f):
                offers.append(Offer(product_id=item["product_id"], discount=item["discount"],
                                    start_date=date.fromisoformat(item["start_date"]),
                                    end_date=date.fromisoformat(item["end_date"])))
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return offers


# ─── MAIN APP ────────────────────────────────────────────────────────────────

class InventoryApp:
    def __init__(self):
        # Load all data
        self.products = load_products()
        self.categories = load_categories()
        self.suppliers = load_suppliers()
        self.clients = load_clients()
        self.orders = load_orders()
        self.offers = load_offers()
        self._assign_offers()
        self._clean_data()

        # Build window
        self.root = tk.Tk()
        self.root.title("Inventory Management System")
        self.root.geometry("900x600")
        self.root.resizable(True, True)

        # Frame container (simulates CardLayout)
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)
        self.current_frame = None

        self.show_main_menu()
        self.root.mainloop()

    # ── Data helpers ──────────────────────────────────────────────────────────

    def _assign_offers(self):
        for p in self.products:
            p.set_offer(None)
        for offer in self.offers:
            p = self._find_product(offer.get_product_id())
            if p:
                p.set_offer(offer)

    def _clean_data(self):
        cat_names = {c.get_name().lower() for c in self.categories}
        self.products = [p for p in self.products if p.get_category().lower() in cat_names]

    def _find_product(self, pid):
        for p in self.products:
            if p.get_id() == pid:
                return p
        return None

    def _find_client(self, cid):
        for c in self.clients:
            if c.id == cid:
                return c
        return None

    # ── Frame switching ───────────────────────────────────────────────────────

    def _show_frame(self, frame):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = frame
        frame.pack(fill="both", expand=True)

    # ═══════════════════════════════════════════════════════════════════
    #  MAIN MENU
    # ═══════════════════════════════════════════════════════════════════

    def show_main_menu(self):
        frame = tk.Frame(self.container, padx=20, pady=20)

        title = tk.Label(frame, text="Inventory Management System",
                         font=("Arial", 24, "bold"))
        title.pack(pady=(20, 40))

        btn_frame = tk.Frame(frame)
        btn_frame.pack(expand=True)

        tk.Button(btn_frame, text="Admin", font=("Arial", 18), width=20, height=2,
                  command=self.show_admin_panel).pack(pady=10)
        tk.Button(btn_frame, text="Client", font=("Arial", 18), width=20, height=2,
                  command=self.show_client_panel).pack(pady=10)

        self._show_frame(frame)

    # ═══════════════════════════════════════════════════════════════════
    #  ADMIN PANEL
    # ═══════════════════════════════════════════════════════════════════

    def show_admin_panel(self):
        frame = tk.Frame(self.container, padx=10, pady=10)

        tk.Label(frame, text="Admin Dashboard", font=("Arial", 16, "bold")).pack(pady=10)

        menu_frame = tk.Frame(frame)
        menu_frame.pack(expand=True)

        items = [
            ("Product Management",   self.show_product_management),
            ("Category Management",  self.show_category_management),
            ("Supplier Management",  self.show_supplier_management),
            ("Manage Offers",        self.show_offer_management),
            ("View Reports",         self.show_reports),
            ("Expiry Notifications", self.show_expiry_notifications),
            ("Back to Main Menu",    self.show_main_menu),
        ]
        for text, cmd in items:
            tk.Button(menu_frame, text=text, font=("Arial", 12), width=25, height=1,
                      command=cmd).pack(pady=4)

        self._show_frame(frame)

    # ═══════════════════════════════════════════════════════════════════
    #  CLIENT PANEL
    # ═══════════════════════════════════════════════════════════════════

    def show_client_panel(self):
        frame = tk.Frame(self.container, padx=10, pady=10)

        tk.Label(frame, text="Client Dashboard", font=("Arial", 16, "bold")).pack(pady=10)

        menu_frame = tk.Frame(frame)
        menu_frame.pack(expand=True)

        items = [
            ("Register New Client",  self.show_client_registration),
            ("Existing Client Login", self.show_client_login),
            ("View Products",        self.show_client_product_view),
            ("Back to Main Menu",    self.show_main_menu),
        ]
        for text, cmd in items:
            tk.Button(menu_frame, text=text, font=("Arial", 12), width=25, height=1,
                      command=cmd).pack(pady=4)

        self._show_frame(frame)

    # ═══════════════════════════════════════════════════════════════════
    #  PRODUCT MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════

    def show_product_management(self):
        frame = tk.Frame(self.container)

        tk.Label(frame, text="Product Management", font=("Arial", 14, "bold")).pack(pady=5)

        cols = ("ID", "Name", "Category", "Prod Date", "Exp Date", "Qty", "Price", "Offer")
        tree = self._make_table(frame, cols)
        self._refresh_product_table(tree)

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", padx=5, pady=5)

        tk.Button(btn_frame, text="Add Product",    command=lambda: self._dlg_add_product(tree)).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Update Qty",     command=lambda: self._dlg_update_qty(tree)).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Delete Product", command=lambda: self._delete_product(tree)).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Search",         command=lambda: self._dlg_search(tree)).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Edit Offer",     command=lambda: self._dlg_edit_offer(tree, refresh_fn=lambda: self._refresh_product_table(tree))).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Back",           command=self.show_admin_panel).pack(side="right", padx=3)

        self._show_frame(frame)

    def _refresh_product_table(self, tree):
        for row in tree.get_children():
            tree.delete(row)
        for p in self.products:
            o = p.get_offer()
            offer_text = "No Offer"
            if o and o.is_active_today():
                offer_text = f"{o.get_discount()*100:.0f}% off until {o.get_end_date()}"
            tree.insert("", "end", values=(
                p.get_id(), p.get_name(), p.get_category(),
                p.get_production_date(), p.get_expiration_date(),
                p.get_quantity(), f"${p.get_price():.2f}", offer_text))

    def _dlg_add_product(self, tree):
        dlg = tk.Toplevel(self.root)
        dlg.title("Add New Product")
        dlg.geometry("400x320")
        dlg.grab_set()

        fields = {}
        rows = [
            ("Product ID:", "id"),
            ("Name:", "name"),
            ("Production Date (yyyy-mm-dd):", "prod_date"),
            ("Expiration Date (yyyy-mm-dd):", "exp_date"),
            ("Quantity:", "qty"),
            ("Price:", "price"),
        ]
        for i, (label, key) in enumerate(rows):
            tk.Label(dlg, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=3)
            default = ""
            if key == "prod_date":
                default = str(date.today())
            elif key == "exp_date":
                default = str(date.today().replace(year=date.today().year + 1))
            elif key == "qty":
                default = "1"
            elif key == "price":
                default = "0.00"
            e = tk.Entry(dlg)
            e.insert(0, default)
            e.grid(row=i, column=1, sticky="w", padx=5, pady=3)
            fields[key] = e

        # Category dropdown
        tk.Label(dlg, text="Category:").grid(row=len(rows), column=0, sticky="e", padx=5, pady=3)
        cat_var = tk.StringVar()
        cat_names = [c.get_name() for c in self.categories]
        cat_combo = ttk.Combobox(dlg, textvariable=cat_var, values=cat_names, state="readonly")
        if cat_names:
            cat_combo.current(0)
        cat_combo.grid(row=len(rows), column=1, sticky="w", padx=5, pady=3)

        def save():
            try:
                pid = int(fields["id"].get().strip())
                name = fields["name"].get().strip()
                category = cat_var.get()
                prod_date = date.fromisoformat(fields["prod_date"].get().strip())
                exp_date = date.fromisoformat(fields["exp_date"].get().strip())
                qty = int(fields["qty"].get().strip())
                price = float(fields["price"].get().strip())
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please check all fields.", parent=dlg)
                return

            if self._find_product(pid):
                messagebox.showerror("Error", "Product ID already exists.", parent=dlg)
                return
            if prod_date > exp_date:
                messagebox.showerror("Error", "Production date must be before expiration date.", parent=dlg)
                return

            self.products.append(Product(id=pid, name=name, category=category,
                                         productionDate=prod_date, expirationDate=exp_date,
                                         quantity=qty, price=price))
            save_products(self.products)
            self._refresh_product_table(tree)
            dlg.destroy()

        btn_row = len(rows) + 1
        tk.Button(dlg, text="Save",   command=save).grid(row=btn_row, column=0, pady=8)
        tk.Button(dlg, text="Cancel", command=dlg.destroy).grid(row=btn_row, column=1, pady=8)

    def _dlg_update_qty(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Error", "Please select a product first.")
            return
        pid = int(tree.item(sel[0])["values"][0])
        p = self._find_product(pid)

        dlg = tk.Toplevel(self.root)
        dlg.title("Update Quantity")
        dlg.geometry("280x130")
        dlg.grab_set()

        tk.Label(dlg, text="Current Quantity:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tk.Label(dlg, text=str(p.get_quantity())).grid(row=0, column=1, sticky="w", padx=5)
        tk.Label(dlg, text="New Quantity:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        qty_var = tk.StringVar(value=str(p.get_quantity()))
        tk.Entry(dlg, textvariable=qty_var).grid(row=1, column=1, sticky="w", padx=5)

        def update():
            try:
                new_qty = int(qty_var.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number.", parent=dlg)
                return
            if new_qty < 0:
                messagebox.showerror("Error", "Quantity cannot be negative.", parent=dlg)
                return
            p.set_quantity(new_qty)
            save_products(self.products)
            self._refresh_product_table(tree)
            dlg.destroy()

        tk.Button(dlg, text="Update", command=update).grid(row=2, column=0, pady=8)
        tk.Button(dlg, text="Cancel", command=dlg.destroy).grid(row=2, column=1, pady=8)

    def _delete_product(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Error", "Please select a product first.")
            return
        pid = int(tree.item(sel[0])["values"][0])
        self.products = [p for p in self.products if p.get_id() != pid]
        save_products(self.products)
        self._refresh_product_table(tree)
        messagebox.showinfo("Info", "Product deleted successfully.")

    def _dlg_search(self, tree):
        dlg = tk.Toplevel(self.root)
        dlg.title("Search Products")
        dlg.geometry("300x160")
        dlg.grab_set()

        tk.Label(dlg, text="Search by name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        name_var = tk.StringVar()
        tk.Entry(dlg, textvariable=name_var).grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(dlg, text="Search by category:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        cat_var = tk.StringVar()
        cat_names = ["All Categories"] + [c.get_name() for c in self.categories]
        cat_combo = ttk.Combobox(dlg, textvariable=cat_var, values=cat_names, state="readonly")
        cat_combo.current(0)
        cat_combo.grid(row=1, column=1, sticky="w", padx=5)

        def search():
            name_q = name_var.get().lower()
            cat_q = cat_var.get()
            if cat_q == "All Categories":
                cat_q = ""

            for row in tree.get_children():
                tree.delete(row)

            found = False
            for p in self.products:
                if (not name_q or name_q in p.get_name().lower()) and \
                   (not cat_q or p.get_category().lower() == cat_q.lower()):
                    o = p.get_offer()
                    offer_text = "No Offer"
                    if o and o.is_active_today():
                        offer_text = f"{o.get_discount()*100:.0f}% off until {o.get_end_date()}"
                    tree.insert("", "end", values=(
                        p.get_id(), p.get_name(), p.get_category(),
                        p.get_production_date(), p.get_expiration_date(),
                        p.get_quantity(), f"${p.get_price():.2f}", offer_text))
                    found = True

            if not found:
                tree.insert("", "end", values=("No products found", "", "", "", "", "", "", ""))
            dlg.destroy()

        tk.Button(dlg, text="Search", command=search).grid(row=2, column=0, columnspan=2, pady=10)

    # ═══════════════════════════════════════════════════════════════════
    #  CATEGORY MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════

    def show_category_management(self):
        frame = tk.Frame(self.container)

        tk.Label(frame, text="Category Management", font=("Arial", 14, "bold")).pack(pady=5)

        cols = ("ID", "Name")
        tree = self._make_table(frame, cols)
        self._refresh_category_table(tree)

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", padx=5, pady=5)

        tk.Button(btn_frame, text="Add Category",    command=lambda: self._dlg_add_category(tree)).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Delete Category", command=lambda: self._delete_category(tree)).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Back",            command=self.show_admin_panel).pack(side="right", padx=3)

        self._show_frame(frame)

    def _refresh_category_table(self, tree):
        for row in tree.get_children():
            tree.delete(row)
        for c in self.categories:
            tree.insert("", "end", values=(c.id, c.get_name()))

    def _dlg_add_category(self, tree):
        dlg = tk.Toplevel(self.root)
        dlg.title("Add New Category")
        dlg.geometry("280x110")
        dlg.grab_set()

        tk.Label(dlg, text="Category Name:").grid(row=0, column=0, sticky="e", padx=5, pady=8)
        name_var = tk.StringVar()
        tk.Entry(dlg, textvariable=name_var).grid(row=0, column=1, sticky="w", padx=5)

        def save():
            name = name_var.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a category name.", parent=dlg)
                return
            self.categories.append(Category(name=name))
            save_categories(self.categories)
            self._refresh_category_table(tree)
            dlg.destroy()

        tk.Button(dlg, text="Save",   command=save).grid(row=1, column=0, pady=8)
        tk.Button(dlg, text="Cancel", command=dlg.destroy).grid(row=1, column=1, pady=8)

    def _delete_category(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Error", "Please select a category first.")
            return
        cid = int(tree.item(sel[0])["values"][0])
        self.categories = [c for c in self.categories if c.id != cid]
        save_categories(self.categories)
        self._refresh_category_table(tree)
        messagebox.showinfo("Info", "Category deleted successfully.")

    # ═══════════════════════════════════════════════════════════════════
    #  SUPPLIER MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════

    def show_supplier_management(self):
        frame = tk.Frame(self.container)

        tk.Label(frame, text="Supplier Management", font=("Arial", 14, "bold")).pack(pady=5)

        cols = ("ID", "Name", "Email")
        tree = self._make_table(frame, cols)
        self._refresh_supplier_table(tree)

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", padx=5, pady=5)

        tk.Button(btn_frame, text="Add Supplier",    command=lambda: self._dlg_add_supplier(tree)).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Delete Supplier", command=lambda: self._delete_supplier(tree)).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Back",            command=self.show_admin_panel).pack(side="right", padx=3)

        self._show_frame(frame)

    def _refresh_supplier_table(self, tree):
        for row in tree.get_children():
            tree.delete(row)
        for s in self.suppliers:
            tree.insert("", "end", values=(s.id, s.name, s.email))

    def _dlg_add_supplier(self, tree):
        dlg = tk.Toplevel(self.root)
        dlg.title("Add New Supplier")
        dlg.geometry("300x140")
        dlg.grab_set()

        tk.Label(dlg, text="Supplier Name:").grid(row=0, column=0, sticky="e", padx=5, pady=6)
        name_var = tk.StringVar()
        tk.Entry(dlg, textvariable=name_var).grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(dlg, text="Email:").grid(row=1, column=0, sticky="e", padx=5, pady=6)
        email_var = tk.StringVar()
        tk.Entry(dlg, textvariable=email_var).grid(row=1, column=1, sticky="w", padx=5)

        def save():
            name = name_var.get().strip()
            email = email_var.get().strip()
            if not name or not email:
                messagebox.showerror("Error", "Please fill all fields.", parent=dlg)
                return
            self.suppliers.append(Supplier(name=name, email=email))
            save_suppliers(self.suppliers)
            self._refresh_supplier_table(tree)
            dlg.destroy()

        tk.Button(dlg, text="Save",   command=save).grid(row=2, column=0, pady=8)
        tk.Button(dlg, text="Cancel", command=dlg.destroy).grid(row=2, column=1, pady=8)

    def _delete_supplier(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Error", "Please select a supplier first.")
            return
        sid = int(tree.item(sel[0])["values"][0])
        self.suppliers = [s for s in self.suppliers if s.id != sid]
        save_suppliers(self.suppliers)
        self._refresh_supplier_table(tree)
        messagebox.showinfo("Info", "Supplier deleted successfully.")

    # ═══════════════════════════════════════════════════════════════════
    #  OFFER MANAGEMENT
    # ═══════════════════════════════════════════════════════════════════

    def show_offer_management(self):
        frame = tk.Frame(self.container)

        tk.Label(frame, text="Offer Management", font=("Arial", 14, "bold")).pack(pady=5)

        cols = ("Product ID", "Product Name", "Current Offer", "Discount (%)", "Start Date", "End Date")
        tree = self._make_table(frame, cols)
        self._refresh_offer_table(tree)

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", padx=5, pady=5)

        tk.Button(btn_frame, text="Add Offer",    command=lambda: self._dlg_add_offer(tree)).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Edit Offer",   command=lambda: self._dlg_edit_offer(tree, refresh_fn=lambda: self._refresh_offer_table(tree))).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Delete Offer", command=lambda: self._delete_offer(tree)).pack(side="left", padx=3)
        tk.Button(btn_frame, text="Back",         command=self.show_admin_panel).pack(side="right", padx=3)

        self._show_frame(frame)

    def _refresh_offer_table(self, tree):
        for row in tree.get_children():
            tree.delete(row)
        for p in self.products:
            o = p.get_offer()
            if o:
                status = "Active" if o.is_active_today() else "Inactive"
                tree.insert("", "end", values=(
                    p.get_id(), p.get_name(), status,
                    f"{o.get_discount()*100:.2f}",
                    str(o.get_start_date()), str(o.get_end_date())))
            else:
                tree.insert("", "end", values=(p.get_id(), p.get_name(), "No Offer", "", "", ""))

    def _dlg_add_offer(self, offer_tree):
        dlg = tk.Toplevel(self.root)
        dlg.title("Add New Offer")
        dlg.geometry("400x240")
        dlg.grab_set()

        tk.Label(dlg, text="Product:").grid(row=0, column=0, sticky="e", padx=5, pady=6)
        prod_var = tk.StringVar()
        prod_options = [f"{p.get_id()} - {p.get_name()}" for p in self.products]
        prod_combo = ttk.Combobox(dlg, textvariable=prod_var, values=prod_options, state="readonly", width=28)
        if prod_options:
            prod_combo.current(0)
        prod_combo.grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(dlg, text="Discount % (e.g. 15):").grid(row=1, column=0, sticky="e", padx=5, pady=6)
        disc_var = tk.StringVar()
        tk.Entry(dlg, textvariable=disc_var).grid(row=1, column=1, sticky="w", padx=5)

        tk.Label(dlg, text="Start Date (yyyy-mm-dd):").grid(row=2, column=0, sticky="e", padx=5, pady=6)
        start_var = tk.StringVar(value=str(date.today()))
        tk.Entry(dlg, textvariable=start_var).grid(row=2, column=1, sticky="w", padx=5)

        tk.Label(dlg, text="End Date (yyyy-mm-dd):").grid(row=3, column=0, sticky="e", padx=5, pady=6)
        end_var = tk.StringVar(value=str(date.today() + timedelta(days=30)))
        tk.Entry(dlg, textvariable=end_var).grid(row=3, column=1, sticky="w", padx=5)

        def save():
            try:
                sel = prod_var.get()
                if not sel:
                    messagebox.showerror("Error", "Please select a product.", parent=dlg)
                    return
                pid = int(sel.split(" - ")[0])
                disc_val = float(disc_var.get().strip())
                if not (0 < disc_val < 100):
                    messagebox.showerror("Error", "Discount must be >0 and <100%.", parent=dlg)
                    return
                discount = disc_val / 100.0
                start_date = date.fromisoformat(start_var.get().strip())
                end_date = date.fromisoformat(end_var.get().strip())
                if start_date > end_date:
                    messagebox.showerror("Error", "Start date must be before end date.", parent=dlg)
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid input, please check all fields.", parent=dlg)
                return

            self.offers = [o for o in self.offers if o.get_product_id() != pid]
            new_offer = Offer(product_id=pid, discount=discount, start_date=start_date, end_date=end_date)
            self.offers.append(new_offer)
            p = self._find_product(pid)
            if p:
                p.set_offer(new_offer)
            save_offers(self.offers)
            self._refresh_offer_table(offer_tree)
            dlg.destroy()

        tk.Button(dlg, text="Save",   command=save).grid(row=4, column=0, pady=10)
        tk.Button(dlg, text="Cancel", command=dlg.destroy).grid(row=4, column=1, pady=10)

    def _dlg_edit_offer(self, tree, refresh_fn=None):
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Error", "Please select a product first.")
            return

        pid = int(tree.item(sel[0])["values"][0])
        p = self._find_product(pid)
        if not p:
            return
        offer = p.get_offer()

        dlg = tk.Toplevel(self.root)
        dlg.title("Edit Offer")
        dlg.geometry("400x240")
        dlg.grab_set()

        tk.Label(dlg, text="Product:").grid(row=0, column=0, sticky="e", padx=5, pady=6)
        tk.Label(dlg, text=f"{pid} - {p.get_name()}").grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(dlg, text="Discount % (e.g. 15):").grid(row=1, column=0, sticky="e", padx=5, pady=6)
        disc_var = tk.StringVar(value=str(offer.get_discount() * 100) if offer else "")
        tk.Entry(dlg, textvariable=disc_var).grid(row=1, column=1, sticky="w", padx=5)

        tk.Label(dlg, text="Start Date (yyyy-mm-dd):").grid(row=2, column=0, sticky="e", padx=5, pady=6)
        start_var = tk.StringVar(value=str(offer.get_start_date()) if offer else str(date.today()))
        tk.Entry(dlg, textvariable=start_var).grid(row=2, column=1, sticky="w", padx=5)

        tk.Label(dlg, text="End Date (yyyy-mm-dd):").grid(row=3, column=0, sticky="e", padx=5, pady=6)
        end_var = tk.StringVar(value=str(offer.get_end_date()) if offer else str(date.today() + timedelta(days=30)))
        tk.Entry(dlg, textvariable=end_var).grid(row=3, column=1, sticky="w", padx=5)

        def save():
            try:
                discount = float(disc_var.get().strip()) / 100.0
                if not (0 < discount < 1):
                    messagebox.showerror("Error", "Discount must be >0 and <100%.", parent=dlg)
                    return
                start_date = date.fromisoformat(start_var.get().strip())
                end_date = date.fromisoformat(end_var.get().strip())
                if start_date > end_date:
                    messagebox.showerror("Error", "Start date must be before end date.", parent=dlg)
                    return
            except ValueError:
                messagebox.showerror("Error", "Invalid input, please check all fields.", parent=dlg)
                return

            if offer and offer in self.offers:
                self.offers.remove(offer)
            new_offer = Offer(product_id=pid, discount=discount, start_date=start_date, end_date=end_date)
            self.offers.append(new_offer)
            p.set_offer(new_offer)
            save_offers(self.offers)
            if refresh_fn:
                refresh_fn()
            dlg.destroy()

        tk.Button(dlg, text="Save",   command=save).grid(row=4, column=0, pady=10)
        tk.Button(dlg, text="Cancel", command=dlg.destroy).grid(row=4, column=1, pady=10)

    def _delete_offer(self, tree):
        sel = tree.selection()
        if not sel:
            messagebox.showerror("Error", "Please select a product first.")
            return
        pid = int(tree.item(sel[0])["values"][0])
        p = self._find_product(pid)
        if not p:
            return
        offer = p.get_offer()
        if not offer:
            messagebox.showinfo("Info", "No offer to delete for this product.")
            return
        if offer in self.offers:
            self.offers.remove(offer)
        p.set_offer(None)
        save_offers(self.offers)
        self._refresh_offer_table(tree)
        messagebox.showinfo("Info", "Offer deleted.")

    # ═══════════════════════════════════════════════════════════════════
    #  REPORTS
    # ═══════════════════════════════════════════════════════════════════

    def show_reports(self):
        frame = tk.Frame(self.container)

        tk.Label(frame, text="Reports and Statistics", font=("Arial", 14, "bold")).pack(pady=5)

        text = tk.Text(frame, state="normal", wrap="word", font=("Courier", 11))
        text.pack(fill="both", expand=True, padx=10, pady=5)

        cat_counts = {}
        for p in self.products:
            cat_counts[p.get_category()] = cat_counts.get(p.get_category(), 0) + 1

        text.insert("end", "=== Products per Category ===\n")
        for cat, cnt in cat_counts.items():
            text.insert("end", f"  {cat:<15}: {cnt} product(s)\n")

        revenue = sum(o.total for o in self.orders)
        cost = revenue * 0.70
        profit = revenue - cost
        text.insert("end", "\n=== Profit Report ===\n")
        text.insert("end", f"  Revenue: ${revenue:.2f} | Cost: ${cost:.2f} | Profit: ${profit:.2f}\n")

        text.config(state="disabled")

        tk.Button(frame, text="Back", command=self.show_admin_panel).pack(pady=5)

        self._show_frame(frame)

    # ═══════════════════════════════════════════════════════════════════
    #  EXPIRY NOTIFICATIONS
    # ═══════════════════════════════════════════════════════════════════

    def show_expiry_notifications(self):
        frame = tk.Frame(self.container)

        tk.Label(frame, text="Expiry Notifications", font=("Arial", 14, "bold")).pack(pady=5)

        input_frame = tk.Frame(frame)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Days to expiry threshold:").grid(row=0, column=0, sticky="e", padx=5, pady=4)
        days_var = tk.StringVar(value="30")
        tk.Entry(input_frame, textvariable=days_var, width=8).grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(input_frame, text="Low quantity threshold:").grid(row=1, column=0, sticky="e", padx=5, pady=4)
        qty_var = tk.StringVar(value="10")
        tk.Entry(input_frame, textvariable=qty_var, width=8).grid(row=1, column=1, sticky="w", padx=5)

        text = tk.Text(frame, state="disabled", wrap="word", font=("Courier", 11))
        text.pack(fill="both", expand=True, padx=10, pady=5)

        def check():
            try:
                days = int(days_var.get())
                qty_thresh = int(qty_var.get())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers.")
                return
            today = date.today()
            text.config(state="normal")
            text.delete("1.0", "end")
            found = False
            for p in self.products:
                days_to_exp = (p.get_expiration_date() - today).days
                if days_to_exp <= days or p.get_quantity() <= qty_thresh:
                    text.insert("end", f"⚠ WARNING! {p.get_name()} -> {days_to_exp} day(s) to expire, Qty={p.get_quantity()}\n")
                    found = True
            if not found:
                text.insert("end", "No products nearing expiry or with low quantity.")
            text.config(state="disabled")

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Check Notifications", command=check).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Back", command=self.show_admin_panel).pack(side="left", padx=5)

        self._show_frame(frame)

    # ═══════════════════════════════════════════════════════════════════
    #  CLIENT REGISTRATION
    # ═══════════════════════════════════════════════════════════════════

    def show_client_registration(self):
        frame = tk.Frame(self.container, padx=20, pady=20)

        tk.Label(frame, text="Register New Client", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Name:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        name_var = tk.StringVar()
        tk.Entry(frame, textvariable=name_var, width=25).grid(row=1, column=1, sticky="w", padx=5)

        tk.Label(frame, text="Email:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        email_var = tk.StringVar()
        tk.Entry(frame, textvariable=email_var, width=25).grid(row=2, column=1, sticky="w", padx=5)

        tk.Label(frame, text="Phone:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        phone_var = tk.StringVar()
        tk.Entry(frame, textvariable=phone_var, width=25).grid(row=3, column=1, sticky="w", padx=5)

        def register():
            name = name_var.get().strip()
            email = email_var.get().strip()
            phone = phone_var.get().strip()
            if not name or not email or not phone:
                messagebox.showerror("Error", "Please fill all fields.")
                return
            c = Client(name=name, email=email, phone=phone)
            self.clients.append(c)
            save_clients(self.clients)
            messagebox.showinfo("Success", f"Registered! Your ID is: {c.id}")
            self.show_client_panel()

        tk.Button(frame, text="Register", command=register).grid(row=4, column=0, pady=10)
        tk.Button(frame, text="Back", command=self.show_client_panel).grid(row=4, column=1, pady=10)

        self._show_frame(frame)

    # ═══════════════════════════════════════════════════════════════════
    #  CLIENT LOGIN
    # ═══════════════════════════════════════════════════════════════════

    def show_client_login(self):
        frame = tk.Frame(self.container, padx=20, pady=20)

        tk.Label(frame, text="Client Login", font=("Arial", 14, "bold")).pack(pady=10)

        row = tk.Frame(frame)
        row.pack(pady=10)
        tk.Label(row, text="Enter your client ID:").pack(side="left")
        id_var = tk.StringVar()
        tk.Entry(row, textvariable=id_var, width=10).pack(side="left", padx=5)

        def login():
            try:
                cid = int(id_var.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid ID.")
                return
            client = self._find_client(cid)
            if client:
                self.show_client_dashboard(client)
            else:
                messagebox.showerror("Error", "Client not found.")

        btn_row = tk.Frame(frame)
        btn_row.pack(pady=5)
        tk.Button(btn_row, text="Login", command=login).pack(side="left", padx=5)
        tk.Button(btn_row, text="Back",  command=self.show_client_panel).pack(side="left", padx=5)

        self._show_frame(frame)

    # ═══════════════════════════════════════════════════════════════════
    #  CLIENT PRODUCT VIEW (public, no login)
    # ═══════════════════════════════════════════════════════════════════

    def show_client_product_view(self):
        frame = tk.Frame(self.container)

        tk.Label(frame, text="Available Products", font=("Arial", 14, "bold")).pack(pady=5)

        cols = ("ID", "Name", "Category", "Price", "Qty Available", "Offer")
        tree = self._make_table(frame, cols)

        for p in self.products:
            o = p.get_offer()
            offer_text = "No Offer"
            if o and o.is_active_today():
                offer_text = f"{o.get_discount()*100:.0f}% off until {o.get_end_date()}"
            tree.insert("", "end", values=(
                p.get_id(), p.get_name(), p.get_category(),
                f"${p.get_effective_price():.2f}", p.get_quantity(), offer_text))

        tk.Button(frame, text="Back", command=self.show_client_panel).pack(pady=5)

        self._show_frame(frame)

    # ═══════════════════════════════════════════════════════════════════
    #  CLIENT DASHBOARD
    # ═══════════════════════════════════════════════════════════════════

    def show_client_dashboard(self, client):
        frame = tk.Frame(self.container, padx=10, pady=10)

        tk.Label(frame, text=f"Welcome, {client.name} (ID: {client.id})",
                 font=("Arial", 16, "bold")).pack(pady=10)

        menu_frame = tk.Frame(frame)
        menu_frame.pack(expand=True)

        tk.Button(menu_frame, text="Edit Profile",   width=20, command=lambda: self.show_edit_profile(client)).pack(pady=5)
        tk.Button(menu_frame, text="Place Order",    width=20, command=lambda: self.show_place_order(client)).pack(pady=5)
        tk.Button(menu_frame, text="View My Orders", width=20, command=lambda: self.show_client_orders(client)).pack(pady=5)

        tk.Button(frame, text="Logout", command=self.show_client_panel).pack(pady=10)

        self._show_frame(frame)

    def show_edit_profile(self, client):
        frame = tk.Frame(self.container, padx=20, pady=20)

        tk.Label(frame, text="Edit Profile", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(frame, text="Name:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        name_var = tk.StringVar(value=client.name)
        tk.Entry(frame, textvariable=name_var, width=25).grid(row=1, column=1, sticky="w", padx=5)

        tk.Label(frame, text="Email:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        email_var = tk.StringVar(value=client.email)
        tk.Entry(frame, textvariable=email_var, width=25).grid(row=2, column=1, sticky="w", padx=5)

        tk.Label(frame, text="Phone:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        phone_var = tk.StringVar(value=client.phone)
        tk.Entry(frame, textvariable=phone_var, width=25).grid(row=3, column=1, sticky="w", padx=5)

        def save():
            client.set_name(name_var.get().strip())
            client.set_email(email_var.get().strip())
            client.set_phone(phone_var.get().strip())
            save_clients(self.clients)
            messagebox.showinfo("Success", "Profile updated successfully!")
            self.show_client_dashboard(client)

        tk.Button(frame, text="Save Changes", command=save).grid(row=4, column=0, pady=10)
        tk.Button(frame, text="Cancel", command=lambda: self.show_client_dashboard(client)).grid(row=4, column=1, pady=10)

        self._show_frame(frame)

    def show_place_order(self, client):
        frame = tk.Frame(self.container)

        tk.Label(frame, text="Available Products", font=("Arial", 14, "bold")).pack(pady=5)

        order_frame = tk.Frame(frame)
        order_frame.pack(fill="x", padx=10, pady=3)
        tk.Label(order_frame, text="Product ID:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        pid_var = tk.StringVar()
        tk.Entry(order_frame, textvariable=pid_var, width=10).grid(row=0, column=1, sticky="w", padx=5)
        tk.Label(order_frame, text="Quantity:").grid(row=1, column=0, sticky="e", padx=5, pady=3)
        qty_var = tk.StringVar()
        tk.Entry(order_frame, textvariable=qty_var, width=10).grid(row=1, column=1, sticky="w", padx=5)

        cols = ("ID", "Name", "Category", "Price", "Qty Available")
        tree = self._make_table(frame, cols)
        self._refresh_order_product_table(tree)

        def place():
            try:
                product_id = int(pid_var.get().strip())
                quantity = int(qty_var.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers.")
                return
            p = self._find_product(product_id)
            if not p:
                messagebox.showerror("Error", "Invalid product ID.")
                return
            if p.get_quantity() < quantity:
                messagebox.showerror("Error", "Not enough stock.")
                return
            total = quantity * p.get_effective_price()
            self.orders.append(Order(client_id=client.id, product_id=product_id,
                                     quantity=quantity, total_amount=total))
            save_orders(self.orders)
            p.set_quantity(p.get_quantity() - quantity)
            save_products(self.products)
            messagebox.showinfo("Success", f"Order placed successfully!\n{p.get_name()} x {quantity} = ${total:.2f}")
            self._refresh_order_product_table(tree)

        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Place Order", command=place).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Back", command=lambda: self.show_client_dashboard(client)).pack(side="left", padx=5)

        self._show_frame(frame)

    def _refresh_order_product_table(self, tree):
        for row in tree.get_children():
            tree.delete(row)
        for p in self.products:
            tree.insert("", "end", values=(
                p.get_id(), p.get_name(), p.get_category(),
                f"${p.get_effective_price():.2f}", p.get_quantity()))

    def show_client_orders(self, client):
        frame = tk.Frame(self.container)

        tk.Label(frame, text="Your Orders", font=("Arial", 14, "bold")).pack(pady=5)

        cols = ("Order ID", "Product ID", "Quantity", "Total", "Date")
        tree = self._make_table(frame, cols)

        found = False
        for o in self.orders:
            if o.client_id == client.id:
                tree.insert("", "end", values=(o.id, o.product_id, o.quantity, f"${o.total:.2f}", o.date))
                found = True
        if not found:
            tree.insert("", "end", values=("No orders found", "", "", "", ""))

        tk.Button(frame, text="Back", command=lambda: self.show_client_dashboard(client)).pack(pady=5)

        self._show_frame(frame)

    # ═══════════════════════════════════════════════════════════════════
    #  UTILITY
    # ═══════════════════════════════════════════════════════════════════

    def _make_table(self, parent, columns):
        container = tk.Frame(parent)
        container.pack(fill="both", expand=True, padx=5, pady=5)

        tree = ttk.Treeview(container, columns=columns, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(container, orient="vertical",   command=tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor="center")

        return tree


if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    InventoryApp()