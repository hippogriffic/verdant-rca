from django.db import models
from core.models import Page as PageBase, Orderable
from core.fields import RichTextField
from cluster.fields import ParentalKey

from verdantadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel
from verdantimages.edit_handlers import ImageChooserPanel
from verdantimages.models import AbstractImage, AbstractRendition
from verdantdocs.edit_handlers import DocumentChooserPanel
from verdantsnippets.edit_handlers import SnippetChooserPanel


EVENT_AUDIENCE_CHOICES = (
    ('public', "Public"),
    ('private', "Private"),
)


# Some abstract classes that define common fields
class Page(PageBase):
    seo_title = models.CharField("Page title", max_length=255, blank=True, help_text="Optional. 'Search Engine Friendly' title. This will appear at the top of the browser window.")
    show_in_menus = models.BooleanField(default=False, help_text="Whether a link to this page will appear in automatically generated menus")
    meta_description = models.TextField(blank=True)

    is_abstract = True

    promote_panels = [
        FieldPanel('slug'),
        FieldPanel('seo_title'),
        FieldPanel('show_in_menus'),
        FieldPanel('meta_description'),
    ]

    indexed_fields = ('seo_title', 'meta_description')
    search_name = "Page"

    class Meta:
        abstract = True


class LinkFields(models.Model):
    link_external = models.URLField("External link", blank=True)
    link_page = models.ForeignKey('core.Page', null=True, blank=True, related_name='+')
    link_document = models.ForeignKey('verdantdocs.Document', null=True, blank=True, related_name='+')

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        elif self.link_document:
            return self.link_document.url
        else:
            return self.link_external

    panels = [
        FieldPanel('link_external'),
        PageChooserPanel('link_page'),
        DocumentChooserPanel('link_document'),
    ]

    class Meta:
        abstract = True


class CarouselItemFields(LinkFields):
    image = models.ForeignKey('verdantimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    embed_url = models.URLField("Embed URL", blank=True)
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('embed_url'),
        FieldPanel('caption'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


class RelatedLinkFields(LinkFields):
    title = models.CharField(max_length=255, help_text="Link title")

    panels = [
        FieldPanel('title'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

    class Meta:
        abstract = True


class ContactFields(models.Model):
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address_1 = models.CharField(max_length=255, blank=True)
    address_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    post_code = models.CharField(max_length=10, blank=True)

    panels = [
        FieldPanel('telephone'),
        FieldPanel('email'),
        FieldPanel('address_1'),
        FieldPanel('address_2'),
        FieldPanel('city'),
        FieldPanel('country'),
        FieldPanel('post_code'),
    ]

    class Meta:
        abstract = True


# Home Page

class HomePageCarouselItem(Orderable, CarouselItemFields):
    page = ParentalKey('demo.HomePage', related_name='carousel_items')

class HomePageRelatedLink(Orderable, RelatedLinkFields):
    page = ParentalKey('demo.HomePage', related_name='related_links')

class HomePage(Page):
    body = RichTextField(blank=True)

    indexed_fields = ('body', )
    search_name = "Homepage"

    class Meta:
        verbose_name = "Homepage"

HomePage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
    InlinePanel(HomePage, 'carousel_items', label="Carousel items"),
    InlinePanel(HomePage, 'related_links', label="Related links"),
]

HomePage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
]


# Standard index page

class StandardIndexPage(Page):
    # No additional fields required

    search_name = None

StandardIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
]

StandardIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
]


# Standard page

class StandardPageCarouselItem(Orderable, CarouselItemFields):
    page = ParentalKey('demo.StandardPage', related_name='carousel_items')

class StandardPageRelatedLink(Orderable, RelatedLinkFields):
    page = ParentalKey('demo.StandardPage', related_name='related_links')

class StandardPage(Page):
    intro = RichTextField(blank=True)
    body = RichTextField(blank=True)

    indexed_fields = ('intro', 'body', )
    search_name = None

StandardPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    FieldPanel('body', classname="full"),
    InlinePanel(StandardPage, 'carousel_items', label="Carousel items"),
    InlinePanel(StandardPage, 'related_links', label="Related links"),
]

StandardPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
]


# Blog index page

class BlogIndexPageRelatedLink(Orderable, RelatedLinkFields):
    page = ParentalKey('demo.BlogIndexPage', related_name='related_links')

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    indexed_fields = ('intro', )
    search_name = "Blog"

    @property
    def blogs(self):
        # Get list of blog pages that are descentands of this page
        return BlogPage.objects.filter(live=True, path__startswith=self.path)

BlogIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel(BlogIndexPage, 'related_links', label="Related links"),
]

BlogIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
]


# Blog page

class BlogPageCarouselItem(Orderable, CarouselItemFields):
    page = ParentalKey('demo.BlogPage', related_name='carousel_items')

class BlogPageRelatedLink(Orderable, RelatedLinkFields):
    page = ParentalKey('demo.BlogPage', related_name='related_links')

class BlogPage(Page):
    body = RichTextField()

    indexed_fields = ('body', )
    search_name = "Blog Entry"

BlogPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
    InlinePanel(BlogPage, 'carousel_items', label="Carousel items"),
    InlinePanel(BlogPage, 'related_links', label="Related links"),
]

BlogPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
]


# Person page

class PersonPageRelatedLink(Orderable, RelatedLinkFields):
    page = ParentalKey('demo.PersonPage', related_name='related_links')

class PersonPage(Page, ContactFields):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    intro = RichTextField(blank=True)
    biography = RichTextField(blank=True)
    image = models.ForeignKey('verdantimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    indexed_fields = ('first_name', 'last_name', 'intro', 'biography')
    search_name = "Person"

PersonPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('first_name'),
    FieldPanel('last_name'),
    FieldPanel('intro', classname="full"),
    FieldPanel('biography', classname="full"),
    ImageChooserPanel('image'),
    MultiFieldPanel(ContactFields.panels, "Contact"),
    InlinePanel(PersonPage, 'related_links', label="Related links"),
]

PersonPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
]


# Contact page

class ContactPage(Page, ContactFields):
    body = RichTextField(blank=True)

    indexed_fields = ('body', )
    search_name = "Contact information"

ContactPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('body', classname="full"),
    MultiFieldPanel(ContactFields.panels, "Contact"),
]

ContactPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
]


# Event index page

class EventIndexPageRelatedLink(Orderable, RelatedLinkFields):
    page = ParentalKey('demo.EventIndexPage', related_name='related_links')

class EventIndexPage(Page):
    intro = RichTextField(blank=True)

    indexed_fields = ('intro', )
    search_name = "Event index"

    @property
    def events(self):
        # Get list of event pages that are descentands of this page
        return EventPage.objects.filter(live=True, path__startswith=self.path)

EventIndexPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('intro', classname="full"),
    InlinePanel(EventIndexPage, 'related_links', label="Related links"),
]

EventIndexPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
]


# Event page

class EventPageCarouselItem(Orderable, CarouselItemFields):
    page = ParentalKey('demo.EventPage', related_name='carousel_items')

class EventPageRelatedLink(Orderable, RelatedLinkFields):
    page = ParentalKey('demo.EventPage', related_name='related_links')

class EventPageDatesAndTimes(Orderable):
    page = ParentalKey('demo.EventPage', related_name='dates_and_times')
    date_from = models.DateField("Start date")
    date_to = models.DateField("End date", null=True, blank=True, help_text="Not required if event is on a single day")
    time_from = models.TimeField("Start time", null=True, blank=True)
    time_to = models.TimeField("End time", null=True, blank=True)
    time_other = models.CharField("Time other", max_length=255, blank=True, help_text="Use this field to give additional information about start and end times")

    panels = [
        FieldPanel('date_from'),
        FieldPanel('date_to'),
        FieldPanel('time_from'),
        FieldPanel('time_to'),
        FieldPanel('time_other'),
    ]

class EventPageSpeaker(Orderable, LinkFields):
    page = ParentalKey('demo.EventPage', related_name='speakers')
    first_name = models.CharField("Name", max_length=255, blank=True)
    last_name = models.CharField("Surname", max_length=255, blank=True)
    image = models.ForeignKey('verdantimages.Image', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    @property
    def name_display(self):
        return self.first_name + " " + self.last_name

    panels = [
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        ImageChooserPanel('image'),
        MultiFieldPanel(LinkFields.panels, "Link"),
    ]

class EventPage(Page):
    audience = models.CharField(max_length=255, choices=EVENT_AUDIENCE_CHOICES)
    location = models.CharField(max_length=255)
    body = RichTextField(blank=True)
    specific_directions = models.TextField(blank=True)
    specific_directions_link = models.URLField(blank=True)
    cost = RichTextField(blank=True)
    signup_link = models.URLField(blank=True)

    indexed_fields = ('get_audience_display', 'location', 'body')
    search_name = "Event"

EventPage.content_panels = [
    FieldPanel('title', classname="full title"),
    FieldPanel('audience'),
    FieldPanel('location'),
    FieldPanel('body', classname="full"),
    InlinePanel(EventPage, 'speakers', label="Speakers"),
    InlinePanel(EventPage, 'dates_and_times', label="Dates and times"),
    MultiFieldPanel([
        FieldPanel('specific_directions'),
        FieldPanel('specific_directions_link'),
    ], 'Specific directions'),
    FieldPanel('cost'),
    FieldPanel('signup_link'),
    InlinePanel(EventPage, 'carousel_items', label="Carousel items"),
    InlinePanel(EventPage, 'related_links', label="Related links"),
]

EventPage.promote_panels = [
    MultiFieldPanel(Page.promote_panels, "Common page configuration"),
]