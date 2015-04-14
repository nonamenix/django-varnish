from urlparse import urljoin

__author__ = 'nonamenix'

import httplib
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def ban(url_pattern):
    """
    Make ban request to url_pattern on varnish server.

    :param url_pattern: pattern of url for ban
    :return: status code of response
    """
    conn = httplib.HTTPConnection(settings.SITE_URL)
    url = urljoin(settings.SITE_URL, url_pattern)
    conn.request('BAN', url)
    resp = conn.getresponse()
    information_string = 'BAN request for: %(url)s, taken response: %(status)s with body \n%(body)s'
    if resp.status == httplib.OK:
        logger.info(information_string % {
            'url': url,
            'body': resp.read(),
            'status': resp.status
        })
    else:
        logger.error(information_string % {
            'url': url,
            'body': resp.read(),
            'status': resp.status
        })
    conn.close()
    return resp.status