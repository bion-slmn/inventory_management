from functools import wraps
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

def handle_exceptions(view_func):
    @wraps(view_func)
    def _wrapped_view(*args, **kwargs):
        try:
            return view_func(*args, **kwargs)
        except Http404:
            return Response(
                {'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            return Response(
                {'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
    return _wrapped_view
