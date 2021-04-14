from roiback.settings import *  # NOQA


# Remove documentation form drf
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)