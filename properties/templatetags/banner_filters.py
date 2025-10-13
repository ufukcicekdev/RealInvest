from django import template

register = template.Library()

@register.filter
def get_position_style(position):
    """
    Convert position choice to CSS style
    """
    positions = {
        'left': 'left: 2rem; top: 50%; transform: translateY(-50%);',
        'center': 'left: 50%; top: 60%; transform: translate(-50%, -50%);',
        'right': 'right: 2rem; top: 50%; transform: translateY(-50%);',
    }
    return positions.get(position, positions['center'])

@register.filter
def get_alt_text_position_style(position):
    """
    Convert position choice to CSS style for alternative text
    """
    positions = {
        'left': 'left: 2rem; top: 60%; transform: translateY(-50%);',
        'center': 'left: 50%; top: 40%; transform: translate(-50%, -50%);',
        'right': 'right: 2rem; top: 60%; transform: translateY(-50%);',
    }
    return positions.get(position, positions['center'])