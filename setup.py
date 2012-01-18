from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.app.container'
version = '2.0a1'
readme = open(join("src", "dolmen", "app", "container", "README.txt")).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'dolmen.app.layout >= 2.0',
    'dolmen.app.security',
    'dolmen.container',
    'dolmen.content >= 0.7',
    'dolmen.menu',
    'dolmen.view',
    'dolmen.viewlet',
    'grokcore.component',
    'setuptools',
    'zope.component',
    'zope.dublincore',
    'zope.i18n',
    'zope.i18nmessageid',
    'zope.interface',
    'zope.security',
    ]

tests_require = [
    'zope.configuration',
    'zope.schema',
    'zope.securitypolicy',
    'zope.testing',
    ]

setup(name = name,
      version = version,
      description = 'Containers tools for Dolmen applications',
      long_description = readme + '\n\n' + history,
      keywords = 'Grok Zope3 CMS Dolmen',
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
        'Framework :: Zope3',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
)
