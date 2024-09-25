def userEntity(item) -> dict:
    return {
        "u_id": str(item.id),  # Dùng `id` từ MySQL thay vì `ObjectId` từ MongoDB
        "fullname": item.fullname,
        "username": item.username,
        "email": item.email,
        "password": item.password
    }


def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i == '_id'}, **{i:a[i] for i in a if i != '_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]