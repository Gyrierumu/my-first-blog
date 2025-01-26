from django import template
register = template.Library()

@register.filter
def add_class(field, css_class):
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={
            "class": " ".join((field.field.widget.attrs.get("class", ""), css_class))
        })
    else:
        return field

@register.filter
def get_class_name(value):
    return value.__class__.__name__