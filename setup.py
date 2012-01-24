from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.app.container'
version = '2.0.1'
readme = open(join("src", "dolmen", "app", "container", "README.txt")).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'unidecode',
    'cromlech.browser >= 0.4',
    'cromlech.container',
    'cromlech.i18n',
    'dolmen.content >= 2.0a1',
    'dolmen.forms.base',
    'dolmen.forms.ztk >= 2.0',
    'dolmen.forms.table >= 2.0',
    'dolmen.location',
    'dolmen.template',
    'grokcore.component',
    'grokcore.security',
    'setuptools',
    'zope.cachedescriptors',
    'zope.component',
    'zope.dublincore',
    'zope.i18n',
    'zope.i18nmessageid',
    'zope.interface',
    'zope.location',
    'zope.security',
    ]

tests_require = [
    'cromlech.io [test]',
    'cromlech.browser [test]',
    ]

setup(name = name,
      version = version,
      description = 'Containers tools for Dolmen applications',
      long_description = readme + '\n\n' + history,
      keywords = 'Cromlech Dolmen Container',
      author = 'Souheil Chelfouh',
      author_email = 'trollfot@gmail.com',
      url = 'http://gitweb.dolmen-project.org/',
      download_url = '',
      license = 'GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages = ['dolmen', 'dolmen.app'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      tests_require = tests_require,
      install_requires = install_requires,
      extras_require = {'test': tests_require},
      test_suite="dolmen.app.container",
      classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
)
