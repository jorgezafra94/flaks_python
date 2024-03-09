import uuid
from flask import Flask, request
from db import stores, items
from flask_smorest import abort

app = Flask(__name__)


@app.get("/stores")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/stores")
def add_store():
    store_data = request.get_json()
    if "name" not in store_data.keys():
        raise ValueError("Store don't have a name")
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.get("/stores/<store_id>")
def get_store(store_id):
    store = stores.get(store_id, None)
    if not store:
        abort(404, message="Store not found")
    return store


@app.get("/items")
def get_items():
    return {"items": list(items.values())}


@app.post("/items")
def add_item():
    item_data = request.get_json()
    if item_data.get("store_id") not in stores:
        abort(404, message="Store not found")
    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id": item_id}
    items[item_id] = new_item
    return new_item, 201


@app.get("/items/<item_id>")
def get_item(item_id):
    item = items.get(item_id, None)
    if not item:
        abort(404, message="Item not found")
    return item


if __name__ == "__main__":
    app.run()
