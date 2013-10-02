from django import template

from rca.models import EventItem, NewsItem
from datetime import date
from django.db.models import Min, Max

register = template.Library()

# FIXME: order by should really be on the first dates_times object
@register.inclusion_tag('rca/includes/modules/upcoming_events.html', takes_context=True)
def upcoming_events(context, count=3):
    events = EventItem.objects.annotate(start_date=Min('dates_times__date_from'), end_date=Max('dates_times__date_to')).filter(end_date__gte=date.today()).order_by('start_date')[:count]
    return {
        'events': events,
        'request': context['request'],  # required by the {% pageurl %} tag that we want to use within this template
    }

@register.inclusion_tag('rca/includes/modules/carousel-news.html', takes_context=True)
def news_carousel(context, area="", programme="", count=6):
    if area:
        news_items = NewsItem.objects.filter(area=area)[:count]
    elif programme:
        news_items = NewsItem.objects.filter(related_programmes__programme=programme)[:count]
    return {
        'news_items': news_items,
        'request': context['request'],  # required by the {% pageurl %} tag that we want to use within this template
    }

@register.inclusion_tag('rca/includes/modules/upcoming_events_by_programme.html', takes_context=True)
def upcoming_events_by_programme(context, opendays=0, programme=""):
    events = EventItem.objects.annotate(start_date=Min('dates_times__date_from'), end_date=Max('dates_times__date_to')).filter(end_date__gte=date.today()).filter(related_programmes__programme=programme).order_by('start_date')
    if opendays:
        events = events.filter(audience='openday')
    else:
        events = events.exclude(audience='openday')
    return {
        'events': events,
        'request': context['request'],  # required by the {% pageurl %} tag that we want to use within this template
    }
