from django.conf import settings

from translaterservice.models import Device


class StackOverflowMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):
        if settings.DEBUG:
            intitle = u'{}: {}'.format(exception.__class__.__name__, exception.message)
            print(intitle)

            url = 'https://api.stackexchange.com/2.2/search'
            headers = {'User-Agent': 'github.com/vitorfs/seot'}
            params = {
                'order': 'desc',
                'sort': 'votes',
                'site': 'stackoverflow',
                'pagesize': 3,
                'tagged': 'python;django',
                'intitle': intitle
            }

            r = request.get(url, params=params, headers=headers)
            questions = r.json()

            print('')

            for question in questions['items']:
                print(question['title'])
                print(question['link'])
                print('')

        return None


class DeviceMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        headers = request.headers
        device_id = headers.get('Device-Id')
        device_type = headers.get('Device-Type')
        if device_id and device_type:
            obj, created = Device.objects.filter(device_id=device_id).get_or_create(device_id=device_id,
                                                                                    device_type=device_type)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
