from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from cats.models import Cat, Breed
from cats.forms import CatForm, BreedForm
# Create your views here.

class CatList(LoginRequiredMixin, View):
    template = 'cats/cats_list.html'
    def get(self, request):
        bc = Breed.objects.count()
        cl = Cat.objects.all()

        context = { 'breed_count' : bc,
                    'cat_list' : cl
                    }

        return render(request, self.template, context)

class BreedList(LoginRequiredMixin, View):
    template = 'cats/breed_list.html'
    def get(self, request):
        bl = Breed.objects.all()
        context = {'breed_list': bl }
        return render(request, self.template, context)

class CatUpdate(LoginRequiredMixin, View):
    template = 'cats/cat_form.html'
    success_url = reverse_lazy('cats:all')
    def get(self, request, pk):
        cat = get_object_or_404(Cat, pk=pk)
        form = CatForm(instance=cat)
        context = {
            'form' : form
            }
        return render(request, self.template, context)

    def post(self, request, pk):
        cat = get_object_or_404(Cat, pk=pk)
        form = CatForm(request.POST, instance=cat)
        ctx = {'form' : form }
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template, ctx)

class CatDelete(LoginRequiredMixin, View):
    template = 'cats/cat_delete.html'
    success_url = reverse_lazy('cats:all')
    def get(self, request, pk):
        cat = get_object_or_404(Cat, pk=pk)
        context = {'cat' : cat }
        return render(request, self.template, context)

    def post(self, request, pk):
        cat = get_object_or_404(Cat, pk=pk)
        cat.delete()
        return redirect(self.success_url)

class CatCreate(LoginRequiredMixin, View):
    template = 'cats/cat_form.html'
    success_url = reverse_lazy('cats:all')
    def get(self, request):
        form = CatForm()
        context = { 'form' : form }
        return render(request, self.template, context)
    def post(self, request):
        form = CatForm(request.POST)
        context = { 'form' : form }
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template, context)

class BreedCreate(LoginRequiredMixin, View):
    template = 'cats/breed_form.html'
    success_url = reverse_lazy('cats:all')
    def get(self, request):
        form = BreedForm()
        context = { 'form' : form }
        return render(request, self.template, context)
    def post(self, request):
        form = BreedForm(request.POST)
        context = { 'form' : form }
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template, context)

class BreedUpdate(LoginRequiredMixin, View):
    template = 'cats/breed_form.html'
    success_url = reverse_lazy('cats:all')
    def get(self, request, pk):
        breed = get_object_or_404(Breed, pk=pk)
        form = BreedForm(instance=breed)
        context = {
            'form' : form
            }
        return render(request, self.template, context)

    def post(self, request, pk):
        breed = get_object_or_404(Breed, pk=pk)
        form = BreedForm(request.POST, instance=breed)
        ctx = {'form' : form }
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template, ctx)

class BreedDelete(LoginRequiredMixin, View):
    template = 'cats/breed_delete.html'
    success_url = reverse_lazy('cats:all')
    def get(self, request, pk):
        breed = get_object_or_404(Breed, pk=pk)
        context = {'breed' : breed }
        return render(request, self.template, context)

    def post(self, request, pk):
        breed = get_object_or_404(Breed, pk=pk)
        breed.delete()
        return redirect(self.success_url)
