# -*- coding: utf-8 -*-
from django.template import Library, TemplateSyntaxError

register = Library()


@register.filter(is_safe=False)
def get_attr(object, attr):
    return getattr(object, attr)
