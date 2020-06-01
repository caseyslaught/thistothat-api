
import csv
from django.conf import settings
from django.core.management.base import BaseCommand
import json
import os

from species.models import Genus, Species


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):

        # TODO: how to connect to another database (ITIS)?

        print('chapters:', Genus.objects.all().count())
        print('headings:', Species.objects.all().count())
