from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

class AuthRequiredMiddleware:
    """
    Middleware to enforce user authentication on specified paths.

    This middleware checks if a user is authenticated before accessing any pages that
    are not explicitly marked as authentication exempt. If a user is not authenticated,
    they are redirected to the login page with a message prompting them to log in.

    Attributes:
        get_response: A callable that takes a request and returns a response. This is
                      part of the middleware structure in Django, allowing for response
                      processing or passing the request to the next middleware or view.

    Methods:
        __call__(self, request):
            Processes each request, checks user authentication, and redirects
            unauthenticated users to the login page for protected routes.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware with the Django-provided get_response callable.

        Parameters:
            get_response: A callable that takes a request and returns a response.
                          This is provided by Django's middleware mechanism.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process each request through the middleware.

        Checks if the user is authenticated and if the request path is not in the
        list of authentication-exempt URLs. If the user is unauthenticated and the
        path requires authentication, redirect them to the login page with a message.

        Parameters:
            request: HttpRequest object representing the current request.

        Returns:
            HttpResponse: The response object returned by the next middleware or view
                          if the request passes through, or a redirect response if
                          the user is unauthenticated on a protected path.
        """
        # Ensure the request path ends with a slash for consistent matching
        request_path = request.path if request.path.endswith('/') else f"{request.path}/"

        # Check if the user is authenticated or if the path is exempt from authentication
        if not request.user.is_authenticated and request_path not in settings.AUTH_EXEMPT_URLS:
            messages.add_message(request, messages.INFO, 'You must be logged in to view this page.')
            return redirect(f'{settings.LOGIN_URL}?next={request.path}')

        # Call the next middleware or view if authentication is not required or if the user is authenticated
        response = self.get_response(request)
        return response
