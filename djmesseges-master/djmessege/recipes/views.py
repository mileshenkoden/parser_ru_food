from datetime import datetime
from urllib import request
from .forms import ArticlesForm, InstructionTextForm, InstructionImageForm
from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView
from django.core.files.storage import default_storage
from .models import Article, InstructionText, InstructionImage
from django.forms.models import inlineformset_factory
from django.contrib import messages



class NewDeleteView(DeleteView):


    model = Article
    template_name = 'recipes/delete.html'
    success_url = '/recipes'


class NewUpdateView(UpdateView):
    model = Article
    template_name = 'recipes/create.html'
    form_class = ArticlesForm


from .models import InstructionText, InstructionImage

class NewDetailView(DetailView):
    model = Article
    template_name = "recipes/details_view.html"
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        context['instructions_text'] = InstructionText.objects.filter(article=article)
        context['instructions_image'] = InstructionImage.objects.filter(article=article)
        return context


def recipes_home(request):
    recipes = Article.objects.all()  # Отримуємо всі статті з бази даних
    return render(request, 'recipes/recipes_home.html', {'recipes': recipes})




def create(request):
    if request.method == "POST":
        form = ArticlesForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.POST)  # Дивимося, чи приходять текстові інструкції
            print(request.FILES)  # Дивимося, чи передаються файли

            article = form.save()
            instructions_text = request.POST.getlist('instruction_text[]')  # Отримуємо список текстових інструкцій
            instructions_image = request.FILES.getlist('instruction_image[]')  # Отримуємо список файлів зображень

            print(f"Текст інструкцій: {instructions_text}")
            print(f"Зображення інструкцій: {[img.name for img in instructions_image]}")

            for index, text in enumerate(instructions_text, start=1):
                if text.strip():  # Переконуємося, що текст не порожній
                    InstructionText.objects.create(article=article, text=text, step_number=index)

            for index, image in enumerate(instructions_image, start=1):
                if image:  # Переконуємося, що файл зображення не порожній
                    InstructionImage.objects.create(article=article, image=image, step_number=index)

            messages.success(request, "Рецепт успішно збережено!")
            print(InstructionText.objects.filter(article=article))  # Дивимося, чи збережені тексти
            print(InstructionImage.objects.filter(article=article))  # Дивимося, чи збережені зображення

            return redirect('recipes_home')
        else:
            messages.error(request, "Будь ласка, перевірте форму на наявність помилок.")
    else:
        form = ArticlesForm()

    return render(request, 'recipes/create.html', {'form': form})
