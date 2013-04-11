# -*- coding: utf-8 -*-

from cromlech.browser import IRenderable, HTMLWrapper
from dolmen.app.container import MF as _
from dolmen.forms.base import Fields
from dolmen.forms.table import BaseTable
from grokcore.component import title
from zope.i18n import translate
from zope.interface import implements
from zope.location.interfaces import ILocation


class FolderListing(BaseTable):
    title(u"Content")

    css_class = "listing sortable"

    tableFields = Fields(ILocation).omit('__parent__')
    tableFields['__name__'].mode = 'link'

    @property
    def title(self):
        return u"<h1>%s</h1>" % translate(
            _(u'Folder contents'), context=self.request)

    def render(self, *args, **kwargs):
        return self.template.render(
            self, target_language=self.target_language, **self.namespace())

    def updateWidgets(self):
        return super(FolderListing, self).updateWidgets()


class ListingRenderer(object):
    implements(IRenderable)

    tableFactory = FolderListing
    
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update(self):
        self.table = self.tableFactory(self.context, self.request)
        self.table.update()
        self.table.updateForm()

    def render(self):
        html = HTMLWrapper()
        table = self.table
        return html('\n' +
            table.title.encode('utf-8') + '\n' +
            table.render().encode('utf-8'))
