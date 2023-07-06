from django import template

from ..models import Team

register = template.Library()


@register.simple_tag
def get_teams():
    return Team.objects.all()
