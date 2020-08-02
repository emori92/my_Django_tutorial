from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.views import generic
from django.utils import timezone

import logging
from .models import Question, Choice


# logging
logger = logging.getLogger(__name__)


# views
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'question'

    def get_queryset(self):
        """最新の5件(未来は含まない)を取得"""
        return Question.objects.order_by('-pub_date')[:5]
        # return Question.objects.filter(pub_date__lte=timezone.now()) \
        #     .order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """publishされてないquerysetを返す"""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    # return HttpResponse("question: %s に投票しました。" % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # KeyError時は再度投票ページを表示
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "選択できていませんでした。",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 通常、POSTデータに問題がなければHttpResponseRedirectをreturnする
        # これは、ユーザーが戻るボタンを押した時に２回投票されることを防げます。
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


index = IndexView.as_view()
detail = DetailView.as_view()
results = ResultsView.as_view()


# function view
# def index(request):
#     # return HttpResponse("pollsのindexです。")
#     # object list
#     question = Question.objects.order_by('-pub_date')[:5]
#     # result = ', '.join([q.question_text for q in question])
#     # template = loader.get_template('polls/index.html')
#     context = {'question': question}
#     # return HttpResponse(template.render(context, request))
#     return render(request, 'polls/index.html', context)


# def detail(request, question_id):
#     # return HttpResponse("question: %s を閲覧しています。" % question_id)
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Questionのレコードはありません。")
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})


# def results(request, question_id):
#     # response = "question: %s の結果です。"
#     # return HttpResponse(response % question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
