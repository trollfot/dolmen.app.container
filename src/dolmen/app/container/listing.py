# -*- coding: utf-8 -*-

from os import path
from cromlech.browser import IRenderer
from cromlech.container.interfaces import IContainer
from dolmen.app.container import MF as _
from dolmen.forms.base import Fields
from dolmen.forms.base.interfaces import IFormData, IField
from dolmen.forms.base.widgets import DisplayFieldWidget
from dolmen.forms.table import BaseTable
from dolmen.location import get_absolute_url
from dolmen.template import TALTemplate
from grokcore.component import baseclass, adapts, context, name, title
from zope.i18n import translate
from zope.interface import Interface, implements
from zope.location.interfaces import ILocation


TEMPLATE_DIR = path.join(path.dirname(__file__), 'templates')


class FolderListing(BaseTable):
    title(u"Content")

    css_class = "listing sortable"

    fields = Fields(ILocation).omit('__parent__')
    fields['__name__'].mode = 'link'

    @property
    def title(self):
        return u"<h1>%s</h1>" % translate(
            _(u'Folder contents'), context=self.request)


class LinkWidget(DisplayFieldWidget):
    name('link')
    adapts(IField, IFormData, Interface)

    template = TALTemplate(path.join(TEMPLATE_DIR, 'link.pt'))

    def update(self):
        DisplayFieldWidget.update(self)
        content = self.form.getContentData().getContent()
        self.url = get_absolute_url(content, self.request)


class ListingRenderer(object):
    implements(IRenderer)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def namespace(self):
        return {}

    def update(self):
        self.table = FolderListing(self.context, self.request)
        self.table.update()

    def render(self):
        return self.table.render()
