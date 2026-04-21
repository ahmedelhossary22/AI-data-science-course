import os
import sys

# Make sure inventory_system/models is importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "inventory_system"))

from GUI.gui import InventoryApp

if __name__ == "__main__":
    InventoryApp()