#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Ino de Bruijn'
SITENAME = u'Data Trop Cuit'
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

MENUITEMS = (("ino.pm", "http://www.ino.pm"),)

# Bootstrap conf
BOOTSTRAP_NAVBAR_INVERSE = True
PYGMENTS_STYLE = 'friendly'
DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False
SHOW_ARTICLE_CATEGORY = True
DISPLAY_CATEGORIES_ON_SIDEBAR = True
