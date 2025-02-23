from django.shortcuts import render
from .models import Ad
from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class AdListView(OwnerListView):
    model = Ad
    template = 'ads/ad_list.html'
    def get(self, request):
        ad_list = Ad.objects.all()
        ctx = {'ad_list': ad_list}
        return render(request, self.template, ctx)

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'

class AdCreateView(OwnerCreateView):
    model = Ad
    fields = ['title', 'text']
    template_name = 'ads/ad_form.html'
    def get(self, request):
        
        render(request, self.template_name)

class AdUpdateView(OwnerUpdateView):
    model = Ad
    fields = ['title', 'text']
    template_name = 'ads/ad_form.html'

class AdDeleteView(OwnerDeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'