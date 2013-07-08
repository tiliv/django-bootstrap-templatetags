from easytag import EasyTag

from django import template

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
        self.active_panel = active_panel
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
        return context.render_context[self]['counter'] == self.active_panel

register.tag(BootstrapAccordion.name, BootstrapAccordion.parser)
