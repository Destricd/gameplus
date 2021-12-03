from django import template
from ..models import Employee

register = template.Library()

@register.simple_tag
def get_companion(request, chat):
    for u in chat.members.all():
        if u != request.session["id_user"]:
            return u
    return None