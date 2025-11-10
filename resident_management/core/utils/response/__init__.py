def success(data=None, message: str = "OK", code: int = 0):
    return {
        "success": True,
        "message": message,
        "code": code,
        "data": data,
    }


def error(message: str = "Error", code: int = 400, errors=None):
    return {
        "success": False,
        "message": message,
        "code": code,
        "errors": errors,
    }


def paginated(data, page: int, per_page: int, total: int, message: str = "OK", code: int = 0):
    total_pages = ((total + per_page - 1) // per_page) if per_page else 0
    return {
        "success": True,
        "message": message,
        "code": code,
        "data": data,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        },
    }

