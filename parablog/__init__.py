import datetime
from pyramid.config import Configurator
from pyramid.renderers import JSON


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    json_renderer = JSON()

    def datetime_adapter(obj, request):
        return obj.isoformat().replace('T', ' ')
    json_renderer.add_adapter(datetime.datetime, datetime_adapter)

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')

    config.add_renderer('json', json_renderer)
    config.add_renderer(None, json_renderer)  # set as default renderer

    config.scan()
    return config.make_wsgi_app()
