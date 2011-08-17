from templatetag_sugar.register import tag
from templatetag_sugar.parser import Variable, Optional, Constant, Name

@register.filter
def first(iterable):
    return iterable[0]

@register.filter
def last(iterable):
    return iterable[-1]
