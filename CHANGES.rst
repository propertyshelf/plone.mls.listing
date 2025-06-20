Changelog
=========

1.24 (unreleased)
-----------------

- Nothing changed yet.


1.23 (2025-06-20)
-----------------

- Add a new configuration option to check if a listing detail view should be displayed based on the listing collection settings.
- Bug fix: when getting the settings for a page, only check for collections and searches which are currently active.


1.22 (2025-04-22)
-----------------

- Add the ability to switch between different mapping providers (Google Map, Mapbox, and Maptiler).
- Fix some problematic translations
- Fix the "See More Details" link to only show when there is a long description available.


1.21 (2023-08-04)
-----------------

- Update the sender address so that listing inquiries originate from the portal address.


1.20 (2020-03-09)
-----------------

- Change position of listing description in Plone 5.
- Add option for grid layout to listing collections, searches, and recent listings.
- Add number of results for listing collections.


1.19 (2019-05-20)
-----------------

- Add live chat embedding code to development listings.
- Allow line breaks and parragraph spacing in listing descriptions.
- Remove the "Agent Quote" and modify the way the long description is shown.


1.18 (2018-05-30)
-----------------

- Fix random api key usage.


1.17 (2018-05-18)
-----------------

- Allow multiple API keys.


1.16 (2017-12-12)
-----------------

- Add dependency to ps.plone.mls.
- Remove controlpanel settings from GS profiles (now handled by ps.plone.mls).
- Truncate description for listings in summaries with global configuration.
- Make fotorama default slideshow.


1.15 (2017-09-05)
-----------------

- Add class pat-select2 for valuerange widget.


1.14 (2017-08-21)
-----------------

- Hide location fields completely, don't use hidden mode.
- Don't index print listing pages.
- Adjust listing search form template for Plone 5.
- Add custom quick search portlet form template for Plone 5.
- Fix get link method for tcwidget (now supports UIDs).


1.13 (2017-05-26)
-----------------

- Add city field to listing collection.
- Add workflow_state to listing search config.
- Add location fields to listing search config. Hide all location fields in search form when one option is pre-selected.
- Add auto-search option for listing searches.
- Use custom vocabulary for available listing searches for quick search portlet (migration included).


1.12 (2017-05-12)
-----------------

- Allow freetext search using the searchable_text index in the MLS.
- Update translations.
- Fix listing search portlet and viewlet form availablilty.
- Use custom prefix for listing search forms to avoid form clashing.


1.11 (2017-04-24)
-----------------

- Add Plone 5 compatibility.
- Add option to show unverified MLS listings.
- Removed JS modal dialogs for MLS configuration views.


1.10 (2017-04-12)
-----------------

- Use plone.api.portal.send_email to send emails. Fixes utf-8 encoding issues.


1.9 (2017-04-04)
----------------

- In agent contact form, use sender for email 'from', instead of 'reply-to'.


1.8.2 (2016-11-07)
------------------

- Fix CSS.


1.8.1 (2016-10-17)
------------------

- Fix manifest.


1.8 (2016-10-17)
----------------

- Add single beds and baths for listings (hidden with CSS by default).
- Use high resolution lead image for listing collections, if available.
- Add listing description for listing collections (hidden with CSS by default).
- Add calculated price for listings (hidden with CSS by default).
- Remove colons after labels from listing templates (now added via CSS).
- Clean up listing templates.
- Fix base_url for print listing links.
- Remove international phone validator from agent contact form again.
- Added setting for required status of agent contact form phone field.
- Added backport of custom title and dublin core viewlets from ps.plone.mls.
- Update buildout environment.
- Fix code-analysis errors.
- Remove Google Maps API from portal_javascripts.
- Google Maps now uses configured API key.


1.7.1 (2016-05-24)
------------------

- Remove wrong class names from listing detail template.
- Add living and interior area for print listing template.


1.7 (2016-05-20)
----------------

- Add CSS classes to listing summary fields.
- Fix wrong title for agent contact portlet add and edit forms.
- Update german translations.
- Show interior area and living area in listing summary, if available.
- Add agency priority ordering to recent listings and listing search.
- Agent contact form field 'phone' is now required.
- Agent contact form field 'zipcode' is now not required anymore.
- Use formencode's international phone validator for agent contact phone field.
- I18N updates.


1.6.1 (2016-02-18)
------------------

- [Bugfix] string formatting to accept special characters in unicode strings.


1.6 (2016-02-18)
----------------

- Fix canonical links for listing details pages within a collection to point to itself instead of the collection page.
- Add a canonical link from the listing print page to the actual listing page.


1.5.1 (2016-02-17)
------------------

- Inherit TCWidget from SingleCheckBox.
  This fixes the 'Object is of wrong type.' error.
- Dynamically add data fields to agent contact email message.
- I18N updates.


1.5 (2016-02-16)
----------------

- Add new fields (country, zip and accept terms & conditions) to agent contact portlet.
  Fields can be configured to be shown or not.
  A link to an internal document can be set for the terms & conditions.


1.4 (2016-02-10)
----------------

- Show availability calendar for rental listings, if available.
- Listing map is now shown below the listing details section.
- Fixed GenericSetup import step dependencies.


1.3 (2015-12-22)
----------------

- Fixed wrong JS code for map in listing details.
- Bugfix: The interior area search is now mapped to the 'floor_area' index, which applies to both residential and commercial types.


1.2 (2015-12-3)
----------------

- Add workflow state options for Active, PendingSale, and Sold to listing collection configuration.
- Add sort options to configuration for Listing Collections.
- Add the reverse sort parameter as a configurable option in Listing Collections.
- Add the agency priority option and override agency ID option to Listing Collections.
- Add lot size, interior area, bedroom, bathroom configuration options to listing collections.
- Bugfix: special characters in geocoordinates cause errors when trying to view the listing.


1.1 (2015-10-06)
----------------

- add MultiSelect widgets to ListingCollections
- migrate existing ListingCollections



1.0 (2015-09-02)
----------------

- add Geolocation map
- change sort order for RecentListings to "last activated"


0.9.22 (2015-06-15)
-------------------

- Email templates are i18n message strings in order to be translatable.


0.9.21 (2015-05-07)
-------------------

- mobile improvement ListingDetails
- additional spacing around embedding video
- added migration step


0.9.20 (2015-05-07)
-------------------

- ListingQuickSearch Portlet: fix JQuery Error
- ListingDetails: add css for responsive Video embedding


0.9.19 (2015-05-06)
-------------------

- Listing Details template: add Listing Video


0.9.18 (2015-01-30)
-------------------

- Fixed migration step from 1008 to 1009.


0.9.17 (2015-01-30)
-------------------

- Make a copy of the field before changing its attributes.
- Make ps.plone.fotorama dependency optional.


0.9.16 (2014-11-24)
-------------------

- Listing Details template: add field id CSS class to tabbed ListingDetails.
- Removed kupu integration.
- Support galleria and fotorama slideshow.
- Added MLS UI settings controlpanel. Allows selection of slideshow plugin.


0.9.15 (2014-09-17)
-------------------

- Limit listing types in searches if restricted and no listing type is selected.
- Show no results found message when no search results available.
- I18N updates.


0.9.14 (2014-09-15)
-------------------

- Support 'filtered' vocabularies for e.g. search options.
- Support filtering of listing types within the search.
- Include phone number in contact email.
- I18N updates.


0.9.13 (2014-08-21)
-------------------

- Don't send a copy of the agent contact portlet message to the sender.
- Added override recipient to agent contact portlet. Use this to redirect all emails to that address for (spam) review.
- Add info about the original agent to the contact form email. Referral agents need to be able to contact the responsible listing agent.
- I18N updates.


0.9.12 (2014-07-14)
-------------------

- Added option to filter listing results for the current agency.
- Add css classes for agent info portlet fields.
- I18N updates.


0.9.11 (2014-03-17)
-------------------

- Fixed UnicodeDecodeError for contact portlet.
- I18N updates.


0.9.10 (2014-02-24)
-------------------

- Allow local agency information.
- Show phone number for all listing types in agent contact portlet.
- I18N updates.


0.9.9 (2014-01-31)
------------------

- Fixed traversal conflict with contentleadimage.
- I18N updates.


0.9.8 (2014-01-18)
------------------

- Added agent avatar URL field.
- Fixed portlet reistartions so we can customise them now.
- I18N updates.


0.9.7 (2013-07-02)
------------------

- Changed default search result order to creation date (reversed).


0.9.6 (2013-06-28)
------------------

- Fixed tal error in portlet template.


0.9.5 (2013-06-27)
------------------

- CI with travis-ci.
- Removed dependency to raptus.article.


0.9.4 (2013-06-26)
------------------

- Fixed JS for configuration view overlays.
- CSS fixes.


0.9.3 (2013-06-11)
------------------

- [Bugfix] Set captcha widget after fields are set up.


0.9.2 (2013-06-11)
------------------

- Hide contact info for agent info portlet if contact portlet is available.
- Added fields to agent contact form for residential lease.
- Use transparent background for galleria slideshow container.
- Hide county and district from quick search portlet.
- Add collective.captcha based captcha for agent contact form.


0.9.1 (2013-03-27)
------------------

- I18N updates.


0.9 (2013-03-27)
----------------

- Added lot size and interior size to listing search.
- Made lookup values translatable.
- I18N updates.


0.8 (2012-08-20)
----------------

- Added Agent Contact portlet.
- Added Quick Search portlet.
- Show custom agent info if 3rd party listing and option for showing custom info is selected.


0.7.1 (2012-06-15)
------------------

- Adjusted listing detail view to new api fields.
- I18N updates.


0.7 (2012-06-13)
----------------

- Adjusted viewlets so they can be customized through the ZMI.
- Added noValueMessage adapter for listing forms.
- I18N updates.


0.6 (2012-03-22)
----------------

- Added agent quote section (incl. images and styles).


0.5 (2012-02-14)
----------------

- Added missing i18n ids (#1744).
- I18N updates (es, ja).


0.4 (2012-02-11)
----------------

- Registered I18N locales folder.


0.3 (2012-02-11)
----------------

- I18N updates merged.
- Added SearchOptions cache objects for listing search categories. Defaults to 1 hour ram cache.


0.2 (2012-02-05)
----------------

- Use plone.app.testing for tests.
- Upgraded dexterity content types. Requires plone.app.dexterity >= 1.1.
- Added 'Recent Listings' viewlet with configuration.
- Added 'Listing Collection' viewlet with configuration.
- Added 'Listing Search' viewlet with configuration.
- Added API methods to access the MLS API. Requires mls.apiclient.
- Added Infinite Ajax Scroll JavaScript (disabled by default) for Facebook like scroll and auto-load of next items.
- Added I18N.
- Adjusted raptus.article based views (don't use tables anymore).


0.1.2 (2011-10-26)
------------------

- Bugfix: Plone 4.1.x compatibility.


0.1.1 (2011-09-07)
------------------

- BUGFIX: Added missing get_language import.


0.1 (2011-09-07)
----------------

- Added language support.


0.1rc3 (2011-06-04)
-------------------

- Fixed location info traceback if listing does not exist.


0.1rc2 (2011-05-26)
-------------------

- Added missing lead image to list of images.
- Updated css for listing slideshow.


0.1rc1 (2011-05-26)
-------------------

- Added custom browserlayer and custom css file.
- Added migrations for browserlayer and css.
- Added Galleria JS Slideshow.
- Disable 'Link using UID's in TinyMCE.


0.1b2 (2011-05-24)
------------------

- Added versioning for dexterity content type.


0.1b1 (2011-05-23)
------------------

- Added description and long description to detail view.
- Added listing to linkable types (TinyMCE and Kupu).
- Moved images on top below the listing information.
- Added configuration for raptus.article.
- Added article integration.


0.1dev (2011-05-18)
-------------------

- First Beta Release.
