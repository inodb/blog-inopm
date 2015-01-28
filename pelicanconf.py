#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Ino de Bruijn'
SITENAME = u'Ino de Bruijn'
#SITEURL = 'http://blog.ino.pm'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
#LINKS =  (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),
#          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('twitter', 'http://twitter.com/inodb'),
          ('linkedin', 'http://www.linkedin.com/in/inodb'),
          ('github', 'http://github.com/inodb'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# Widgets
TWITTER_USERNAME = "inodb"
TWITTER_WIDGET_ID = 460780344342364160
#GITHUB_USER = "inodb"

THEME = "pelican-bootstrap3"
#BOOTSTRAP_THEME = 'readable'

MENUITEMS = (("About", "http://www.ino.pm"),
             ("CV", "http://ino.pm/docs/ino_de_bruijn_cv.pdf"))
TIMEZONE = "Europe/Stockholm"
USE_FOLDER_AS_CATEGORY = True
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = True

AUTHOR_SAVE_AS = ''
DIRECT_TEMPLATES = ('tags', 'archives')

# Bootstrap conf
BOOTSTRAP_NAVBAR_INVERSE = True
PYGMENTS_STYLE = 'friendly'
SHOW_ARTICLE_CATEGORY = True
DISPLAY_CATEGORIES_ON_SIDEBAR = False
HIDE_SITENAME = True
DISPLAY_TAGS_INLINE = True
TYPOGRIFY = True
DISPLAY_BREADCRUMBS = False
HIDE_SIDEBAR = False
#AVATAR = "ola"
#ABOUT_ME = '<img src="https://1.gravatar.com/avatar/c299bc8a8166b38033cd9258c34360c7?d=https%3A%2F%2Fidenticons.github.com%2Fba823da16b7cb66ed74a55a6bce91f13.png&r=x&s=440" width="220" height="220" alt="Blog logo">'

## IPython notebook conf
#MARKUP = ('rst', 'md', 'ipynb')
#PLUGIN_PATHS = ['./plugins']
#PLUGINS = ['ipynb']
#IGNORE_FILES = ["*-checkpoint.ipynb"]
