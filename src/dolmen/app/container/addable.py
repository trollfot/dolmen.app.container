# -*- coding: utf-8 -*-

import os.path
import dolmen.content
from cromlech.browser import IRenderer
from cromlech.container.constraints import checkFactory
from cromlech.i18n import ILanguage
from dolmen.location import get_absolute_url
from dolmen.template import TALTemplate
from grokcore.security import require
from zope.component import getUtilitiesFor
from zope.interface import implements
from zope.security import checkPermission
from zope.security.checker import CheckerPublic


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')


def check_factory_permission(container, name, factory):
    """Verifies the factory and the right of the logged user against
    the container and the required permission of the content type.
    """
    if not checkFactory(container, name, factory):
        return False

    permission = require.bind('zope.Public').get(factory.factory)
    if permission == 'zope.Public':
        permission = CheckerPublic
    return checkPermission(permission, container)


class AddMenuViewlet(object):
    implements(IRenderer)

    template = TALTemplate(os.path.join(TEMPLATE_DIR, 'addmenu.pt'))

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def namespace(self):
        return {}

    @property
    def target_language(self):
        return ILanguage(self.request, None)

    def update(self, *args, **kwargs):
        """Gathers the factories allowed for the context container
        in a list of factories information useable by the template.
        """
        self.factories = []
        contexturl = get_absolute_url(self.context, self.request)

        for name, factory in getUtilitiesFor(dolmen.content.IFactory):
            # We iterate and check the factories
            if check_factory_permission(self.context, name, factory):
                factory_class = factory.factory
                self.factories.append(dict(
                    name=name,
                    id=name.replace(".", "-"),
                    url='%s/++add++%s' % (contexturl, name),
                    title=factory_class.__content_type__,
                    description=(factory.description or
                                 factory_class.__doc__),
                    ))

    def render(self, *args, **kwargs):
        return self.template(
            self, target_language=self.target_language, entries=self.factories)
