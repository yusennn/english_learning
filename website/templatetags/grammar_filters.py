from django import template

register = template.Library()

@register.filter(name='replace_gaps')
def replace_gaps(value):
    return value.replace("___", '<span class="gap">[drop here]</span>')
