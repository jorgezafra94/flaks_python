from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My store",
        "items": [
            {
                "name": "chair",
                "price": 15.99
            }
        ]
    }
]


@app.get("/stores")
def get_stores():
    return {"stores": stores}


@app.post("/stores")
def add_store():
    data = request.get_json()
    if "name" not in data.keys():
        raise ValueError("Store don't have a name")
    new_store = {"name": data.get("name"), "items": data.get("items", [])}
    stores.append(new_store)
    return new_store, 201


@app.get("/stores/<store_name>")
def get_store(store_name):

    for store in stores:
        if store.get("name") == store_name:
            return store
    return "{message: Store not found}", 404


@app.get("/stores/<store_name>/items")
def get_store_items(store_name):
    for store in stores:
        if store.get("name") == store_name:
            return store.get("items")
    return "{message: Store not found}", 404


@app.post("/stores/<store_name>/items")
def add_item_to_store(store_name):
    for store in stores:
        if store_name == store.get("name"):
            data = request.get_json()
            new_item = {"name": data.get("name"), "price": float(data.get("price"))}
            store["items"].append(new_item)
            return new_item, 201
    return "{message: store not found}", 404


if __name__ == "__main__":
    app.run()
