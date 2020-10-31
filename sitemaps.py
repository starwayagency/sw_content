from django.contrib.sitemaps import Sitemap 
from .models import Page


class PageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 1
    protocol = 'https'
    i18n = True 

    def items(self):
        return Page.objects.all()
        
    def lastmod(self, obj):
        return obj.updated

    def location(self, obj):
        return obj.get_absolute_url()

