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
"""Test Setup of plone.mls.listing."""

# python imports
import unittest2 as unittest

# local imports
from plone.mls.listing.testing import PLONE_MLS_LISTING_INTEGRATION_TESTING


class TestSetup(unittest.TestCase):
    """Setup Test Case for plone.mls.listing."""
    layer = PLONE_MLS_LISTING_INTEGRATION_TESTING

    def test_plone_mls_core_installed(self):
        """Test that plone.mls.core is installed."""
        portal = self.layer['portal']
        qi = portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('plone.mls.core'))

    def test_plone_app_dexterity_installed(self):
        """Test that plone.app.dexterity is installed."""
        portal = self.layer['portal']
        qi = portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('plone.app.dexterity'))

    def test_raptus_article_core_installed(self):
        """Test that raptus.article.core is installed.

        Note that raptus.article.core is only installed automatically in tests
        so that we can test the article integration.
        """
        portal = self.layer['portal']
        qi = portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('raptus.article.core'))
