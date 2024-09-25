
def userEntity(item) -> dict:
    return {
        "u_id": str(item.id),  
        "fullname": item.fullname,
        "username": item.username,
        "email": item.email,
        "password": item.password
    }


def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]
