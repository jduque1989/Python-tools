import csv
import os

from dotenv import load_dotenv
from tqdm import tqdm
from woocommerce import API

# Load secrets from .env
load_dotenv()

WC_URL = os.getenv("WC_URL")
WC_KEY = os.getenv("WC_KEY")
WC_SECRET = os.getenv("WC_SECRET")

wcapi = API(
    url=WC_URL,
    consumer_key=WC_KEY,
    consumer_secret=WC_SECRET,
    version="wc/v3",
    timeout=60,
)

per_page = 100
fields = "id,sku,name,stock_quantity"

print("Fetching products from WooCommerce...")

products = []
page = 1
while True:
    params = {
        "status": "publish",
        "per_page": per_page,
        "page": page,
        "_fields": fields,
    }
    response = wcapi.get("products", params=params)
    data = response.json()
    if not data:
        break
    products.extend(data)
    print(f"Fetched page {page}, total products so far: {len(products)}")
    page += 1

print(f"\nTotal published products fetched: {len(products)}")
print("Exporting to productos_publicados.csv ...")

with open("productos_publicados.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["ID", "SKU", "Name", "Inventory"])
    for product in tqdm(products, desc="Writing products", unit="product"):
        product_id = product.get("id")
        sku = product.get("sku")
        name = product.get("name")
        inventory = product.get("stock_quantity")
        if sku:  # Only export products with SKU
            writer.writerow([product_id, sku, name, inventory])

print("\n¡Exportación completada! Archivo: productos_publicados.csv")
