
from rest_framework import serializers


from commodities.models import HsChapter, HsHeading, HsSubheading



class GetHsChapterSerializer(serializers.ModelSerializer):

    level = serializers.SerializerMethodField()
    def get_level(self, chapter):
        return 'chapter'

    class Meta:
        model = HsChapter
        fields = ['code', 'description', 'level']


class GetHsHeadingSerializer(serializers.ModelSerializer):

    level = serializers.SerializerMethodField()
    def get_level(self, chapter):
        return 'heading'

    class Meta:
        model = HsHeading
        fields = ['code', 'description', 'level']


class GetHsSubheadingSerializer(serializers.ModelSerializer):

    level = serializers.SerializerMethodField()
    def get_level(self, chapter):
        return 'subheading'

    class Meta:
        model = HsSubheading
        fields = ['code', 'description', 'level']