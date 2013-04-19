#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2008 Zuza Software Foundation
#
# This file is part of Pootle.
#
# Pootle is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Pootle is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pootle; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from django.conf.urls import patterns, url

urlpatterns = patterns('pootle_app.views.language.view',
    # Translation
    url(r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/(?P<dir_path>(.*/)*)translate.html$',
        'translate', name='translate-wide'),

    # XHR
    (r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/(?P<dir_path>(.*/)*)checks.html$',
        'get_failing_checks_dir'),
    (r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/(?P<dir_path>(.*/)*)view.html$',
        'get_view_units_dir'),

    # VCS
    (r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/(?P<file_path>.*)/commit$',
        'commit_file'),
    (r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/(?P<file_path>.*)/update$',
        'update_file'),
    (r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/(?P<dir_path>(.*/)*)commit_all$',
        'commit_all'),
    (r'^(?P<language_code>[^/]*)/(?P<project_code>[^/]*)/(?P<dir_path>(.*/)*)update_all$',
        'update_all'),
)
