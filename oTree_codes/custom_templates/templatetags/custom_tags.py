from django import template
import os, json
from custom_templates.custom_funcs import get_box
import hashlib
register = template.Library()

@register.inclusion_tag('_data_display.html')
def data_display(data):
    return {
        'data': data
    }

@register.inclusion_tag('_delayed_next.html')
def delayed_next(wait=2000, label='NEXT'):
    return {
        'wait_time': wait,
        'label': label
    }

@register.inclusion_tag('_counting_task.html')
def counting_box(field_name='test', img=None, num_zeros=None):
    next_page=True
    if (img is None):
        img, num_zeros = get_box()

    return {
        'img': os.path.join('boxes', img),
        'answer': hashlib.md5((str(num_zeros)).encode("utf-8")).hexdigest(),
        'field_name': field_name,
        'next_page': next_page
    }
@register.inclusion_tag('_counting_task_practice.html')
def counting_box_practice(field_name='test', img=None, num_zeros=None):
    next_page=True
    if (img is None):
        img, num_zeros = get_box()

    return {
        'img': os.path.join('boxes', img),
        'answer': hashlib.md5((str(num_zeros)).encode("utf-8")).hexdigest(),
        'field_name': field_name,
        'next_page': next_page
    }
