# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.forms.utils import flatatt
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from .easytag import EasyTag

register = template.Library()

if not hasattr(settings, "BOOTSTRAP_TEMPLATETAGS_STYLE"):
    raise AttributeError(
        "settings.BOOTSTRAP_TEMPLATETAGS_STYLE is unset; please use 'bootstrap2' or 'bootstrap3'."
    )


def stop_unsupported_use(tag, style, required_values):
    """
    Raises a ValueError if settings.BOOTSTRAP_TEMPLATETAGS_STYLE is set inappropriately for the use
    of values in the ``required_values`` list, which is a list of 2-tuples of user-defined values
    paired to the required untampered value.
    """
    if settings.BOOTSTRAP_TEMPLATETAGS_STYLE == style:
        for arg, default_value in required_values:
            if arg != default_value:
                raise ValueError("%s's '%s' option not available for %s" % (tag.name, arg, style))


class BaseBootstrapTag(EasyTag):
    """Provides simplified template fragment rendering. Should not be directly registered."""

    templates = {}

    def render_template(self, name, version=settings.BOOTSTRAP_TEMPLATETAGS_STYLE, **context):
        """
        Looks up ``name`` as a key to the tag's ``templates`` dictionary attribute and returns the
        rendered string content.
        """
        name = self.templates[name]
        content = render_to_string("{version}/{name}".format(version=version, name=name), context)
        return mark_safe(content)


class BootstrapAccordion(BaseBootstrapTag):
    name = "bootstrap_accordion"
    intermediate_tags = ["group", "panel"]
    end_tag = True

    templates = {
        "wrapper": "accordion/wrapper.html",
        "heading": "accordion/heading.html",
        "body": "accordion/body.html",
        "panel": "accordion/panel.html",
    }

    def render(self, context):
        """Wraps the entire output with the accordion div."""
        content = super(BootstrapAccordion, self).render(context)
        return self.render_template("wrapper", id=self.id, content=mark_safe(content))

    def bootstrap_accordion(
        self, context, nodelist, id, active_panel=1, style="default", use_title=False
    ):
        """
        Main handler, typically empty, but specifies the HTML id.

        If provided, ``active_panel`` is a 1-based index to override which panel is expanded by
        default.

        For Bootstrap 3, ``style`` controls the class type that will be applied to all panels in the
        group (unless a panel declares its own ``style`` argument).  This option is unavailable for
        Bootstrap 2, since legacy accordions did not support this 'type' paradigm.

        For Bootstrap 3, ``use_title`` is optionally a string between 'h1' and 'h6' to describe the
        desire for an HTML title heading around the clickable panel text.  This produces, for
        example, <h1 class="panel-title> <a ...></a> </h1>" instead of just a link.
        """

        stop_unsupported_use(
            self,
            "bootstrap2",
            [
                (style, "default"),
                (use_title, False),
            ],
        )

        if self not in context.render_context:
            context.render_context[self] = {"counter": 0}

        self.id = id
        self.active_index = active_panel
        self.global_style = style
        self.use_title = use_title
        return nodelist.render(context)

    def group(self, context, nodelist, heading, style="default"):
        import warnings

        warnings.warn(
            "The bootstrap_accordion's {% group %} tag is deprecated; use {% panel %}" " instead",
            DeprecationWarning,
        )
        return self.panel(context, nodelist, heading, style=style)

    def panel(self, context, nodelist, heading, style=None):
        """
        Renders a simple header text and treats the following template content as the panel's body
        content.
        """

        stop_unsupported_use(self, "bootstrap2", [(style, None)])

        content = nodelist.render(context)
        context.render_context[self]["counter"] += 1
        i = context.render_context[self]["counter"]
        active = "in" if self._is_active(i, context) else ""
        data = {
            "id": self.id,
            "i": i,
            "active": active,
            "heading": heading,
            "body": content,
            "use_title": self.use_title,
        }
        panel_heading = self.render_template("heading", **data)
        panel_body = self.render_template("body", **data)
        return self.render_template(
            "panel",
            panel_heading=panel_heading,
            panel_body=panel_body,
            style=(style or self.global_style),
            **data,
        )

    def _is_active(self, i, context):
        return context.render_context[self]["counter"] == self.active_index


register.tag(BootstrapAccordion.name, BootstrapAccordion.parser)


class BootstrapNavTabs(BaseBootstrapTag):
    name = "bootstrap_navtabs"
    intermediate_tags = ["tab"]
    end_tag = True

    templates = {
        "wrapper": "navtabs/wrapper.html",
        "tab": "navtabs/tab.html",
        "panels_wrapper": "navtabs/panels_wrapper.html",
        "panel": "navtabs/panel.html",
    }

    def render(self, context):
        """Wraps the entire output with the ul.nav.nav-tabs container."""
        content = super(BootstrapNavTabs, self).render(context)

        # Mark rendered pieces as safe!
        tabs = self.render_template("wrapper", content=mark_safe(content))
        panels = self.render_template(
            "panels_wrapper", content=mark_safe(self.render_content_panels(context))
        )
        return "".join([tabs, panels])

    def bootstrap_navtabs(self, context, nodelist, active_tab=1):
        """Usually empty opening node handler."""
        if self not in context.render_context:
            context.render_context[self] = {
                "tabs": [],
                "counter": 0,
            }

        self.active_index = active_tab

        return nodelist.render(context)

    def tab(self, context, nodelist, label, id=None, show=True, active=False, **data_attrs):
        context.render_context[self]["counter"] += 1
        i = context.render_context[self]["counter"]

        if not id:
            id = slugify(label)
        if active or self._is_active(i, context):
            if show:
                active = "active"
            else:
                # If the active index is actually not showing, push it down by one
                active = ""
                self.active_index += 1
        else:
            active = ""

        # Store away certain data for rendering the panel
        context.render_context[self]["tabs"].append(
            {
                "tab_id": id,
                "active": active,
                "show": show,
            }
        )

        if show:
            # Render the panel innards, but don't return the string data yet
            context.render_context[self]["tabs"][-1]["content"] = nodelist.render(context)

            # Render the tab part
            data_attrs = flatatt(dict((k.replace("_", "-"), v) for k, v in enumerate(data_attrs)))
            return self.render_template(
                "tab", label=label, active=active, tab_id=id, data_attrs=data_attrs
            )
        return ""

    def render_content_panels(self, context):
        """Custom end handler to append output outside of the tabs wrapper."""
        content_panels = []
        for tab in context.render_context[self]["tabs"]:
            if tab["show"]:
                content_panels.append(self.render_template("panel", **tab))
        return "".join(content_panels)

    def _is_active(self, i, context):
        return context.render_context[self]["counter"] == self.active_index


register.tag(BootstrapNavTabs.name, BootstrapNavTabs.parser)
