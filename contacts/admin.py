from django.contrib import admin

from .models import Contact, Inquiry


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'listing', 'email', 'contact_date')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email', 'listing')
    list_per_page = 25


class InquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'ref_id',
                    'last_updated', 'nda_sent')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email', 'ref_id')
    list_per_page = 25


admin.site.register(Contact, ContactAdmin)
admin.site.register(Inquiry, InquiryAdmin)
