# -*- coding: utf-8 -*-

import dolmen.content as dolmen
import grokcore.viewlet as grok

from dolmen.app.layout import master, IDisplayView
from zope.security.management import checkPermission
from zope.app.container.constraints import checkFactory
from zope.component import getUtilitiesFor, getMultiAdapter
from zope.traversing.browser.absoluteurl import absoluteURL

grok.templatedir("templates")


class AddMenu(grok.Viewlet):
    grok.order(60)
    grok.view(IDisplayView)
    grok.context(dolmen.IContainer)
    grok.viewletmanager(master.AboveBody)
    grok.require("dolmen.content.Add")

    
    def checkFactory(self, name, factory):
        """Verifies the factory and the right of the logged user against
        the container and the required permission of the content type.
        """
        if not checkFactory(self.context, name, factory):
            return False

        permission = dolmen.require.bind().get(factory.factory)
        return checkPermission(permission, self.context)

        
    def update(self):
        """Gathers the factories allowed for the context container
        in a list of factories information useable by the template.
        """
        self.factories = []
        self.contexturl = absoluteURL(self.context, self.request)

        for name, factory in getUtilitiesFor(dolmen.IFactory):
            if self.checkFactory(name, factory):
                factory_class = factory.factory
                icon_view = getMultiAdapter(
                    (factory_class, self.request), name='contenttype_icon'
                    )
                
                self.factories.append(dict(
                    name = name,
                    icon = icon_view(),
                    url = '%s/++add++%s' % (self.contexturl, name),
                    title = factory_class.__content_type__,
                    description = (factory.description or
                                   factory_class.__doc__),
                    ))
