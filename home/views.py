import sentiment_analysis
from django.http import JsonResponse
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "home/index.html"


class DiscoverView(TemplateView):
    template_name = "home/discover.html"


class FAQView(TemplateView):
    template_name = "home/faq.html"


class PlayGroundView(TemplateView):
    template_name = "home/playground.html"


def playground_response(request):
    print(request.GET)
    return JsonResponse({"hello": 12})


def playground_polarity_response(request):
    sentence = request.GET.get("input")
    polarity = sentiment_analysis.get_polarity(sentence)
    return JsonResponse({"polarity": polarity})
