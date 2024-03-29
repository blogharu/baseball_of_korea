# Generated by Django 4.2.3 on 2023-07-06 02:17

from django.db import migrations, models
import post.models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_remove_like_post_remove_like_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='logo_svg',
            field=models.FileField(upload_to='team/logo', validators=[post.models.validate_svg]),
        ),
    ]
