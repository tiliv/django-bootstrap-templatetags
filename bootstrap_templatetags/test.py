from django.template import Context, Template
from django.test import SimpleTestCase


class BootstrapTemplateTagTest(SimpleTestCase):

    def test_rendered(self):

        context = Context({'title': 'my_title'})
        template_to_render = Template(
            '''
            {% load bootstrap_tags %}
            {% bootstrap_accordion id="my_accordion" style="primary" %}
                {% panel heading="First heading" %}
                    First panel content
                {% panel heading="Second heading" %}
                    Second panel content
            {% endbootstrap_accordion %}
            '''
        )
        rendered_template = template_to_render.render(context)
        self.assertIn('<div class="panel-group" id="my_accordion">', rendered_template)
        self.assertIn('<div class="panel panel-primary">', rendered_template)
        self.assertInHTML('<a href="#my_accordion-panel-1" data-toggle="collapse" '
                          'data-parent="#my_accordion" class="accordion-toggle">', rendered_template)