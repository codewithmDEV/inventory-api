import requests

BASE_URL = "http://127.0.0.1:5000"

def list_items():
    response = requests.get(f"{BASE_URL}/inventory")
    if response.status_code == 200:
        return response.json()
    return None

def view_item(item_id):
    response = requests.get(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 200:
        return response.json()
    return None

def add_item(item_data):
    response = requests.post(f"{BASE_URL}/inventory", json=item_data)
    if response.status_code == 201:
        return response.json()
    return None

def update_item(item_id, item_data):
    response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=item_data)
    if response.status_code == 200:
        return response.json()
    return None

def delete_item(item_id):
    response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    if response.status_code == 200:
        return True
    return False

def search_items(query):
    response = requests.get(f"{BASE_URL}/inventory/search", params={"query": query})
    if response.status_code == 200:
        return response.json()
    return None

def find_and_add(barcode):
    response = requests.get(f"{BASE_URL}/inventory/fetch/{barcode}")
    if response.status_code == 200:
        product_data = response.json().get("product")
        if product_data:
            print(f"\nFound: {product_data.get('product_name', 'Unknown')}")
            print(f"Brand: {product_data.get('brands', 'Unknown')}")
            confirm = input("Add to inventory? [y/n]: ").strip().lower()
            if confirm == "y":
                price = float(input("Price: "))
                quantity = int(input("Quantity: "))
                item_data = {
                    "product_name": product_data.get("product_name", "Unknown"),
                    "price": price,
                    "quantity": quantity,
                    "brand": product_data.get("brands", "Unknown"),
                    "description": product_data.get("generic_name", "")
                }
                return add_item(item_data)
            else:
                print("Cancelled.")
                return None
    return None

def main():
    print("Inventory CLI — type 'help' for commands")
    while True:
        raw = input("> ").strip()
        if not raw:
            continue
        parts = raw.split()
        action = parts[0].lower()

        if action == "list":
            result = list_items()
            print(result)

        elif action == "view" and len(parts) == 2:
            result = view_item(int(parts[1]))
            print(result)

        elif action == "add":
            name = input("Product name: ")
            price = float(input("Price: "))
            quantity = int(input("Quantity: "))
            brand = input("Brand: ")
            description = input("Description: ")
            result = add_item({
                "product_name": name,
                "price": price,
                "quantity": quantity,
                "brand": brand,
                "description": description
            })
            print(result)

        elif action == "update" and len(parts) == 2:
            field = input("Field to update (product_name/price/quantity): ")
            value = input("New value: ")
            data = {field: float(value) if field == "price" else (int(value) if field == "quantity" else value)}
            result = update_item(int(parts[1]), data)
            print(result)

        elif action == "delete" and len(parts) == 2:
            result = delete_item(int(parts[1]))
            print("Deleted" if result else "Not found")

        elif action == "search" and len(parts) >= 2:
            query = " ".join(parts[1:])
            result = search_items(query)
            print(result)

        elif action == "find" and len(parts) == 2:
            result = find_and_add(parts[1])
            if result:
                print(result)

        elif action == "exit":
            print("Bye.")
            break

        elif action == "help":
            print("Commands: list, view <id>, add, update <id>, delete <id>, search <name>, find <barcode>, exit")

        else:
            print("Unknown command. Type 'help'.")

if __name__ == "__main__":
    main()