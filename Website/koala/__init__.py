from pyramid.config import Configurator

#To Store Sessions
from pyramid.session import SignedCookieSessionFactory
my_session_factory = SignedCookieSessionFactory('itsaseekreet')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('.models')
        config.include('pyramid_jinja2')
        config.include('.routes')
        config.include(".security")
        config.set_session_factory(my_session_factory)
        config.scan()


    return config.make_wsgi_app()
