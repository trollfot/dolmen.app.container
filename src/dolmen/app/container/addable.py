# -*- coding: utf-8 -*-

import os.path
import dolmen.content
from cromlech.browser import IRenderable
from cromlech.container.constraints import checkFactory
from cromlech.i18n import ILanguage
from dolmen.location import get_absolute_url
from dolmen.template import TALTemplate
from grokcore.security import require
from zope.cachedescriptors.property import Lazy
from zope.component import getUtilitiesFor
from zope.interface import implements
from zope.security import checkPermission
from zope.security.checker import CheckerPublic

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')


def check_factory_permission(container, name, factory):
    """Verifies the factory and the right of the logged user against
    the container and the required permission of the content type.
    """
    permission = require.bind('zope.Public').get(factory.factory)
    if permission == 'zope.Public':
        permission = CheckerPublic
    return checkPermission(permission, container)


def get_valid_factories(container):
    for name, factory in getUtilitiesFor(dolmen.content.IFactory):
        if checkFactory(container, name, factory):
            yield name, factory


def get_addable_factories(container):
    for name, factory in get_valid_factories(container):
        if check_factory_permission(container, name, factory):
            yield name, factory


class AddMenu(object):
    implements(IRenderable)

    template = TALTemplate(os.path.join(TEMPLATE_DIR, 'addmenu.pt'))

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def target_language(self):
        return ILanguage(self.request, None)

    @Lazy
    def context_url(self):
        return get_absolute_url(self.context, self.request)

    def get_factory_url(self, name, factory):
        return u'%s/add/%s' % (self.context_url, name)

    def namespace(self):
        return {'entries': self.factories}

    def update(self, *args, **kwargs):
        """Gathers the factories allowed for the context container
        in a list of factories information useable by the template.
        """
        self.factories = []
        for name, factory in get_addable_factories(self.context):
            factory_class = factory.factory
            self.factories.append(dict(
                name=name,
                id=name.replace(".", "-"),
                url=self.get_factory_url(name, factory),
                title=factory_class.__content_type__,
                description=(factory.description or
                             factory_class.__doc__),
                ))

    def render(self, *args, **kwargs):
        return self.template.render(
            self, target_language=self.target_language, **self.namespace())
