from django.contrib import admin


from commodities.models import HsChapter, HsHeading, HsSubheading


@admin.register(HsChapter)
class HsChapterAdmin(admin.ModelAdmin):
    list_display = ['code', 'description', 'datetime_created']
    search_fields = ['code', 'description']
    list_filter = []
    ordering = ['code']

    readonly_fields = ['datetime_created', 'datetime_updated', 'uid']
    exclude = ['datetime_deleted']


@admin.register(HsHeading)
class HsHeadingAdmin(admin.ModelAdmin):
    list_display = ['code', 'description', 'chapter', 'datetime_created']
    search_fields = ['code', 'description']
    list_filter = []
    ordering = ['code']

    readonly_fields = ['datetime_created', 'datetime_updated', 'uid']
    exclude = ['datetime_deleted']


@admin.register(HsSubheading)
class HsSubheadingAdmin(admin.ModelAdmin):
    list_display = ['code', 'description', 'chapter', 'heading', 'datetime_created']
    search_fields = ['code', 'description']
    list_filter = []
    ordering = ['code']

    readonly_fields = ['datetime_created', 'datetime_updated', 'uid']
    exclude = ['datetime_deleted']