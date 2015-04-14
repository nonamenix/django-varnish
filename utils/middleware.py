__author__ = 'nonamenix'


class VarnishMiddleware(object):
    def process_request(self, request):
        cookies = ["IS_AUTH", "LANG", "SESSIONID", "CSRFTOKEN"]
        for cookie_name in cookies:
            http_header = "HTTP_X_%s" % cookie_name
            try:
                request.COOKIES[cookie_name.lower()] = request.META[http_header]
            except KeyError:
                pass
