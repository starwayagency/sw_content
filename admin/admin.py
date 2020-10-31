from django.contrib import admin
from django.forms import Textarea
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.actions import delete_selected


from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline, TranslationStackedInline
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin


from box.core.utils import AdminImageWidget, move_to, BaseAdmin
from box.core.helpers import get_admin_url


from ..models import *
from ..resources import *
from ..filters import *
from ..forms import *
from .abstract_admin import * 






class BaseInline(TranslationStackedInline):
    def has_add_permission(self, request, obj=None):
        return False
    classes = [
        'collapse',
    ]
    exclude = [
        "order",
        'created',
        'updated',
    ]
    readonly_fields = [
        "page",
        'code',
    ]
    formfield_overrides = {
        models.ImageField:{'widget':AdminImageWidget},
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':25})},

    }


class ImgInline(BaseInline):
    model = Img


class MapInline(BaseInline):
    model = Map


class TextInline(BaseInline):
    model = Text


class AddressInline(BaseInline):
    model = Address


class LinkInline(BaseInline):
    model = Link


class TelInline(BaseInline):
    model = Tel


class MailtoInline(BaseInline):
    model = Mailto





class PageAdmin(
    ImportExportActionModelAdmin, 
    ImportExportModelAdmin,
    TabbedTranslationAdmin,
    ):
    resource_class = PageResource

    inlines = [
        ImgInline,
        MapInline,
        TextInline,
        AddressInline,
        LinkInline,
        TelInline,
        MailtoInline,
    ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':'2', 'cols':'25'})},
    }
    list_editable = [
        'meta_key',
    ]
    list_display = [
        'code',
        'meta_title',
        'meta_descr',
        'meta_key',
        'updated',
        'created',
    ]
    list_display_links = [
        'code',
        'meta_title',
        'meta_descr',
    ]
    search_fields = [
        'meta_title',
    ]
    exclude = [
        "order",
        'image',
        'alt',
        'title',
        'description',
        'slug',
    ]
    readonly_fields = [
        'code',
        'is_active',
        'created',
        'updated',
    ]


# AbstractContent 


class MapAdmin(AbstractContentAdmin):
    resource_class  = MapResource
    list_display    = [
        'code',
        'html',
        'updated',
        'created',
    ]
    readonly_fields = [
        "page",
        'code',
        'updated',
        'created',
    ]
    search_fields   = [
        'code',
    ]
    list_display_links = [
        'code',
        'updated',
        'created',
    ]
    list_editable = [
        'html',
    ]
    list_per_page = 20 
    list_filter = ['page']








class ImgAdmin(AbstractContentAdmin):
    resource_class = ImgResource
    list_per_page  = 20
    search_fields = [
        'code',
    ]
    formfield_overrides = {
        models.ImageField:{'widget':AdminImageWidget}
    }
    list_display_links = [
        'code',
        'show_image',
    ]
    list_display = [
        'code',
        'show_image',
        'alt',
        'updated',
        'created',
    ]
    list_filter = [
        'page',
    ]
    list_editable = [
        'alt',
    ]
    readonly_fields = [
        "page",
        'code',
        'updated',
        'created',
    ]
    def show_image(self, obj):
        return mark_safe(f'<img src="{obj.image_url}" alt={obj.alt} style="max-width:150px; height:100px"/>')
    show_image.short_description = _("Картинка")


class TextAdmin(AbstractTextAdmin):
    resource_class = TextResource
    search_fields = [
        'code',
    ]
    list_per_page = 20 
    list_editable  = [
        'text',
    ]
    list_display   = [
        'code',
        'text',
        'updated',
        'created',
    ]
    list_display_links = [
        'code',
        'updated',
        'created',
    ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':19})},
    }
    list_filter = [
        'page',
        TextIsNoneFilter
    ]
    readonly_fields = [
        "page",
        'code',
        'updated',
        'created',
    ]
    exclude = [
        'order',
        'is_active',
    ]


class AddressAdmin(AbstractTextAdmin):
    resource_class = AddressResource 
    search_fields = [
        'code',
        'text',
    ]
    list_per_page = 20
    readonly_fields = [
        "page",
        'code',
        'updated',
        'created',
    ]
    list_editable  = [
        'href',
        'text',
    ]
    list_display   = [
        'code',
        'href',
        'text',
        'updated',
        'created',
    ]
    list_display_links = [
        'code',
        'updated',
        'created',
    ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':25})},
    }
    list_filter = [
        'page',
        TextIsNoneFilter
    ]


class LinkAdmin(AbstractLinkAdmin):
    resource_class = LinkResource
    search_fields = [
        'code',
        'text',
        'href',
    ]
    list_per_page = 20
    exclude = [
        'order',
        'is_active',
    ]
    readonly_fields = [
        "page",
        'code',
        'created',
        'updated',
    ]
    list_display   = [
        'code',
        'href',
        'text',
        'created',
        'updated',
    ]
    list_display_links = [
        'code',
        'updated',
        'created',
    ]
    list_editable  = [
        'text',
        'href',
    ]
    list_filter = [
        'text',
        TextIsNoneFilter,
    ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':'1', 'cols':'25'})},
    }


class TelAdmin(AbstractLinkAdmin):
    resource_class = TelResource
    search_fields = [
        'code',
        'text',
        'href',
    ]
    list_per_page = 20
    list_display = [
        'code',
        'href',
        'text',
        'updated',
        'created',
    ]
    list_editable = [
        'text',
        'href',
    ]
    readonly_fields = [
        "page",
        'code',
        'created',
        'updated',
    ]
    list_filter = [
        'page',
        TextIsNoneFilter,
    ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':'1', 'cols':'25'})},
    }


class MailtoAdmin(AbstractLinkAdmin):
    resource_class = MailtoResource 
    list_per_page = 20
    readonly_fields = [
        "page",
        'code',
        'created',
        'updated',
    ]
    search_fields = [
        'code',
        'text',
        'href',
    ]
    list_display = [
        'code',
        'href',
        'text',
        'created',
        'updated',
    ]
    list_display_links = [
        'code',
        'updated',
        'created',
    ]
    list_editable = [
        'text',
        'href',
    ]
    list_filter = [
        'page',
        TextIsNoneFilter
    ]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':'1', 'cols':'25'})},
    }


class SlideInline(
    SortableInlineAdminMixin,
    TranslationStackedInline,
    ):
    model = Slide
    extra = 0 
    exclude = [
        "order",
        'created',
        'updated',
        'page',
        'text',
        'title',
        'alt',
        'code',
        'name',
        'is_active',
    ]
    readonly_fields = [
        "page",
        # 'code',
    ]
    classes = [
        'collapse'
    ]
    formfield_overrides = {
        models.ImageField: {'widget': AdminImageWidget}
    }


class SliderAdmin(
    ImportExportActionModelAdmin,
    ImportExportModelAdmin, 
    admin.ModelAdmin,
    ):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, requets, obj=None):
        return False  
    save_on_top = True 
        
    resource_class = SliderResource
    list_display_links = [
        'name',
        'page',
    ]
    list_display = [
        'name',
        'page',
        # "show_delete_link",
    ]
    inlines = [
        SlideInline,
    ]
    fields = [
        # 'is_active', # шоб не попливла верстка лобацького, якшо вдруг дибіляка-клієнт вдруг захоче виключити слайдер 
        'name',
        'page',
        'created',
        'updated',
        'code',
    ]
    readonly_fields = [
        "page",
        'created',
        'updated',
        'code',
    ]
    search_fields = [
        'name',
        'page',
        'code',
    ]


class SlideAdmin(
    ImportExportActionModelAdmin,
    ImportExportModelAdmin, 
    SortableAdminMixin,
    TabbedTranslationAdmin,
    ):
    # change_list 
    resource_class = SlideResource
    # TODO: перенести цей шаблон в інші адмінки, де треба імпортувати і міняти порядок.
    change_list_template = 'core/sortable_import_export_change_list.html'
    save_on_top = True 

    def show_image(self, obj):
        return mark_safe(f"<img src='{obj.get_image_url()}' height='150' width='auto' />")

    def show_delete_link(self, obj):
        return mark_safe(f'<a href="/admin/{obj._meta.app_label}/{obj._meta.model_name}/{obj.id}/change" style="color:red">x</a>')
    
    def show_slider_link(self, obj):
        return mark_safe(f'<a href="{get_admin_url(obj.slider)}">{obj.slider_name}</a>')

    show_delete_link.short_description = _("Видалити")
    show_slider_link.short_description = _("Посилання на слайдер")
    
    def change_slider(self, request, queryset):
        initial = {
            'model':Slider,
            'attr':'slider',
            'action_value':'change_slider',
            'action_type':'add',
            'text':_('Новий слайдер буде застосований для наступних позиций:'),
            'title':_("Додавання маркерів"),
            'message':_('Слайдер {0} був застосований до {1} слайдів'),
        }
        return move_to(self, request, queryset, initial)

    show_image.short_description = _("Зображення")
    change_slider.short_description = _('Перемістити в слайдер')
    actions = [
        "is_active_on",
        "is_active_off",
        'change_slider',  
    ]
    list_display = [
        'show_image',
        'name',
        "show_slider_link",
        'is_active',
        'show_delete_link',
    ]
    list_display_links = [
        'show_image',
        'name',

    ]
    list_editable = [
        'is_active',
        # 'slider',
    ]
    list_filter = [
        # 'slider',
        SliderFilter
        # TODO: slider.is_active True or False
    ]
    # change_form
    save_on_top = True 
    search_fields = [
        'name',
    ]
    fields = [
        'name',
        'image',
        'slider',
        'is_active',
        'alt',
        'title',
        # 'text',
    ]
    formfield_overrides = {
        models.ImageField:{'widget':AdminImageWidget},
    }




class FaqAdmin(
    BaseAdmin,
    SortableAdminMixin,
    TabbedTranslationAdmin,
    ):
    list_display = [
        'name',
        'is_active',
    ]
    list_display_links = [
        'name',
    ]
    list_editable = [
        'is_active',
    ]

