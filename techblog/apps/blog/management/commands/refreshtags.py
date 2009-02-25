from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = "Refreshes tags if they get out of sync"

    def handle_noargs(self, **options):
        from techblog.apps.blog.models import Tag, Post
        Tag.objects.all().delete()
        for p in Post.objects.all():
            p.save()
