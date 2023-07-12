from .models import Post, Team


def get_teams(request):
    return {"teams": Team.objects.all()}
