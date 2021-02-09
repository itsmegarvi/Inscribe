import random

from accounts import models as accounts_models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.translation import gettext
from faker import Faker
from mdgen import MarkdownPostProvider
from notes import models as notes_models


class Command(BaseCommand):

    help = gettext(
        "Create instances of accounts.CustomUser, notes.Note. "
        "By default 100 instances of each are created. Can be changed by passing "
        "the -i argument to the command."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "-i",
            "--instances",
            default=100,
            dest="instances",
            help=gettext("The number of data instances to be created."),
        )

    def handle(self, *args, **options):
        if settings.DEBUG is not True:
            self.stdout.write(
                self.style.ERROR(
                    "This command can not be used in a production environment"
                )
            )
            exit(1)

        instances = int(options["instances"])

        fake = Faker()
        fake.add_provider(MarkdownPostProvider)
        CustomUser = get_user_model()

        users = []
        for __ in range(1, instances + 1):
            user = CustomUser.objects.create_user(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password=fake.password(),
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f"\nCreated {instances} custom users"))

        notes = [  # noqa
            notes_models.Note.objects.create(
                title=fake.sentence(),
                writer=random.choice(users),
                updated_at=fake.future_date(),
                body=fake.post(size="large"),
                draft=fake.boolean(chance_of_getting_true=75),
                hidden=fake.boolean(chance_of_getting_true=25),
                description=fake.sentence(),
            )
            for _ in range(instances)
        ]
        self.stdout.write(self.style.SUCCESS(f"\nCreated {instances} notes"))

        super_user = CustomUser.objects.get(is_superuser=True)
        user_notes = [  # noqa
            notes_models.Note.objects.create(
                title=fake.sentence(),
                writer=super_user,
                updated_at=fake.future_date(),
                body=fake.post(size="large"),
                draft=fake.boolean(chance_of_getting_true=75),
                hidden=fake.boolean(chance_of_getting_true=25),
                description=fake.sentence(),
            )
            for _ in range(instances)
        ]
        self.stdout.write(
            self.style.SUCCESS(f"\nCreated {instances} notes for superuser")
        )

        user_comments = []
        for _ in range(instances):
            note = random.choice(user_notes)
            parent = None
            if user_comments:
                comments = notes_models.Comment.objects.filter(note=note)
                if comments:
                    parent = sorted(comments, key=lambda x: random.random())[0]
            user_comment = notes_models.Comment.objects.create(
                note=note,
                user=random.choice(users),
                content=fake.paragraph(),
                active=fake.boolean(chance_of_getting_true=75),
                parent=parent,
            )
            user_comments.append(user_comment)
        self.stdout.write(
            self.style.SUCCESS(
                f"\nCreated {instances} of parented comments for superuser's notes"
            )
        )

        user_comments_no_parent = [  # noqa
            notes_models.Comment.objects.create(
                note=random.choice(user_notes),
                user=random.choice(users),
                content=fake.paragraph(),
                active=fake.boolean(chance_of_getting_true=75),
                parent=parent,
            )
            for _ in range(instances * 10)
        ]
        self.stdout.write(
            self.style.SUCCESS(
                f"\nCreated {instances * 10} comments for superuser's notes"
            )
        )

        common_comments = [  # noqa
            notes_models.Comment.objects.create(
                note=note,
                user=random.choice(users),
                content=fake.paragraph(),
                active=fake.boolean(chance_of_getting_true=75),
                parent=None,
            )
            for note in notes
        ]
        self.stdout.write(
            self.style.SUCCESS(
                f"\nCreated {len(common_comments)} comments for common notes"
            )
        )

        user_bookmarks = []
        for user_note in user_notes:
            bookmarks = [
                notes_models.Bookmark.objects.create(
                    note=user_note, user=random.choice(users)
                )
                for _ in range(random.randint(1, 100))
            ]
            user_bookmarks.extend(bookmarks)

        self.stdout.write(
            self.style.SUCCESS(
                f"\nCreated {len(user_bookmarks)} bookmarks for superuser"
            )
        )

        common_bookmarks = []
        for note in notes:
            bookmarks = [
                notes_models.Bookmark.objects.create(
                    note=note, user=random.choice(users)
                )
                for _ in range(random.randint(1, 100))
            ]
            common_bookmarks.extend(bookmarks)

        self.stdout.write(
            self.style.SUCCESS(
                f"\nCreated {len(common_bookmarks)} bookmarks for common users"
            )
        )

        user_followers = [  # noqa
            accounts_models.CustomUserFollowing.objects.create(
                user=super_user, follower=follower
            )
            for follower in users
        ]
        self.stdout.write(
            self.style.SUCCESS(f"\nCreated {instances} followers for superuser")
        )

        user_followed = [  # noqa
            accounts_models.CustomUserFollowing.objects.create(
                follower=super_user, user=user
            )
            for user in users
        ]
        self.stdout.write(self.style.SUCCESS(f"\nSuperuser followed {len(users)} users"))
