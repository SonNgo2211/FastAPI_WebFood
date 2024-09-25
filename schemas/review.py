
def reviewEntity(item) -> dict:
    return {
        "r_id": str(item["_id"]),
        "f_id": str(item["f_id"]),
        "user": dict(item["user"]),
        "content": item["content"],
        "time": item["time"],
    }

def reviewsEntity(entity) -> list:
    return [reviewEntity(item) for item in entity]