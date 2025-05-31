import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

BASE_URL = "http://190.0.50.162:8081/Api"
USERNAME = "Almago"
PASSWORD = "Almago2022"
COD_COMPANIA = "1"
COD_EMPRESA = "1"
TARGET_WAREHOUSES = {"1", "3", "5", "6", "7", "8"}
TOKEN_LIFETIME = 240  # 4 minutes


def get_token():
    """
    Authenticate with the HGI API and return a fresh JWT token.
    Prints the token upon successful retrieval.
    Handles server error messages and allows manual input as a fallback.
    """
    url = f"{BASE_URL}/Autenticar?usuario={USERNAME}&clave={PASSWORD}&cod_compania={COD_COMPANIA}&cod_empresa={COD_EMPRESA}"
    while True:
        resp = requests.get(url)
        print("STATUS:", resp.status_code)
        print("RESPONSE:", resp.text)
        resp.raise_for_status()
        data = resp.json()

        jwt_token = data.get("JwtToken")
        if jwt_token:
            print(f"\n[INFO] New JWT token acquired at {time.strftime('%H:%M:%S')}:")
            print(jwt_token)
            return jwt_token

        # If the server provides an error message (e.g., token still valid)
        if "Error" in data and data["Error"].get("Mensaje"):
            print("SERVER ERROR:", data["Error"]["Mensaje"])
            # Ask the user for a token, or press ENTER to retry automatic fetch
            token = input(
                "Paste your JWT Token (or press ENTER to try again): "
            ).strip()
            if token:
                print(f"[INFO] Token provided manually:\n{token}")
                return token
            else:
                print("[INFO] Retrying automatic token retrieval...")
                time.sleep(2)
                continue  # Try again

        print("[ERROR] Unexpected server response. Retrying...")
        time.sleep(2)


def get_inventory(sku, token, get_new_token_callback):
    headers = {"Authorization": f"Bearer {token}"}
    params = {"codigo_producto": sku, "codigo_bodega": "*", "codigo_lote": "*"}
    url = f"{BASE_URL}/Inventario/ObtenerInventario"
    resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 401:
        print(f"Token inválido para SKU {sku}, solicitando un nuevo token...")
        token = get_new_token_callback()
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers, params=params)
    if resp.status_code == 404:
        print(f"Not found for SKU {sku}")
        return sku, 0
    resp.raise_for_status()
    data = resp.json()
    total = 0
    for item in data:
        bodega = str(item.get("CodigoBodega", item.get("Bodega", "")))
        cantidad = float(item.get("Cantidad", 0))
        if bodega in TARGET_WAREHOUSES:
            total += cantidad
    return sku, total


def main():
    # Read SKUs from CSV
    skus = []
    with open("productos_publicados.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sku = row["SKU"].strip()
            if sku:
                skus.append(sku)

    print(f"Total SKUs publicados encontrados: {len(skus)}")

    results = []
    token = get_token()
    token_time = time.time()

    def get_new_token():
        nonlocal token
        nonlocal token_time
        token = get_token()
        token_time = time.time()
        return token

    def process_sku(sku):
        nonlocal token
        nonlocal token_time
        # Refresh token every 4 minutes
        if time.time() - token_time > TOKEN_LIFETIME:
            token = get_token()
            token_time = time.time()
        try:
            sku_code, total = get_inventory(sku, token, get_new_token)
            return {"SKU": sku_code, "Inventario_total_bodegas_1_3_5_7": total}
        except Exception as e:
            print(f"Error for SKU {sku}: {e}")
            return {"SKU": sku, "Inventario_total_bodegas_1_3_5_7": "ERROR"}

    max_workers = 10  # Tune this as needed
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_sku = {executor.submit(process_sku, sku): sku for sku in skus}
        count = 0
        for future in as_completed(future_to_sku):
            result = future.result()
            results.append(result)
            count += 1
            print(
                f"Processed {count}/{len(skus)}: {result['SKU']} - Inv: {result['Inventario_total_bodegas_1_3_5_7']}"
            )

    # Save results
    with open("sync_result.csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["SKU", "Inventario_total_bodegas_1_3_5_7"]
        )
        writer.writeheader()
        writer.writerows(results)

    analyze_results("sync_result.csv")


def analyze_results(filename="sync_result.csv"):
    count_0 = 0
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4_or_more = 0
    valid_products = 0

    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                inv = float(row["Inventario_total_bodegas_1_3_5_7"])
            except Exception:
                continue  # Ignore errors (e.g. "ERROR" strings)
            valid_products += 1
            if inv == 0:
                count_0 += 1
            elif inv == 1:
                count_1 += 1
            elif inv == 2:
                count_2 += 1
            elif inv == 3:
                count_3 += 1
            elif inv >= 4:
                count_4_or_more += 1

    def percent(x):
        return f"{(x / valid_products * 100):.1f}%" if valid_products else "0%"

    print(f"Total productos analizados (válidos): {valid_products}\n")
    print(f"Productos con inventario 0: {count_0} ({percent(count_0)})")
    print(f"Productos con inventario 1: {count_1} ({percent(count_1)})")
    print(f"Productos con inventario 2: {count_2} ({percent(count_2)})")
    print(f"Productos con inventario 3: {count_3} ({percent(count_3)})")
    print(
        f"Productos con inventario 4 o más: {count_4_or_more} ({percent(count_4_or_more)})"
    )


if __name__ == "__main__":
    main()
