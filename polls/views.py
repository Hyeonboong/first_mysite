from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.urls import reverse_lazy
from .models import Question

from .models import Choice, Question

class QuestionupdateView(generic.edit.UpdateView):
    model = Question
    fields = ['question_text']
    template_name = 'polls/question_update_form.html'
    success_url = reverse_lazy('polls:index')

class ChoiceCreateView(generic.edit.CreateView):
    model = Choice
    fields = ['choice_text']
    template_name = 'polls/choice_form.html'
    def form_valid(self, form):
        form.instance.question = get_object_or_404(Question, pk=self.kwargs['pk'])
        return super().form_valid(form)

    success_url = reverse_lazy('polls:index')
    
#IndexView
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:3]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_object(self):
        question_id = self.kwargs['pk']
        question = get_object_or_404(Question, pk=question_id)
        return question

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

class QuestionCreateView(generic.edit.CreateView):
    model = Question
    fields = ['question_text']
    template_name='polls/question_form.html'
    success_url = reverse_lazy('polls:index')

class ChoiceUpdateView(generic.edit.UpdateView):
    model = Choice
    fields = ['choice_text']
    template_name = 'polls/choice_update_form.html'  # 새로운 템플릿 또는 기존 템플릿 지정

    def get_success_url(self):
        # 선택지가 업데이트된 후, 선택지가 속한 질문의 상세 페이지로 리다이렉션
        choice = self.object
        return reverse('polls:detail', kwargs={'pk': choice.question.pk})
    
class QuestionDeleteView(generic.edit.DeleteView):
    model = Question
    template_name = 'polls/question_confirm_delete.html'
    success_url = reverse_lazy('polls:index')  # 삭제 후 리다이렉션될 URL, 실제 프로젝트에 맞게 수정 필요

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})
    

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    
