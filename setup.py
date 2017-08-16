# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import pypandoc
    # for PyPI: Removing images with relative paths and their descriptions:
    import re
    LDESC = open('README.md', 'r').read()
    matches = re.findall(r'\n\n(.*(\n.+)*:\n\n!\[.*\]\((.*\))(\n\n)?)', LDESC)
    for match in matches:
        text, _, link, _ = match
        if text.startswith('http://'): continue
        LDESC = LDESC.replace(text, '')
    # Converting to rst
    LDESC = pypandoc.convert(LDESC, 'rst', format='md')
except (ImportError, IOError, RuntimeError):
    LDESC = ''

setup(name='smrt',
      version = '0.1.dev',
      description = 'Python package and software for the TP-Link TL-SG105E and TL-SG108E smart switches',
      long_description = LDESC,
      author = 'Philipp Klaus',
      author_email = 'philipp.l.klaus@web.de',
      url = 'https://github.com/pklaus/smrt',
      license = 'GPL',
      #packages = ['smrt', 'smrt.discovery', 'smrt.operations', 'smrt.protocol', 'smrt.smrt'],
      packages = ['smrt'],
      entry_points = {
          'console_scripts': [
              'smrt.cli = smrt.smrt:main',
              'smrt.discovery = smrt.discovery:main',
          ],
      },
      include_package_data = True,
      zip_safe = True,
      platforms = 'any',
      install_requires = ['netifaces'],
      extras_require = {
          #'savescreen':  ["Pillow",],
      },
      #package_data = {
      #    '': ['resources/*.png'],
      #},
      keywords = 'TP-Link TL-SG105E TL-SG108E',
      classifiers = [
          'Development Status :: 4 - Beta',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Scientific/Engineering :: Visualization',
          'Topic :: Scientific/Engineering',
          'Topic :: System :: Hardware :: Hardware Drivers',
          'Intended Audience :: Science/Research',
      ]
)


