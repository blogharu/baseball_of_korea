from django import template

register = template.Library()


@register.filter
def get_query_parameters(request, page=None):
    query_parameters = []
    if request and request.GET:
        if page:
            request.GET["page"] = page
        for key, val in request.GET.items():
            query_parameters.append(f"{key}={val}")
    return "&".join(query_parameters)
