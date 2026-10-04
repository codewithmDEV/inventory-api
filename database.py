inventory = [
    {
        "id": 1,
        "product_name": "Almond Milk",
        "price": 3.99,
        "quantity": 50,
        "brand": "Almond Breeze",
        "description": "A dairy-free milk alternative made from almonds."
    },
    {
        "id": 2,
        "product_name": "Organic Eggs",
        "price": 4.99,
        "quantity": 30,
        "brand": "Happy Hen Farms",
        "description": "Free-range organic eggs from happy hens."
    },
    {
        "id": 3,
        "product_name": "Quinoa",
        "price": 5.49,
        "quantity": 20,
        "brand": "Ancient Harvest",
        "description": "A nutritious grain high in protein and fiber."
    },
    {
        "id": 4,
        "product_name": "Greek Yogurt",
        "price": 1.99,
        "quantity": 40,
        "brand": "Chobani",
        "description": "Thick and creamy Greek yogurt, rich in protein."
    },
    {
        "id": 5,
        "product_name": "Almond Butter",
        "price": 7.99,
        "quantity": 25,
        "brand": "Justin's",
        "description": "Smooth almond butter made from roasted almonds."
    }
]

def get_all():
    return inventory

def get_by_id(item_id):
    for item in inventory:
        if item["id"]==item_id:
            return item
    return None

def add_item(item):
    new_id = max(item["id"] for item in inventory) + 1 if inventory else 1
    item["id"] = new_id
    inventory.append(item)
    return item

def update_item(item_id, data):
    for item in inventory:
        if item["id"] == item_id:
            item.update(data)
            return item
    return None

def delete_item(item_id):
    for i, item in enumerate(inventory):
        if item["id"] == item_id:
            del inventory[i]
            return True
    return False

def search_inventory(query):
    return [item for item in inventory if query.lower() in item["product_name"].lower()]