from django import template

register = template.Library()


@register.filter
def create_range(counts: int):
    return range(counts)


@register.simple_tag
def set_variable(counts: int):
    return counts


@register.simple_tag
def increase_variable(counts: int):
    return counts + 1
