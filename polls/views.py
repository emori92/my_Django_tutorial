from django.shortcuts import render
from django.http import HttpResponse
import logging

# logging
logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    return HttpResponse("pollsのindexです。")


def detail(request, question_id):
    return HttpResponse("question: %s を閲覧しています。" % question_id)


def results(request, question_id):
    response = "question: %s の結果です。"
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("question: %s に投票しました。" % question_id)
