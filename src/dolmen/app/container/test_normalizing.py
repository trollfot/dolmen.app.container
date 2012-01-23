# -*- coding: utf-8 -*-
"""Namechoosing normalization
"""

from cromlech.container.components import Container
from dolmen.app.container import NormalizingNamechooser
from zope.interface import implements
from zope.dublincore.interfaces import IDCDescriptiveProperties


class Content(object):
  implements(IDCDescriptiveProperties)

  def __init__(self, title):
      self.title = title
      self.description = u""


def test_unicode_names():
    """
    """
    container = Container()
    chooser = NormalizingNamechooser(container)
    
    jani = Content(u'Jani')
    assert chooser.chooseName('', jani) == 'jani'

    jani = Content(u'Jani Räisänen-Célêt')
    assert chooser.chooseName('', jani) == 'jani_raisanen-celet'

    beijing = Content(u'北京')
    assert chooser.chooseName('', beijing) == 'bei_jing'
