from django.contrib import admin
from .models import Ticket, Comment, File


class FileInline(admin.StackedInline):
    model = File
    can_delete = True
    verbose_name = 'Files'
    verbose_name_plural = verbose_name
    fk_name = 'ticket'
    extra = 0
    readonly_fields = ('uploaded_at',)
    fields = (('file', 'uploaded_at'),)


class CommentInline(admin.StackedInline):
    model = Comment
    prepopulated_fields = {"slug": ("user",)}
    can_delete = True
    verbose_name = 'Comments'
    verbose_name_plural = verbose_name
    fk_name = 'ticket'
    extra = 0
    fields = (('user', 'slug'), ('ticket'), )


class TicketAdmin(admin.ModelAdmin):
    inlines = (CommentInline, FileInline, )
    save_as = True
    save_on_top = True
    list_display = ('title', 'ticket_choices', 'date_sent', 'get_files_count')
    list_display_links = ('title', )
    search_fields = ('title', )
    fields = (('title', ), ('ticket_choices', 'date_sent'),
              )

    def get_files_count(self, instance):
        return instance.file_set.count()
    get_files_count.short_description = 'Files'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)


admin.site.register(Ticket, TicketAdmin)