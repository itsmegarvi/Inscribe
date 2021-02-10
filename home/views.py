from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "home/index.html"


class DiscoverView(TemplateView):
    template_name = "home/discover.html"


class FAQView(TemplateView):
    template_name = "home/faq.html"
