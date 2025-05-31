import csv

# Lee los SKUs y su inventario desde productos_publicados.csv (WEB)
web_inventory = {}
with open("productos_publicados.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        sku = row["SKU"].strip()
        try:
            inv = float(row["Inventory"])
        except Exception:
            inv = None
        web_inventory[sku] = inv

# Lee los SKUs y su inventario desde sync_result.csv (ERP)
erp_inventory = {}
with open("sync_result.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        sku = row["SKU"].strip()
        try:
            inv = float(row["Inventario_total_bodegas_1_3_5_7"])
        except Exception:
            inv = None
        erp_inventory[sku] = inv

# Compara ambos archivos
mismatch_count = 0

print("\n--- Diferencias encontradas por SKU ---\n")

# SKUs en web pero no en ERP
for sku in web_inventory:
    if sku not in erp_inventory:
        print(f"SKU {sku} está en WEB pero NO en ERP")
        mismatch_count += 1

# SKUs en ERP pero no en web
for sku in erp_inventory:
    if sku not in web_inventory:
        print(f"SKU {sku} está en ERP pero NO en WEB")
        mismatch_count += 1

# SKUs en ambos pero inventario diferente (exceptuando None/0)
for sku in web_inventory:
    if sku in erp_inventory:
        inv_web = web_inventory[sku]
        inv_erp = erp_inventory[sku]
        # Equivalentes si uno es None y otro es 0
        if (inv_web is None and inv_erp == 0) or (inv_erp is None and inv_web == 0):
            continue
        if inv_web != inv_erp:
            print(f"SKU {sku}: WEB={inv_web} | ERP={inv_erp}")
            mismatch_count += 1

print(f"\nTotal de diferencias encontradas: {mismatch_count}\n")
