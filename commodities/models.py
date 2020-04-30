from django.db import models

from thistothat.common.models import BaseStaticModel


# Harmonized System (H5)

class HsChapter(BaseStaticModel):
    
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    

class HsHeading(BaseStaticModel):
    
    chapter = models.ForeignKey(HsChapter, on_delete=models.CASCADE, related_name='headings')

    code = models.CharField(max_length=10)
    description = models.CharField(max_length=255)


class HsSubheading(BaseStaticModel):

    chapter = models.ForeignKey(HsChapter, on_delete=models.CASCADE, related_name='subheadings')
    heading = models.ForeignKey(HsHeading, on_delete=models.CASCADE, related_name='subheadings')
    
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    