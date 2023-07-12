import xml.etree.cElementTree as et

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


def validate_svg(f):
    # Find "start" word in file and get "tag" from there
    f.seek(0)
    tag = None
    try:
        for _, el in et.iterparse(f, ("start",)):
            tag = el.tag
            break
    except et.ParseError:
        pass

    # Check that this "tag" is correct
    if tag != "{http://www.w3.org/2000/svg}svg":
        raise ValidationError("Uploaded file is not an image or SVG file.")

    # Do not forget to "reset" file
    f.seek(0)

    return f


class Team(models.Model):
    sponsor = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

    logo_svg = models.FileField(
        upload_to="team/logo", validators=[validate_svg]
    )

    @property
    def full_name(self):
        return f"{self.sponsor} {self.name}"

    @property
    def slug(self):
        return f"{self.sponsor}-{self.name}"

    def get_absolute_url(self):
        return f"{reverse('post:post_list')}?category={self.slug}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)

    title = models.CharField(max_length=100)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["created"])]
