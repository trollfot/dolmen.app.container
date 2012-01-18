# -*- coding: utf-8 -*-

import os.path
import dolmen.content
from dolmen.viewlet import Viewlet
from cromlech.container.constraints import checkFactory
from cromlech.container.interfaces import IContainer
from dolmen.location import get_absolute_url
from dolmen.template import TALTemplate
from grokcore.security import context, require, baseclass
from zope.component import getUtilitiesFor
from zope.security import checkPermission
from zope.security.checker import CheckerPublic


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')


class AddMenuViewlet(Viewlet):
    baseclass()
    context(IContainer)

    template = TALTemplate(os.path.join(TEMPLATE_DIR, 'addmenu.pt'))

    def checkFactory(self, name, factory):
        """Verifies the factory and the right of the logged user against
        the container and the required permission of the content type.
        """
        if not checkFactory(self.context, name, factory):
            return False

        permission = require.bind('zope.Public').get(factory.factory)
        if permission == 'zope.Public':
            permission = CheckerPublic
        return checkPermission(permission, self.context)

    def update(self):
        """Gathers the factories allowed for the context container
        in a list of factories information useable by the template.
        """
        self.factories = []
        self.contexturl = get_absolute_url(self.context, self.request)

        for name, factory in getUtilitiesFor(dolmen.content.IFactory):
            # We iterate and check the factories
            if self.checkFactory(name, factory):
                factory_class = factory.factory
                self.factories.append(dict(
                    name=name,
                    id=name.replace(".", "-"),
                    url='%s/++add++%s' % (self.contexturl, name),
                    title=factory_class.__content_type__,
                    description=(factory.description or
                                 factory_class.__doc__),
                    ))
