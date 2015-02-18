#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009-2012 Zuza Software Foundation
# Copyright 2014-2015 Evernote Corporation
#
# This file is part of Pootle.
#
# Pootle is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# Pootle is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Pootle; if not, see <http://www.gnu.org/licenses/>.

import sys

from django.conf import settings


# Minimum Translate Toolkit version required for Pootle to run.
TTK_MINIMUM_REQUIRED_VERSION = (1, 11, 0)

# Minimum Django version required for Pootle to run.
DJANGO_MINIMUM_REQUIRED_VERSION = (1, 7, 4)

# Minimum lxml version required for Pootle to run.
LXML_MINIMUM_REQUIRED_VERSION = (2, 2, 2, 0)

# Minimum Redis server version required.
# Initially set to some minimums based on:
# 1. Ubuntu 12.04LTS's version 2.8.4 (10.04LTS was too old for RQ)
# 2. RQ requires >= 2.6.0, and
# 3. Wanting to insist on at least the latest stable that devs are using i.e.
#    2.8.* versions of Redis
REDIS_MINIMUM_REQUIRED_SERVER_VERSION = (2, 8, 4)


##########################
# Test core dependencies #
##########################

def test_translate():
    try:
        from translate.__version__ import ver, sver
        if ver >= TTK_MINIMUM_REQUIRED_VERSION:
            return True, sver
        else:
            return False, sver
    except ImportError:
        return None, None


def test_django():
    from django import VERSION, get_version
    if VERSION >= DJANGO_MINIMUM_REQUIRED_VERSION:
        return True, get_version()
    else:
        return False, get_version()


def test_lxml():
    try:
        from lxml.etree import LXML_VERSION, __version__
        if LXML_VERSION >= LXML_MINIMUM_REQUIRED_VERSION:
            return True, __version__
        else:
            return False, __version__
    except ImportError:
        return None, None


def test_redis_server_version():
    from django_rq.queues import get_queue
    queue = get_queue()
    redis_version_string = queue.connection.info()['redis_version']
    redis_version = tuple([int(x) for x in redis_version_string.split(".")])
    if redis_version >= REDIS_MINIMUM_REQUIRED_SERVER_VERSION:
        return True, redis_version_string
    else:
        return False, redis_version_string


def test_cache():
    """Test if cache backend is Redis."""
    if getattr(settings, "CACHES", None):
        return "RedisCache" in settings.CACHES['default']['BACKEND']


def test_cache_server_connection():
    """Test if we can connect to the cache server."""
    from django_redis import get_redis_connection
    return get_redis_connection()


##############################
# Test optional dependencies #
##############################


def test_iso_codes():
    import gettext
    languages = (lang[0] for lang in settings.LANGUAGES)
    if not languages:
        # There are no UI languages, which is a problem, but we won't complain
        # about that here.
        languages = ['af', 'ar', 'fr']
    return len(gettext.find('iso_639', languages=languages, all=True)) > 0


def test_levenshtein():
    try:
        import Levenshtein
        return True
    except ImportError:
        return False


######################
# Test optimal setup #
######################

def test_mysqldb():
    try:
        import MySQLdb
        return True
    except ImportError:
        return False


def test_db():
    """Test that we are not using sqlite3 as the django database."""
    if getattr(settings, "DATABASES", None):
        return "sqlite" not in settings.DATABASES['default']['ENGINE']


def test_session():
    """Test that session backend is set to cache or cache_db."""
    return settings.SESSION_ENGINE.split('.')[-1] in ('cache', 'cached_db')


def test_debug():
    return not settings.DEBUG


def test_webserver():
    """Test that webserver is apache."""
    return ('apache' in sys.modules or
            '_apache' in sys.modules or
            'mod_wsgi' in sys.modules)


def test_from_email():
    return bool(settings.DEFAULT_FROM_EMAIL)


def test_contact_email():
    return bool(settings.CONTACT_EMAIL)
