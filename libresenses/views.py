from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib import messages
from .models import Film, Caption, AudioDescription, SignLanguage, MediaAlternative
from .forms import (
    FilmForm, CaptionForm, AudioDescriptionForm, 
    SignLanguageForm, MediaAlternativeForm
)

class Index(View):
    def get(self, request):
        films = Film.objects.all()
        return render(request, 'index.html', {'films': films})

class FilmList(View):
    def get(self, request):
        films = Film.objects.all()
        return render(request, 'film_list.html', {'films': films})
    
class FilmProfile(View):
    def get(self, request, film_id):
        film = get_object_or_404(Film, pk=film_id)
        
        captions = film.captions.all()
        audio_descriptions = film.audio_descriptions.all()
        sign_languages = film.sign_languages.all()
        media_alternatives = film.media_alternatives.all()
        
        film_form = FilmForm(instance=film)
        caption_form = CaptionForm(initial={'film': film})
        audio_description_form = AudioDescriptionForm(initial={'film': film})
        sign_language_form = SignLanguageForm(initial={'film': film})
        media_alternative_form = MediaAlternativeForm(initial={'film': film})

        context = {
            'film': film,
            'film_form': film_form, 
            'captions': captions, 
            'audio_descriptions': audio_descriptions,
            'sign_languages': sign_languages,
            'media_alternatives': media_alternatives,
            'caption_form': caption_form,
            'audio_description_form': audio_description_form,
            'sign_language_form': sign_language_form,
            'media_alternative_form': media_alternative_form
        }

        return render(request, 'film_profile.html', context)

class SubmitFilm(View):
    def get(self, request):
        film_form = FilmForm()
        return render(request, 'submit_film.html', {'film_form': film_form})

    def post(self, request):
        film_form = FilmForm(request.POST, request.FILES)
        if film_form.is_valid():
            film = film_form.save()
            return redirect('film_profile', film_id=film.id)
        return render(request, 'submit_film.html', {'film_form': film_form})
    
class UpdateFilm(View):
    def get(self, request, film_id):
        film = get_object_or_404(Film, pk=film_id)
        film_form = FilmForm(instance=film)
        audio_description_form = AudioDescriptionForm()
        sign_language_form = SignLanguageForm()
        media_alternative_form = MediaAlternativeForm()

        context = {
            'film_form': film_form,
            'caption_form': caption_form,
            'audio_description_form': audio_description_form,
            'sign_language_form': sign_language_form,
            'media_alternative_form': media_alternative_form,
            'film': film,
        }
        return render(request, 'film_profile.html', context)
    

    def post(self, request, film_id):
        film = get_object_or_404(Film, pk=film_id)
        film_form = FilmForm(request.POST, request.FILES, instance=film)
        caption_form = CaptionForm() 
        audio_description_form = AudioDescriptionForm()
        sign_language_form = SignLanguageForm()
        media_alternative_form = MediaAlternativeForm()

        if film_form.is_valid():
            film_form.save()
            return redirect('film_profile', film_id=film.id)
        else:
            context = {
                'film_form': film_form,
                'caption_form': caption_form,
                'audio_description_form': audio_description_form,
                'sign_language_form': sign_language_form,
                'media_alternative_form': media_alternative_form,
                'film': film,
            }
            return render(request, 'film_profile.html', context)
        
class AddCaption(View):
    def post(self, request, film_id):
        film = get_object_or_404(Film, pk=film_id)
        form = CaptionForm(request.POST, request.FILES)
        if form.is_valid():
            caption = form.save(commit=False)
            caption.film = film
            caption.save()
            return redirect('film_profile', film_id=film_id)
        return redirect('film_profile', film_id=film_id)
    

class AddAudioDescription(View):
    def post(self, request, film_id):
        film = get_object_or_404(Film, pk=film_id)
        form = AudioDescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            audio_description = form.save(commit=False)
            audio_description.film = film
            audio_description.save()
            return redirect('film_profile', film_id=film_id)
        return redirect('film_profile', film_id=film_id)

class AddSignLanguage(View):
    def post(self, request, film_id):
        film = get_object_or_404(Film, pk=film_id)
        form = SignLanguageForm(request.POST, request.FILES)
        if form.is_valid():
            sign_language = form.save(commit=False)
            sign_language.film = film
            sign_language.save()
            return redirect('film_profile', film_id=film_id)
        return redirect('film_profile', film_id=film_id)
    
class AddMediaAlternative(View):
    def post(self, request, film_id):
        film = get_object_or_404(Film, pk=film_id)
        form = MediaAlternativeForm(request.POST, request.FILES)
        if form.is_valid():
            media_alternative = form.save(commit=False)
            media_alternative.film = film
            media_alternative.save()
            return redirect('film_profile', film_id=film_id)
        return redirect('film_profile', film_id=film_id)
    
class DeleteEntry(View):
    def post(self, request, model_name, entry_id):
        model = {
            'caption': Caption,
            'audio_description': AudioDescription,
            'sign_language': SignLanguage,
            'media_alternative': MediaAlternative,
            'film': Film,
        }.get(model_name.lower())

        if not model:
            messages.error(request, "Invalid model name for deletion.")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        entry = get_object_or_404(model, pk=entry_id)
        film_id = entry.film.id if hasattr(entry, 'film') else None
        entry.delete()

        messages.success(request, f'{model_name.replace("_", " ").capitalize()} deletado com sucesso.')
        if film_id:
            return redirect('film_profile', film_id=film_id)
        else:
            return redirect('index')
        