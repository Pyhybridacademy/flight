from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def split(value, delimiter):
    """Split a string by delimiter"""
    if value:
        return value.split(delimiter)
    return []

@register.filter
def currency(value):
    """Format value as USD currency"""
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return f"${0.00}"

@register.filter
def currency_simple(value):
    """Format value as simple USD currency without decimals for whole numbers"""
    try:
        val = float(value)
        if val == int(val):
            return f"${int(val):,}"
        else:
            return f"${val:,.2f}"
    except (ValueError, TypeError):
        return f"$0"

@register.simple_tag
def year_range(start_year, end_year):
    """Generate a range of years"""
    return range(start_year, end_year + 1)

@register.filter
def get_fare_by_class(flight, seat_class):
    """Get fare by seat class"""
    if seat_class.lower() == 'economy':
        return flight.economy_fare
    elif seat_class.lower() == 'business':
        return flight.business_fare
    elif seat_class.lower() == 'first':
        return flight.first_fare
    return 0

@register.filter
def multiply(value, multiplier):
    """Multiply two values"""
    try:
        return float(value) * float(multiplier)
    except (ValueError, TypeError):
        return 0