from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, req):
        if req.user.is_authenticated and req.session.get_expiry_age() <= 600:
            return redirect(reverse('/'))

        response = self.get_response(req)

        return response
