#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2009-2015 Zuza Software Foundation
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

import os
from io import BytesIO
from zipfile import ZipFile
from django.core.servers.basehttp import FileWrapper
from django.http import Http404, HttpResponse
from pootle_store.models import Store
from translate.storage import po


def download(contents, name, content_type):
    response = HttpResponse(contents, content_type=content_type)
    response["Content-Disposition"] = "attachment; filename=%s" % (name)
    return response


def export(request):
    path = request.GET.get("path")
    if not path:
        raise Http404

    stores = Store.objects.filter(pootle_path__startswith=path)
    num_items = stores.count()

    if not num_items:
        raise Http404

    if num_items == 1:
        store = stores.get()
        contents = BytesIO(store.serialize())
        name = os.path.basename(store.pootle_path)
        contents.seek(0)
        return download(contents.read(), name, "application/octet-stream")

    # zip all the stores together
    f = BytesIO()
    prefix = path.strip("/").replace("/", "-")
    if not prefix:
        prefix = "export"
    with BytesIO() as f:
        with ZipFile(f, "w") as zf:
            for store in stores:
                zf.writestr(prefix + store.pootle_path, store.serialize())

        return download(f.getvalue(), "%s.zip" % (prefix), "application/zip")


def _import_file(file):
    pofile = po.pofile(file.read())
    pootle_path = pofile.parseheader().get("X-Pootle-Path")
    if not pootle_path:
        raise ValueError("File %r missing X-Pootle-Path header\n" % (file.name))

    try:
        store, created = Store.objects.get_or_create(pootle_path=pootle_path)
    except Exception as e:
        raise ValueError("Could not import %r. Bad X-Pootle-Path? (%s)" % (file.name, e))

    store.update(store=pofile)


def import_(request):
    for file in request.FILES.values():
        if is_zipfile(file):
            with ZipFile(filename, "r") as zf:
                for path in zf.namelist():
                    _import_file(f)
        else:
            with open(file) as f:
                _import_file(f)

    return HttpResponse("OK")
