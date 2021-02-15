import os
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.translation import gettext
from faker import Faker
from notes import models as notes_models

BLOG_DIR = settings.BASE_DIR / "data" / "blogs"


class Command(BaseCommand):

    help = gettext(
        "Load the files from the blog directory and add them to the database "
        "as valid note objects."
    )

    def handle(self, *args, **options):
        CustomUser = get_user_model()
        super_user = CustomUser.objects.get(is_superuser=True)
        fake = Faker()

        notes = []
        for blog in os.listdir(BLOG_DIR):
            blog_file = BLOG_DIR / blog
            with open(blog_file) as file:
                note = notes_models.Note.objects.create(
                    title=fake.sentence(),
                    writer=super_user,
                    description=fake.paragraph(2),
                    body=file.read(),
                )
                notes.append(note)
        self.stdout.write(
            self.style.SUCCESS("\nAdded the sample blogs to the database!")
        )

        random_note = random.choice(notes)
        for user in CustomUser.objects.all():
            notes_models.Bookmark.objects.create(note=random_note, user=user)
        self.stdout.write(
            self.style.SUCCESS(f"\n'{random_note.slug}' was the bookmark target!")
        )
