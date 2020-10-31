from django.contrib import admin 
from django.db import models 
from django.forms import Textarea, TextInput, NumberInput

from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline, TranslationStackedInline
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin




    
class AbstractContentAdmin(
    ImportExportActionModelAdmin, 
    ImportExportModelAdmin,
    TabbedTranslationAdmin,
    ):
    def has_add_permission(self, request, obj=None):
        return False 
    def has_delete_permission(self, request, obj=None):
        return False 

    pass 



class AbstractTextAdmin(AbstractContentAdmin):
    pass 
  
class AbstractLinkAdmin(AbstractTextAdmin):
    pass
