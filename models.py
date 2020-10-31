from django.db import models 
from tinymce import HTMLField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone 
from django.core.exceptions import ValidationError
from box.core import settings as core_settings

from box.core.models import BaseMixin, AbstractPage
from .abstract_models import (
  AbstractContent, AbstractText, AbstractLink,
)
from .validators import validate_phone_number

class Page(AbstractPage):
  """
  У Page code blank=False, null=False тому що по цьому коду він викликається у
  функціях, які рендерять шаблони. 
  """
  code  = models.SlugField(
    verbose_name=_("Код"), blank=False, null=False, 
    unique=True, max_length=255, help_text=("Код сторінки"),
  )
  title = models.CharField(
    verbose_name=_("Заголовок"), blank=True, null=True, 
    max_length=255, help_text=("Назва сторінки"),
  )

  class Meta:
    verbose_name        = _("cторінка")
    verbose_name_plural = _("cторінки")

  def __str__(self):
    title = '' 
    if self.title:title = self.title 
    return f'{self.code} {title}'


class Map(AbstractContent):
  html = models.TextField(
    verbose_name=_("iframe"), 
    blank=False, null=False,
  )
  class Meta:
    verbose_name = _("карта")
    verbose_name_plural = _("карти")
    ordering = [
      '-updated',
    ]


class Img(AbstractContent):
  image   = models.ImageField(verbose_name=_("Картинка"), upload_to="page/", null=True, blank=True, help_text=("Картинка, яка буде відображатися на сайті"))
  alt     = models.CharField(verbose_name=_("Альт"), blank=True, null=True, max_length=255)

  class Meta:
    verbose_name        = _("картинка")
    verbose_name_plural = _("картинки")
    ordering = [
      '-updated',
    ]

  @classmethod
  def modeltranslation_fields(cls):
    fields = [
      'alt',
    ]
    return fields

  @property
  def image_url(self):
    return self.image.url if self.image else ''


class Text(AbstractText):
  class Meta:
    verbose_name=_("переклад")
    verbose_name_plural=_("переклади")
    ordering = [
      '-updated',
    ]


class Address(AbstractLink):
  class Meta:
    verbose_name=_("адрес")
    verbose_name_plural=_("адреса")
    ordering = [
      '-updated',
    ]


class Tel(AbstractLink):
  class Meta:
    verbose_name = _("телефонний номер")
    verbose_name_plural = _("телефонні номера")
    ordering = [
      '-updated',
    ]
  def clean(self):
    valid = validate_phone_number(self.href)
    if not valid:
      raise ValidationError(_("Номер має бути без пробілів, без літер, без спецсимволів, починатися з + та містити в собі 13 символів. Приклад: +380957891234."))


class Mailto(AbstractLink):
  class Meta:
    verbose_name = _("емейл")
    verbose_name_plural = _("емейли")
    ordering = [
      '-updated',
    ]


class Link(AbstractLink):
  class Meta:
    verbose_name = _("посилання")
    verbose_name_plural = _("посилання")
    ordering = [
      '-updated',
    ]


# class Social(models.Model):
#   img 
#   href 


class Slide(BaseMixin):
    code       = models.SlugField(verbose_name=_("Код"), max_length=255, blank=False, null=False, unique=True)
    page      = models.ForeignKey(verbose_name=_("Сторінка"), to="sw_content.Page", related_name="slides", on_delete=models.SET_NULL, blank=True, null=True)
    image     = models.ImageField(verbose_name=_("Зображення"), blank=False, null=False)
    slider    = models.ForeignKey(verbose_name=_("Слайдер"), to='sw_content.Slider', related_name='slides', on_delete=models.SET_NULL, null=True, blank=False) 
    name      = models.CharField(verbose_name=_("Назва"), max_length=255, blank=True, null=True)  
    alt       = models.CharField(verbose_name=_("Назва зображення(alt)"), max_length=255, blank=True, null=True) 
    title     = models.CharField(verbose_name=_("Вспливаюча підказка(title)"), max_length=255, blank=True, null=True)  
    text      = models.TextField(verbose_name=_("Текст"), blank=True, null=True)  

    # TODO: настройки для лобецького
    # DISPLAY_CHOICES = (
    #     ("no_text", "Зображення без тексту"),
    #     ("text_toned", "Текст на зображенні з тонуванням"),
    #     ("text_right", "Текст праворуч, зображення зліва"),
    #     ("text_left", "Текст зліва, зображення праворуч"),
    # )
    # display   = models.CharField(verbose_name=_("Варіант відображення"), choices=DISPLAY_CHOICES, max_length=255, default=0)  
    # mw_desc   = models.IntegerField(verbose_name=_("Максимальна ширина дексктопі"), default=1050)  
    # mh_desc   = models.IntegerField(verbose_name=_("Максимальна висота на дексктопі"), default=400)  
    # mw_mob    = models.IntegerField(verbose_name=_("Максимальна ширина мобілках"), default=500)  
    # mh_mob    = models.IntegerField(verbose_name=_("Максимальна висота на мобілках"), default=320)  

    def __str__(self):
        return f'{self.id}'
    
    
    def save(self, *args, **kwargs):
        if not self.page:
            if self.slider:
                if self.slider.page:
                    self.page = self.slider.page 
        super().save(*args, **kwargs)
    
    @property
    def slider_name(self):
        slider_name = ''
        if self.slider:
            slider_name = self.slider.name 
        return slider_name 
    
    @property
    def image_url(self):
        image_url = core_settings.IMAGE_NOT_FOUND
        if self.image:
            image_url = self.image.url
        return image_url 
    
    def get_image_url(self):
        image_url = core_settings.IMAGE_NOT_FOUND
        if self.image:
            image_url = self.image.url
        return image_url 
    
    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
            'alt',
            'title',
            'text',
        ]
        return fields

    class Meta:
        verbose_name = ('Слайд')
        verbose_name_plural = ('Слайди')
        ordering = ['order']


class Slider(BaseMixin):
    code = models.SlugField(verbose_name=_("Код"), max_length=255, blank=False, null=False, unique=True)
    name = models.CharField(verbose_name=_("Назва"), max_length=255, blank=True, null=True)
    page = models.ForeignKey(
        verbose_name=("Сторінка"), 
        to="sw_content.Page", 
        related_name='sliders', 
        blank=True,
        null=True, 
        on_delete=models.SET_NULL,
    )
    # SPEED_HELP = ("Застосовується при включеному автоперелистуванні слайдів. Вказується в мілісекундах.")
    # as_slider  = models.BooleanField(verbose_name=_('Група банерів як слайдер'), default=True)
    # auto       = models.BooleanField(verbose_name=_('Автоперегортання слайдів'), default=True)
    # infinite   = models.BooleanField(verbose_name=_('"Нескінченний" слайдер'), default=True)
    # arrows     = models.BooleanField(verbose_name=_('Стрілки навігації (наступний / попередній)'), default=True)
    # navigation = models.BooleanField(verbose_name=_('Точки навігації слайдів'), default=True)
    # speed      = models.PositiveIntegerField(verbose_name=_('Швидкість зміни слайдів'), blank=True, null=True, default=6500, help_text=SPEED_HELP)

    def __str__(self):
        return f'{self.name}'
    
    def save(self, *args, **kwargs):
        if self.page:
            Slide.objects.all().filter(slider=self).update(page=self.page)
        super().save(*args, **kwargs)

    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
        ]
        return fields

    class Meta:
        verbose_name = ('Слайдер')
        verbose_name_plural = ('Слайдери')
        ordering = ['order']




from django.db import models 
from django.shortcuts import reverse 
from box.core.models import BaseMixin
from django.utils.translation import gettext_lazy as _

class Faq(BaseMixin):
    name      = models.CharField(verbose_name=_("Назва"), max_length=255)
    answer    = models.TextField(verbose_name=_("Відповідь"))

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = ("FAQ")
        verbose_name_plural = ("FAQ")
        ordering = ['order']
    
    def get_absolute_url(self):
        try:
            return reverse("faq", kwargs={"pk": self.pk})
        except:
            return '' 
    
    @classmethod
    def modeltranslation_fields(cls):        
        fields = [
            'name',
            'answer',
        ]
        return fields


