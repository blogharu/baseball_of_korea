from .forms import PostSearchForm
from .models import Post, Team


def get_teams(request):
    teams = Team.objects.all()
    if category := request.GET.get("category"):
        try:
            sponsor, name = category.split("-")
            category = teams.get(sponsor=sponsor, name=name)
        except:
            category = None

    return {
        "teams": teams,
        "category": category,
        "post_search_form": PostSearchForm(request.GET),
    }
