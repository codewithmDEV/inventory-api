import requests

def fetch_by_barcode(barcode):
    try:
        url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}.json"
        headers = {"User-Agent": "InventoryAPI/1.0 (mohammedduale1738@gmail.com)"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 1:
                return data["product"]
    except requests.RequestException:
        pass
    return None