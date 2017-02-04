from django import template
import urllib


register = template.Library()


@register.simple_tag
def url_replace(cnx, **kwargs):
    query = cnx['request'].GET.dict()
    query.update(kwargs)
    return urllib.urlencode(query)

@register.inclusion_tag('partial_pagination.html',
                        takes_context=True)
def pagination(context, page_obj):
    current_page = page_obj.number
    total_pages = page_obj.paginator.num_pages
    total_show_pages = 6
    left_page = current_page - total_show_pages / 2 + 1
    right_page = current_page + total_show_pages / 2

    left_give_to_right = 1 - left_page if left_page -1 < 0 \
        else 0
    right_give_to_left = right_page - total_pages if \
        right_page > total_pages else 0

    right_page = min([right_page if left_give_to_right == 0 else \
        right_page + left_give_to_right, total_pages])
    left_page = max([left_page if right_give_to_left == 0 else \
                     left_page - right_give_to_left, 1])
    page_range = range(left_page, right_page + 1)

    context = {'page_range': page_range,
               'page_obj': page_obj,
               'context': context,
               'total_pages': total_pages}
    return context
