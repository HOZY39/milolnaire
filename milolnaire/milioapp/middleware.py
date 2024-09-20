from django.shortcuts import redirect

class NoBackMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.session.get('redirected', False):
            if request.path != '/start_game/':
                return redirect('start_game')
        return response
