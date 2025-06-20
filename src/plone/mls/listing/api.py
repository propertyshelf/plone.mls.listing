# -*- coding: utf-8 -*-
"""MLS API utility methods."""

from Acquisition import aq_inner
from Acquisition import aq_parent
from DateTime import DateTime
from mls.apiclient.client import ListingResource
from mls.apiclient.exceptions import MLSError
from plone import api
from plone.mls.core.api import get_settings
from plone.mls.listing import PRODUCT_NAME
from plone.mls.listing.browser.interfaces import IListingCollection
from plone.mls.listing.browser.interfaces import IListingSearch
from plone.mls.listing.browser.interfaces import IRecentListings
from plone.mls.listing.browser.localconfig import CONFIGURATION_KEY
from plone.mls.listing.interfaces import ILocalAgencyInfo
from plone.mls.listing.interfaces import IMLSAgencyContactInformation
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility

import copy
import logging
import time


LISTING_COLLECTION_KEY = 'plone.mls.listing.listingcollection'
LISTING_SEARCH_KEY = 'plone.mls.listing.listingsearch'
RECENT_LISTINGS_KEY = 'plone.mls.listing.recentlistings'

logger = logging.getLogger(PRODUCT_NAME)
# Store the options here (which means in RAM)
OPTIONS_CACHE = {}  # language_category: ({date, language, category, itemlist})


def _remove_omitted(params, omit):
    """Removed omitted keys from the params dict."""
    if omit is not None and isinstance(omit, (list, tuple)):
        for item in omit:
            try:
                del params[item]
            except KeyError:
                continue


def prepare_search_params(data, omit=None):
    """Prepare search params."""
    params = {}

    _remove_omitted(data, omit)

    for item in data:
        if item == 'interior_area':
            # change data and key to 'floor_area' instead of 'interior_area'
            item = 'floor_area'
            data[item] = data.get('interior_area')
            data.pop('interior_area', None)

        if item in ['baths', 'beds', 'lot_size', 'floor_area']:
            min_max = data[item]
            if isinstance(min_max, (list, tuple)):
                if len(min_max) > 0 and min_max[0] != '--MINVALUE--':
                    params[item + '_min'] = min_max[0]
                if len(min_max) > 1 and min_max[1] != '--MAXVALUE--':
                    params[item + '_max'] = min_max[1]
                continue

        # Convert lists and tuples to comma separated lists.
        if isinstance(data[item], (list, tuple)):
            if len(data.get(item, ())) > 0:
                data[item] = ','.join(data[item])
            else:
                data[item] = None

        # Remove all None-Type values.
        if data[item] is not None:
            value = data[item]
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            params[item] = value
    return params


class SearchOptions(object):
    """Cached search options."""

    # time in minutes after which we retry to load it after a failure
    FAILURE_DELAY = 10
    category = None
    language = None
    timeout = 100

    def __init__(self, category, language, timeout, context=None):
        self.category = category
        self.language = language
        self.timeout = timeout
        self.context = context

        self._items = []
        self._loaded = False  # Is the category already loaded?
        self._failed = False  # Does it fail with the last update?
        self._last_update_time_in_minutes = 0  # When was the last update?
        self._last_update_time = None  # Time as DateTime or Now.

    @property
    def last_update_time_in_minutes(self):
        """return the time the last update was done in minutes"""
        return self._last_update_time_in_minutes

    @property
    def last_update_time(self):
        """return the time the last update was done in minutes"""
        return self._last_update_time

    @property
    def update_failed(self):
        return self._failed

    @property
    def ok(self):
        return (not self._failed and self._loaded)

    @property
    def loaded(self):
        """return whether this feed is loaded or not"""
        return self._loaded

    @property
    def needs_update(self):
        """check if this feed needs updating"""
        now = time.time() / 60
        return (self.last_update_time_in_minutes + self.timeout) < now

    def update(self):
        """update this feed"""
        now = time.time() / 60

        # check for failure and retry
        if self.update_failed:
            if (self.last_update_time_in_minutes + self.FAILURE_DELAY) < now:
                return self._retrieveCategory()
            else:
                return False

        # check for regular update
        if self.needs_update:
            return self._retrieveCategory()

        return self.ok

    def _retrieveCategory(self):
        """do the actual work and try to retrieve the feed"""
        if self.category is not None:
            self._last_update_time_in_minutes = time.time() / 60
            self._last_update_time = DateTime()
            settings = get_settings(context=self.context)
            base_url = settings.get('mls_site', None)
            api_key = settings.get('mls_key', None)
            debug = api.env.debug_mode
            resource = ListingResource(base_url, api_key=api_key, debug=debug)
            results = []
            try:
                results = resource.category(self.category, self.language)
            except MLSError as e:
                self._loaded = True  # we tried at least but have a failed load
                self._failed = True
                logger.warn(e)
                return False
            self._items = results
            self._loaded = True
            self._failed = False
            return True
        self._loaded = True
        self._failed = True  # no url set means failed
        return False  # no url set, although that should not really happen

    @property
    def items(self):
        return self._items


def search_options(mls_url, category, lang=None, context=None):
    if mls_url is None or len(mls_url) < 1:
        return

    timeout = 60
    key = mls_url + category + '_' + str(lang)
    options = OPTIONS_CACHE.get(key, None)

    if options is None:
        options = SearchOptions(category, lang, timeout, context=context)

        if options.update():
            OPTIONS_CACHE[key] = options
    else:
        options.update()

    return options.items


def recent_listings(params={}, batching=True, context=None, config=None):
    """Return a list of recent MLS listings."""
    search_params = {
        'sort_on': 'last_activated_date',
        'reverse': '1',
    }
    search_params.update(params)
    return search(
        params=search_params,
        batching=batching,
        context=context,
        config=config,
    )


def get_all_listing_configs(context=None, merged=False):
    """Return all available configurations."""
    result = {}
    if not context:
        return result
    annotations = IAnnotations(context)
    keys = []
    if IListingCollection.providedBy(context):
        keys.append(LISTING_COLLECTION_KEY)
    elif IListingSearch.providedBy(context):
        keys.append(LISTING_SEARCH_KEY)
    elif IRecentListings.providedBy(context):
        keys.append(RECENT_LISTINGS_KEY)
    for key in keys:
        config = annotations.get(key, {})
        if merged:
            result.update(config)
        else:
            result[key] = config
    return result


def listing_details(listing_id, lang=None, context=None):
    """Return detail information for a listing."""
    settings = get_settings(context=context)
    base_url = settings.get('mls_site', None)
    api_key = settings.get('mls_key', None)
    debug = api.env.debug_mode
    config = get_all_listing_configs(context=context, merged=True)

    # if check_valid_listing is set, we need to ensure the listing exists
    if settings.get('check_valid_listing', False):
        params_search = {}
        params_search['listing_ids'] = [listing_id]
        params_search.update(config)
        params_search = prepare_search_params(params_search)
        results = search(
            params=params_search,
            batching=False,
            context=context,
            config=config,
        )
        if not results or len(results) == 0:
            return None

    # if we have a valid listing, we can continue
    params = {}
    if config.get('show_unverified', False):
        params['apiowner'] = settings.get('agency_id')
        params['show_unverified'] = True
    if config.get('show_unverified_only', False):
        params['show_unverified_only'] = True
    resource = ListingResource(base_url, api_key=api_key, debug=debug)
    try:
        listing = resource.get(listing_id, lang=lang, params=params)
    except MLSError as e:
        logger.warn(e)
        return None
    listing = listing.get('listing', None)
    if listing is not None:
        agent = copy.deepcopy(listing.get('contact', {}).get('agent'))
        listing['original_agent'] = agent
    return listing


def search(params={}, batching=True, context=None, config=None):
    """Search for listings."""
    if config is None:
        config = {}
    settings = get_settings(context=context)
    search_params = {
        'sort_on': 'last_activated_date',
        'reverse': '1',
    }
    if config.get('show_unverified', False):
        search_params['apiowner'] = settings.get('agency_id')
    listing_types = set(config.get('listing_type', ()))
    if listing_types:
        # Available Listing Types are restricted.
        search_listing_types = params.get('listing_type', None)
        if search_listing_types:
            search_listing_types = set(search_listing_types.split(','))
            listing_types = listing_types.intersection(search_listing_types)
        params['listing_type'] = ','.join(listing_types)
    agency_listings = params.pop('agency_listings', False)
    agency_priority = params.get('agency_priority', False)
    if agency_listings is True or agency_priority is True:
        agency_id = params.pop('overriding_agency_id', None)
        if not agency_id:
            agency_id = settings.get('agency_id', None)
        agency_id = agency_id.replace(' ', '')
        search_params['agency_id'] = agency_id
    freetext = config.get('freetext')
    if freetext:
        params['q'] = freetext
    search_params.update(params)
    base_url = settings.get('mls_site', None)
    api_key = settings.get('mls_key', None)
    batch = None
    results = []
    debug = api.env.debug_mode
    resource = ListingResource(base_url, api_key=api_key, debug=debug)

    try:
        results, batch = resource.search(search_params)
    except MLSError as e:
        logger.warn(e)

    if batching:
        return results, batch
    return results


def _local_agency_info(context):
    """Get local agency information."""
    settings = None
    obj = context
    while (
            not IPloneSiteRoot.providedBy(obj) and
            not ILocalAgencyInfo.providedBy(obj)):
        parent = aq_parent(aq_inner(obj))
        if parent is None:
            return
        obj = parent
    if ILocalAgencyInfo.providedBy(obj):
        annotations = IAnnotations(obj)
        settings = annotations.get(
            CONFIGURATION_KEY, annotations.setdefault(CONFIGURATION_KEY, {}))
    return settings


def get_agency_info(context=None):
    """Get the agency information."""
    if context is None:
        context = api.portal.get()

    local_info = _local_agency_info(context)
    if local_info is not None:
        logger.debug('Returning local agency information.')
        return local_info

    # Get the global agency info.
    settings = {}
    registry = getUtility(IRegistry)
    if registry is not None:
        try:
            registry_settings = registry.forInterface(  # noqa
                IMLSAgencyContactInformation,
            )
        except Exception:
            logger.warning('Global agency information not available.')
        else:
            settings = dict([
                (a, getattr(registry_settings, a)) for a in
                registry_settings.__schema__
            ])
            logger.debug('Returning global agency information.')
    if not settings.get('use_custom_info', False):
        return
    return settings
