from django.db import models

from thistothat.common.models import BaseStaticModel


# TODO: complete this....

class Genus(BaseStaticModel):

    tsn = models.IntegerField()
    name_sci = models.CharField(max_length=255)
    name_eng = models.CharField(max_length=255)

    class Meta:
        ordering = ['name_sci']    

    def __str__(self):
        return f'{self.name_sci}'


class Species(BaseStaticModel):

    genus = models.ForeignKey(Genus, on_delete=models.CASCADE)

    tsn = models.IntegerField()
    name_sci = models.CharField(max_length=255)
    name_eng = models.CharField(max_length=255)

    class Meta:
        ordering = ['name_sci']  

    def __str__(self):
        return f'{self.name_sci}'


class TaxonomicUnit(BaseStaticModel):

    name_sci = models.CharField(max_length=255)
    name_eng = models.CharField(max_length=255)

    rank_name = models.CharField(max_length=50) # Kingdom, Phylum, Genus, Species...
    tsn = models.IntegerField()
