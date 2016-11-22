# -*- coding: utf-8 -*-
"""Test Setup of plone.mls.listing."""

# python imports
try:
    import unittest2 as unittest
except ImportError:
    import unittest

# local imports
from plone.mls.listing.testing import PLONE_MLS_LISTING_INTEGRATION_TESTING


class TestSetup(unittest.TestCase):
    """Setup Test Case for plone.mls.listing."""
    layer = PLONE_MLS_LISTING_INTEGRATION_TESTING

    def test_plone_app_dexterity_installed(self):
        """Validate that plone.app.dexterity is installed."""
        portal = self.layer['portal']
        qi = portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('plone.app.dexterity'))

    def test_plone_mls_core_installed(self):
        """Validate that plone.mls.core is installed."""
        portal = self.layer['portal']
        qi = portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('plone.mls.core'))

    def test_ps_plone_fotorama_installed(self):
        """Validate that ps.plone.fotorama is installed."""
        portal = self.layer['portal']
        qi = portal.portal_quickinstaller
        self.assertTrue(qi.isProductInstalled('ps.plone.fotorama'))
