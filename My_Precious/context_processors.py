# My_Precious/context_processors.py


# noinspection PyUnusedLocal
def google_maps_api_key(request):
    # value request is needed to enable google maps
    from django.conf import settings

    return {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY}
