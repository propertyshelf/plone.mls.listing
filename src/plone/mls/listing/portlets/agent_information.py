# -*- coding: utf-8 -*-
"""Agent Information Portlet."""

from plone.app.portlets.portlets import base
from plone.mls.listing import PLONE_4
from plone.mls.listing import PLONE_5
from plone.mls.listing.browser.interfaces import IListingDetails
from plone.mls.listing.i18n import _
from plone.mls.listing.portlets.agent_contact import IAgentContactPortlet
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRetriever
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implementer
from zope.schema.fieldproperty import FieldProperty


if PLONE_4:
    from zope.formlib import form


MSG_PORTLET_DESCRIPTION = _(
    u'This portlet shows the corresponding agent information for a given '
    u'listing. Note that this portlet is only available for the detail view '
    u'of a listing.',
)


class IAgentInformationPortlet(IPortletDataProvider):
    """A portlet displaying agent information for a listing."""

    heading = schema.TextLine(
        description=_(
            u'Custom title for the portlet. If no title is provided, the '
            u'default title is used.'),
        required=False,
        title=_(u'Portlet Title'),
    )


@implementer(IAgentInformationPortlet)
class Assignment(base.Assignment):
    """Agent Information Portlet Assignment."""

    heading = FieldProperty(IAgentInformationPortlet['heading'])
    title = _(u'MLS: Agent Information')

    def __init__(self, heading=None):
        self.heading = heading


class Renderer(base.Renderer):
    """Agent Information Portlet Renderer."""

    if PLONE_5:
        render = ViewPageTemplateFile('templates/p5_agent_information.pt')
    elif PLONE_4:
        render = ViewPageTemplateFile('templates/agent_information.pt')

    @property
    def available(self):
        return IListingDetails.providedBy(self.view) and \
            getattr(self.view, 'listing_id', None) is not None

    @property
    def title(self):
        return self.data.heading or _(u'Agent Information')

    @property
    def agent_contact_portlet_available(self):
        for column in ['plone.leftcolumn', 'plone.rightcolumn']:
            manager = getUtility(IPortletManager, name=column)
            retriever = getMultiAdapter(
                (self.context, manager),
                IPortletRetriever,
            )
            portlets = retriever.getPortlets()
            for portlet in portlets:
                if IAgentContactPortlet.providedBy(portlet['assignment']):
                    return True
        return False


class AddForm(base.AddForm):
    """Add form for the Agent Information portlet."""
    if PLONE_5:
        schema = IAgentInformationPortlet
    elif PLONE_4:
        form_fields = form.Fields(IAgentInformationPortlet)
    label = _(u'Add Agent Information portlet')
    description = MSG_PORTLET_DESCRIPTION

    def create(self, data):
        assignment = Assignment()
        if PLONE_4:
            form.applyChanges(assignment, self.form_fields, data)
        return assignment


class EditForm(base.EditForm):
    """Edit form for the Agent Information portlet."""
    if PLONE_5:
        schema = IAgentInformationPortlet
    elif PLONE_4:
        form_fields = form.Fields(IAgentInformationPortlet)
    label = _(u'Edit Agent Information portlet')
    description = MSG_PORTLET_DESCRIPTION
