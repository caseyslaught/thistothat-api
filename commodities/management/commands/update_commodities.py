
import csv
from django.conf import settings
from django.core.management.base import BaseCommand
import json
import os

from commodities.models import HsChapter, HsHeading, HsSubheading


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **options):

        codes_path = os.path.join('commodities', 'management', 'commands', 'commodities.csv')

        chapter_objs, headings, subheadings = dict(), dict(), dict()

        with open(codes_path, newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
            for row in reader:
                classification, code, description = row[0].strip(), row[1].strip(), row[2].strip()

                if classification == 'H5':
                    if len(code) == 2:
                        try:
                            chapter = HsChapter.objects.get(code=code)
                            chapter.description = description
                            chapter.save()
                        except HsChapter.DoesNotExist:
                            chapter = HsChapter.objects.create(code=code, description=description)
                        chapter_objs[code] = chapter
                        
                    elif len(code) == 4:
                        headings[code] = description                        
                    elif len(code) == 6:
                        subheadings[code] = description
                    else:
                        print(f'invalid code: {code}')
                        continue

        # the chapters are created, now create the headings
        heading_objs = dict()
        for code, description in headings.items():
            chapter = chapter_objs.get(code[:2])
            if chapter:
                try:
                    heading = HsHeading.objects.get(code=code) # heading is unique
                    heading.description = description
                    heading.save()
                except HsHeading.DoesNotExist:
                    heading = HsHeading.objects.create(chapter=chapter, code=code, description=description)
                heading_objs[code] = heading
            else:
                print(f'chapter not found: {code}, {description}')
                continue

        for code, description in subheadings.items():
            chapter = chapter_objs.get(code[:2])
            heading = heading_objs.get(code[:4])

            if chapter and heading:
                try:
                    subheading = HsSubheading.objects.get(code=code)
                    subheading.description = description
                    subheading.save()
                except HsSubheading.DoesNotExist:
                    subheading = HsSubheading.objects.create(
                        chapter=chapter, 
                        code=code, 
                        description=description, 
                        heading=heading
                    )
            else:
                print(f'chapter or  heading not found: {code}, {description}')
                continue

        print('chapters:', HsChapter.objects.all().count())
        print('headings:', HsHeading.objects.all().count())
        print('subheadings:', HsSubheading.objects.all().count())
