# -*- coding: utf-8 -*-

import uuid
import grokcore.component as grok
from unicodedata import normalize
from cromlech.container.interfaces import IContainer, INameChooser
from zope.dublincore.interfaces import IDCDescriptiveProperties


class UUIDNameChooser(grok.Adapter):
    grok.baseclass()
    grok.context(IContainer)
    grok.implements(INameChooser)
    
    def checkName(self, name, object):
        return not name in self.context

    def chooseName(self, name, object):
        return str(uuid.uuid1())


class NormalizingNameChooser(grok.Adapter):
    grok.baseclass()
    grok.context(IContainer)
    grok.implements(INameChooser)

    retries = 100

    def checkName(self, name, object):
        return not name in self.context

    def _findUniqueName(self, name, object):
        if not name in self.context:
            return name

        idx = 1
        while idx <= self.retries:
            new_name = "%s_%d" % (name, idx)
            if not new_name in self.context:
                return new_name
            idx += 1

        raise ValueError(
            "Cannot find a unique name based on "
            "`%s` after %d attemps." % (name, self.retries))

    def chooseName(self, name, object):
        if not name:
            dc = IDCDescriptiveProperties(object, None)
            if dc is not None and dc.title:
                name = dc.title.strip()
                ascii = normalize('NFKD', name).encode('ascii', 'ignore')
                name = ascii.replace(' ', '_').lower()
            else:
                name = object.__class__.__name__.lower()

        return self._findUniqueName(name, object)
