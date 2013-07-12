django-bootstrap-templatetags
=============================

Utility templatetag library for minimizing Bootstrap scaffolding for verbose structures.

Add ``bootstrap_templatetags`` to your installed apps and then load up the ``bootstrap_tags`` library.

**Be warned** that these tags do not exist in order to get wildly fancy and create some frankendjango.  These are provided to simplify some of the heavier Bootstrap scaffolding.  In most cases, care has been taken to not modify anything about how you would normally write your template; you simply replace the scaffolding with these tags and sub-tags.

If you need any more flexibility than what is being provided by the default, vanilla Bootstrap structures, you should actually write some Bootstrap markup and move on with your life :)

**NOTE**: Please be aware of which version of Django you are using.  In Django 1.5, it was added that you can use the ``True``, ``False``, and ``None`` literals as values, which is how the examples below are written.  If you are using Django 1.4 or earlier, you will find that passing a literal ``True`` yeilds a blank string as if a variable resolution failed.  Plan accordingly!

## Available tags

### Accordion
**Tag: ``{% bootstrap_accordion "id" active_panel=1 %}``**

* ``id`` (required): The DOM id for the accordion.
* ``active_panel``: A 1-based index denoting the default expanded panel.

**NOTE**: Content should generally not be placed immediately after opening the tag.  Instead, move on to create the first ``{% group %}`` section.

Sub-tags allowed to appear within ``bootstrap_accordion``:

* ``{% group "heading" %}``
    * ``heading`` (required): The markup that should appear inside of the clickable header's ``<a>`` tag.
    * Any content following a ``{% group %}`` tag will be inside of a content panel, until the next ``{% group %}`` is encountered or the whole tag ends.

Example:

```html
{% bootstrap_accordion id="my_accordion" %}
    {% group heading="First heading" %}
        First panel content
    {% group heading="Second heading" %}
        Second panel content
{% endbootstrap_accordion %}
```

### Nav-tabs
**Tag: ``{% bootstrap_navtabs active_tab=1 %}``**

* ``active_panel``: A 1-based index denoting the default active tab.

Sub-tags allowed to appear within ``bootstrap_navtabs``:

* ``{% tab "label" show=True active=None %}``
    * ``label`` (required): The markup that should appear inside of the tab's ``<a>`` tag.
    * ``show``: A boolean switch to decide if the tab and its content panel should even be rendered.
    * ``active``: If ``True``-ish, explicitly gives or withholds the "active" class on the associated tab and panel.  If you end up setting multiple tabs as active, that's on you, wanderer.

There's not really a proper way to allow you to omit the ``bootstrap_navtabs.active_tab`` setting in favor of using a ``tab.active`` flag.  If you wish to use ``tab.active``, please set the main ``bootstrap_navtabs.active_panel`` to 0, None, or some other non-True value.

Example:

```html
{% bootstrap_navtabs active_tab=3 %}
    {% tab label="First" %}
        First panel content
    {% tab label="Second" show=False %}
        Completely unrendered content, due to the "show" flag being False.
    {% tab label="Third" %}
        Third panel content
{% endbootstrap_navtabs %}
```
