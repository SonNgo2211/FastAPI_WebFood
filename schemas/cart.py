
def CartItemEntity(item) -> dict:
   return {
        "f_id": str(item["f_id"]),
        "fname": str(item["fname"]),
        "image": str(item["image"]),
        "price": float(item["price"]),
        "quantity": int(item["quantity"]),
    }

def CartItemsEntity(entity) -> list:
    return [CartItemEntity(item) for item in entity]


def CartEntity(item) -> dict:
   return {
        "c_id": str(item["_id"]),
        "u_id": str(item["u_id"]),
        "items": CartItemsEntity(item["items"]),
        "amount": float(item["amount"]),
    }

def CartsEntity(entity) -> list:
    return [CartEntity(item) for item in entity]