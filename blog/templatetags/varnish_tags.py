
from __future__ import absolute_import, division, print_function, unicode_literals

from django import template
from django.http import QueryDict


register = template.Library()


@register.filter_function
def varnish(template_names, request, default="varnish_base.html"):
    """
    Returns template name for request.
    :param request: Django request or boolean value
    :param template_names: Base theme name or comma-separated names of base and
      varnish templates.
    Examples::
        {% extends "base.html"|varnish:request %}
        {% extends "base.html,varnish_base.html"|varnish:request %}
        context = {"is_varnish": True}
        {% extends "base.html"|varnish:is_varnish %}
    """
    if isinstance(request, (bool, int)):
        is_varnish = request
    else:
        is_varnish = request.META.get("HTTP_X_VARNISH", False)

    if "," in template_names:
        template_name, varnish_template_name = template_names.split(",", 1)
    else:
        template_name, varnish_template_name = template_names, default

    if is_varnish:
        return varnish_template_name.strip() or default
    return template_name.strip()