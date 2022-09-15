from django.template import library
from django import template
register = template.Library()

@register.filter(name='reverse_date')
def reverse_date(value):
  dakika,saniye = divmod(value, 60)
  saat,dakika=divmod(dakika, 60)
  line="{} saat {} dakika {} saniye".format(saat,dakika,saniye)
  return line
register.filter('reverse_date', reverse_date)