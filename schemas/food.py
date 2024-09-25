
def foodEntity(item) -> dict:
    return {
        "p_id": str(item["_id"]),
        "fname": item["fname"],
        "image": item["image"],
        "category": item["category"],
        "price": float(item["price"])
    }

def foodsEntity(entity) -> list:
    return [foodEntity(item) for item in entity]