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
"""ValueRange Widget Implementation"""

# zope imports
from z3c.form.browser.widget import HTMLTextInputWidget, addFieldClass
from z3c.form.interfaces import IFieldWidget, IFormLayer, NO_VALUE
from z3c.form.widget import FieldWidget, SequenceWidget
from zope.i18n import translate
from zope.interface import implementer, implementsOnly
from zope.schema.interfaces import IField, ITitledTokenizedTerm
from zope.component import adapter

# local imports
from plone.mls.listing.i18n import _
from plone.mls.listing.browser.valuerange.interfaces import IValueRangeWidget


class ValueRangeWidget(HTMLTextInputWidget, SequenceWidget):
    """Value range widget."""
    implementsOnly(IValueRangeWidget)

    klass = u'value-range-widget'
    prompt = False

    noValueMessage = _('no value')
    promptMessage = _('select a value ...')

    # Internal attributes
    _adapterValueAttributes = SequenceWidget._adapterValueAttributes + (
                              'noValueMessage', 'promptMessage', 'prompt')

    def update(self):
        super(ValueRangeWidget, self).update()
        addFieldClass(self)

    @property
    def maximums(self):
        if self.terms is None:  # update() has not been called yet
            return []
        items = []
        selected = self.maximum

        for count, term in enumerate(self.terms):
            if term.token == '--MINVALUE--':
                continue
            id = '%s-%i' % (self.id, count)
            content = term.title or term.value
            if ITitledTokenizedTerm.providedBy(term):
                content = translate(
                    term.title, context=self.request, default=term.title)
            items.append({
                'id': id,
                'value': term.token,
                'content': content,
                'selected': term.token == selected})

#         items.append({
#             'id': self.id + '-novalue',
#             'value': '--MAXVALUE--',
#             'content': u"Max",
#             'selected': selected is None or selected == '--MAXVALUE--',
#         })

        return items

    @property
    def minimums(self):
        if self.terms is None:  # update() has not been called yet
            return ()
        items = []
        selected = self.minimum

#         items.append({
#             'id': self.id + '-novalue',
#             'value': '--MINVALUE--',
#             'content': u"Min",
#             'selected': selected is None or selected == 0,
#         })

        for count, term in enumerate(self.terms):
            if term.token == '--MAXVALUE--':
                continue
            id = '%s-%i' % (self.id, count)
            content = term.title or term.value
            if ITitledTokenizedTerm.providedBy(term):
                content = translate(
                    term.title, context=self.request, default=term.title)
            items.append({
                'id': id,
                'value': term.token,
                'content': content,
                'selected': term.token == selected})
        return items

    @property
    def maximum(self):
        maximum = self.request.get(self.name + '-max', None)
        if maximum:
            return maximum
        else:
            return u'--MAXVALUE--'

    @property
    def minimum(self):
        minimum = self.request.get(self.name + '-min', None)
        if minimum:
            return minimum
        else:
            return u'--MINVALUE--'

    def extract(self, default=NO_VALUE):
        """See z3c.form.interfaces.IWidget."""
        min_ = self.request.get(self.name + '-min', default)
        max_ = self.request.get(self.name + '-max', default)
        return (min_, max_)


@adapter(IField, IFormLayer)
@implementer(IFieldWidget)
def ValueRangeFieldWidget(field, request):
    """IFieldWidget factory for ValueRangeWidget."""
    return FieldWidget(field, ValueRangeWidget(request))
