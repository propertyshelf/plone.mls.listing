# -*- coding: utf-8 -*-
"""Article Provider."""

# zope imports
from plone import api
from raptus.article.core.interfaces import IArticle
from zope.component import adapter
from zope.interface import implementer


# local imports
from plone.mls.listing.article.interfaces import IListingLists


@implementer(IListingLists)
@adapter(IArticle)
class ListingLists(object):
    """Provider for listings contained in an article."""

    def __init__(self, context):
        self.context = context

    def getListingLists(self, **kwargs):
        """Returns a list of listings (catalog brains)."""
        catalog = api.portal.get_tool(name='portal_catalog')
        return catalog(
            portal_type='plone.mls.listing.listing',
            path={
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 1,
            },
            sort_on='getObjPositionInParent', **kwargs)
