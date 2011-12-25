# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) 2011 Propertyshelf, Inc. and its Contributors.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
###############################################################################
"""MLS API utility methods."""

# python imports
import logging

# zope imports
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

# local imports
from mls.apiclient.client import ListingResource
from mls.apiclient.exceptions import MLSError
from plone.mls.core.interfaces import IMLSSettings
from plone.mls.listing import PRODUCT_NAME


logger = logging.getLogger(PRODUCT_NAME)


def recent_listings(params={}, batching=True):
    search_params = {
        'sort_on': 'created',
        'reverse': '1',
    }
    search_params.update(params)
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IMLSSettings)
    base_url = getattr(settings, 'mls_site', None)
    api_key = getattr(settings, 'mls_key', None)
    batch = None
    results = []
    resource = ListingResource(base_url, api_key=api_key, debug=True)

    try:
        results, batch = resource.search(search_params)
    except MLSError, e:
        logger.warn(e)

    if batching:
        return results, batch
    return results
