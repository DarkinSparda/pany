from django.shortcuts import render, redirect
from .models import Ad, Comment
from .owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from .forms import CreateForm, CommentForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect


class AdListView(OwnerListView):
    model = Ad
    template = 'ads/ad_list.html'
    

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        comment_form = CommentForm()
        context = {'ad': ad,
                   'comments': comments,
                   'comment_form': comment_form}
        return render(request, self.template_name, context)

class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)
    
    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        return redirect(self.success_url)


class AdUpdateView(OwnerUpdateView):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)
    

    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)
        
        if not form.is_valid():
            ctx = {'form': form,
                   'msg': 'form is invalid, please try again'}
            return render(request, self.template_name, ctx)
        
        ad = form.save(commit=False)
        ad.save()
        return redirect(self.success_url)

class AdDeleteView(OwnerDeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['text'], owner=request.user, ad=ad)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))

class CommentDeleteView(LoginRequiredMixin, View):
    template_name = 'ads/comment_delete.html'
    def get(self, request, pk):
        comment = get_object_or_404(Comment, id=pk)
        context = {
            'comment': comment
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        comment = get_object_or_404(Comment, id=pk, owner=request.user)
        comment.delete()
        return redirect(reverse('ads:ad_detail', args=[comment.ad.id]))


def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response