from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from resident_management.core.utils.response import success

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000
    
    
    def get_paginated_response(self, data):
        page = self.page.number
        per_page = self.get_page_size(self.request) or self.page.paginator.per_page
        total = self.page.paginator.count
        total_pages = self.page.paginator.num_pages

        payload = success(
            data={
                "results": data,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "total_pages": total_pages,
                },
            },
            message="OK",
            code=0,
        )

        return Response(
            payload,
            status=200
        )


