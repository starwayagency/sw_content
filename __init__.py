from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class PageConfig(AppConfig):
    name = 'box.core.sw_content'
    verbose_name = _('Контент')
    def ready(self):
        from django.urls import path 
        from django.conf import settings 
        # from box.core.sw_content.urls import urlpatterns
        # from box.core.sw_content.views import pages_generator
        # urls_in_db = settings.CMS_TEMPLATES
        # for url_in_db in urls_in_db:
        #     urlpatterns.append(path(url_in_db,
        #                             pages_generator,
        #                             {'param':url_in_db},
        #                             name=url_in_db)
        #     )





default_app_config = 'box.core.sw_content.PageConfig'



'''
AbstractContent(page, code, created, updated)
  Img (AbstractContent + image, alt)
  Map (AbstractContent + html)
  AbstractText (AbstractContent + text )
    Text
    AbstractLink (AbstractText + href )
      Address
      Link
      Tel 
      Mailto

Img
  page, code, created, updated,
  image, alt,

Map
  page, code, created, updated,
  html,

Text
  page, code, created, updated,
  text,

Address
  page, code, created, updated,
  text,


Link
  page, code, created, updated,
  text,
  href,


Tel
  page, code, created, updated,
  text,
  href,


Mailto
  page, code, created, updated,
  text,
  href,
'''