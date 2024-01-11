from fastapi import status
import math


def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    result = {
        "meta": {
            "statusCode": status_code,
            "message": message,
        },
        "result": data,
    }
    return result


def error_response(
    message="An error occurred", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
):
    result = {
        "meta": {
            "statusCode": status_code,
            "message": message,
        }
    }
    return result


def paginate_response(list, start, end, page, limit, resource_name, **kwargs):
    """Paginate response and add pagination links"""
    if len(list[start:end]) > 0:
        total_pages = math.ceil(len(list) / (end - start) if (end - start) > 0 else 1)
    else:
        total_pages = (
            0  # or any other value you want to assign when the sublist is empty
        )

    response = {
        "data": list[start:end],
        "total": len(list),
        "count": len(list[start:end]),
        "totalPages": total_pages,
        "currentPage": page,
        "pagination": {},
    }

    if end >= len(list):
        response["pagination"]["next"] = None
        if page > 1:
            response["pagination"]["previous"] = build_pagination_link(
                resource_name, page - 1, limit, **kwargs
            )
        else:
            response["pagination"]["previous"] = None
    else:
        if page > 1:
            response["pagination"]["previous"] = build_pagination_link(
                resource_name, page - 1, limit, **kwargs
            )
        else:
            response["pagination"]["previous"] = None
        response["pagination"]["next"] = build_pagination_link(
            resource_name, page + 1, limit, **kwargs
        )

    return response


def build_pagination_link(resource_name, page, limit, **kwargs):
    """Build pagination link with optional parameters"""
    result = {"link": f"/{resource_name}?page={page}&limit={limit}", "page": page}

    for key, value in kwargs.items():
        if value is not None:
            result["link"] += f"&{key}={value}"

    return result
