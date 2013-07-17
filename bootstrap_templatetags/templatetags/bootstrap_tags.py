from easytag import EasyTag

from django import template
from django.template.defaultfilters import slugify

register = template.Library()

class BootstrapAccordion(EasyTag):
    name = 'bootstrap_accordion'
    intermediate_tags = ['group']
    end_tag = True

    ACCORDION_WRAPPER = u"""
    <div class="accordion" id="{id}">{content}</div>
    """
    ACCORDION_HEADING = u"""
    <div class="accordion-heading">
        <a data-parent="#{id}" href="#{id}-panel-{i}" class="accordion-toggle" data-toggle="collapse">
            {heading}
        </a>
    </div>
    """
    ACCORDION_BODY = u"""
    <div id="{id}-panel-{i}" class="accordion-body collapse {active}">
        <div class="accordion-inner">
            {body}
        </div>
    </div>
    """
    ACCORDION_GROUP = u"""
    <div class="accordion-group">
        {HEADING}
        {BODY}
    </div>
    """

    def render(self, context):
        """ Wraps the entire output with the accordion div. """
        content = super(BootstrapAccordion, self).render(context)
        return self.ACCORDION_WRAPPER.format(id=self.id, content=content)

    def bootstrap_accordion(self, context, nodelist, id, active_panel=1):
        """
        Main handler, typically empty, but specifies the HTML id.

        If provided, ``active_panel`` is a 1-based index to override which panel is expanded by
        default.
        """

        if self not in context.render_context:
            context.render_context[self] = {'counter': 0}

        self.id = id
        self.active_index = active_panel
        return nodelist.render(context)

    def group(self, context, nodelist, heading):
        """
        Renders a simple header text and treats the following template content as the panel's body
        content.
        """

        content = nodelist.render(context)
        context.render_context[self]['counter'] += 1
        i = context.render_context[self]['counter']
        active = 'in' if self._is_active(i, context) else ''
        group_html = self.ACCORDION_GROUP.format(HEADING=self.ACCORDION_HEADING,
                                                 BODY=self.ACCORDION_BODY)
        return group_html.format(id=self.id, i=i, active=active, heading=heading, body=content)

    def _is_active(self, i, context):
        return context.render_context[self]['counter'] == self.active_index

register.tag(BootstrapAccordion.name, BootstrapAccordion.parser)

class BootstrapNavTabs(EasyTag):
    name = 'bootstrap_navtabs'
    intermediate_tags = ['tab']
    end_tag = True

    NAV_TABS_WRAPPER = u"""
    <ul class="nav nav-tabs">{content}</ul>
    """
    NAV_TAB = u"""
    <li class="{active}"><a data-toggle="tab" href="#{tab_id}">{label}</a></li>
    """
    NAV_PANELS_WRAPPER = u"""
    <div class="tab-content">{content}</div>
    """
    NAV_PANEL = u"""
    <div class="tab-pane {active}" id="{tab_id}">{content}</div>
    """

    def render(self, context):
        """ Wraps the entire output with the ul.nav.nav-tabs container. """
        content = super(BootstrapNavTabs, self).render(context)
        tabs = self.NAV_TABS_WRAPPER.format(content=content)
        panels = self.NAV_PANELS_WRAPPER.format(content=self.render_content_panels(context))
        return u"".join((tabs, panels))

    def bootstrap_navtabs(self, context, nodelist, active_tab=1):
        """ Usually empty opening node handler. """
        if self not in context.render_context:
            context.render_context[self] = {
                'tabs': [],
                'counter': 0,
            }

        self.active_index = active_tab

        return nodelist.render(context)

    def tab(self, context, nodelist, label, show=True, active=False):
        context.render_context[self]['counter'] += 1
        i = context.render_context[self]['counter']

        id = slugify(label)
        if active or self._is_active(i, context):
            active = 'active'
        else:
            active = ''

        # Store away certain data for rendering the panel
        context.render_context[self]['tabs'].append({
            'tab_id': id,
            'active': active,
            'show': show,

            # Render the panel innards, but don't return the string data yet
            'content': nodelist.render(context),
        })

        # Render the tab part
        if show:
            return self.NAV_TAB.format(label=label, active=active, tab_id=id)
        return ""

    def render_content_panels(self, context):
        """ Custom end handler to append output outside of the tabs wrapper. """
        content_panels = []
        for tab in context.render_context[self]['tabs']:
            if tab['show']:
                content_panels.append(self.NAV_PANEL.format(**tab))
        return u"".join(content_panels)

    def _is_active(self, i, context):
        return context.render_context[self]['counter'] == self.active_index


register.tag(BootstrapNavTabs.name, BootstrapNavTabs.parser)
