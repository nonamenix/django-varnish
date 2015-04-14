from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from progressbar import ProgressBar
from blog.models import Post
from yandex_vesna_generator.vesna import VesnaGenerator


class Command(BaseCommand):
    def handle(self, *args, **options):
        vesna = VesnaGenerator()
        n = 100
        pbar = ProgressBar(maxval=n).start()
        for i in range(n):
            entry = vesna.generate_entry()
            Post(
                title=entry.title,
                content=entry.body,
                slug=entry.slug,
                datetime=datetime.now()
            ).save()
            pbar.update(i+1)
        pbar.finish()

