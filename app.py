from flask import Flask, request, jsonify
import database
import external_api

app = Flask(__name__)

@app.route('/inventory', methods=['GET'])
def get_inventory():
    items = database.get_all()
    return jsonify({"inventory": items}), 200

@app.route('/inventory/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = database.get_by_id(item_id)
    if item:
        return jsonify({"item": item}), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/inventory', methods=['POST'])
def add_inventory_item():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    if not data.get("product_name"):
        return jsonify({"error": "product_name is required"}), 400
    if "price" not in data or not isinstance(data["price"], (int, float)):
        return jsonify({"error": "price is required and must be a number"}), 400
    if "quantity" not in data or not isinstance(data["quantity"], int):
        return jsonify({"error": "quantity is required and must be an integer"}), 400
    item = database.add_item(data)
    return jsonify({"item": item}), 201

@app.route('/inventory/<int:item_id>', methods=['PATCH'])
def update_inventory_item(item_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    if "product_name" in data and not data["product_name"]:
        return jsonify({"error": "product_name cannot be empty"}), 400
    if "price" in data and not isinstance(data["price"], (int, float)):
        return jsonify({"error": "price must be a number"}), 400
    if "quantity" in data and not isinstance(data["quantity"], int):
        return jsonify({"error": "quantity must be an integer"}), 400
    item = database.update_item(item_id, data)
    if item:
        return jsonify({"item": item}), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/inventory/<int:item_id>', methods=['DELETE'])
def delete_inventory_item(item_id):
    success = database.delete_item(item_id)
    if success:
        return jsonify({"message": "Item deleted"}), 200
    return jsonify({"error": "Item not found"}), 404

@app.route('/inventory/fetch/<string:barcode>', methods=['GET'])
def fetch_item_by_barcode(barcode):
    product = external_api.fetch_by_barcode(barcode)
    if product:
        return jsonify({"product": product}), 200
    return jsonify({"error": "Product not found"}), 404

@app.route('/inventory/search', methods=['GET'])
def search_inventory():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    items = database.search_inventory(query)
    return jsonify({"results": items}), 200

if __name__ == '__main__':
    app.run(debug=True)