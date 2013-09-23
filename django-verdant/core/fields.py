from django.db import models
from django.forms import Textarea
from south.modelsinspector import add_introspection_rules

from core.rich_text import DbWhitelister, expand_db_html

class RichTextArea(Textarea):
    def get_panel(self):
        from verdantadmin.edit_handlers import RichTextFieldPanel
        return RichTextFieldPanel

    def render(self, name, value, attrs=None):
        translated_value = expand_db_html(value, for_editor=True)
        return super(RichTextArea, self).render(name, translated_value, attrs)

    def value_from_datadict(self, data, files, name):
        original_value = super(RichTextArea, self).value_from_datadict(data, files, name)
        return DbWhitelister.clean(original_value)


class RichTextField(models.TextField):
    def formfield(self, **kwargs):
        defaults = {'widget': RichTextArea}
        defaults.update(kwargs)
        return super(RichTextField, self).formfield(**defaults)

add_introspection_rules([], ["^core\.fields\.RichTextField"])
