# -*- coding: utf-8 -*-
"""Setup handlers for plone.mls.listing."""

# python imports
import pkg_resources

# zope imports
from Products.CMFPlone.interfaces import INonInstallable
from plone import api
from zope.interface import implementer

LISTING_TYPE = 'plone.mls.listing.listing'
ADD_ONS = [
    'ps.plone.fotorama',
]


def setup_article(context):
    """Set up raptus.article."""
    if not context.readDataFile('plone.mls.listing_various.txt'):
        return

    quickinstaller = api.portal.get_tool(name='portal_quickinstaller')
    portal_types = api.portal.get_tool(name='portal_types')
    if quickinstaller.isProductInstalled('raptus.article.core'):
        article = portal_types.get('Article', None)
        if article is None:
            return
        if LISTING_TYPE not in article.allowed_content_types:
            article.allowed_content_types += (LISTING_TYPE, )


def install_add_ons(context):
    """Install additional available add-ons."""
    if not context.readDataFile('plone.mls.listing_various.txt'):
        return

    quickinstaller = api.portal.get_tool(name='portal_quickinstaller')

    for item in ADD_ONS:
        try:
            pkg_resources.get_distribution(item)
        except pkg_resources.DistributionNotFound:
            continue

        # Only install add-ons which are not installed yet.
        if not quickinstaller.isProductInstalled(item):
            if quickinstaller.isProductInstallable(item):
                try:
                    quickinstaller.installProduct(item)
                except AttributeError:
                    pass


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'plone.mls.listing:uninstall',
        ]
