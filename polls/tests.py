from django.test import TestCase
from django.utils import timezone
import datetime
from django.urls import reverse

from .models import Question


# questionを作成する関数
def create_question(text, days):
    """
    textとdaysを引数に問題を作成する。
    過去の日付は避け、publishされてないものを採用する
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=text, pub_date=time)


# Question Model
class QuestionModelTests(TestCase):

    # 正常値
    def test_was_published_recently_with_recent_question(self):
        """pub_dateが1日以内の場合True"""

        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    # 異常値
    def test_was_published_recently_with_old_question(self):
        """pub_dateが1日以上経過している場合False"""

        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_future_question(self):
        """pub_dateが未来の日付ならFalse"""

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)



# index
class QuestionIndexViewTests(TestCase):
    
    def test_no_questions(self):
        """
        - indexへアクセス
        - http: 200
        - レスポンスの文章が含まれてるか確認
        - querysetが空か
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "投票はありません。")
        self.assertQuerysetEqual(response.context['question'], [])

    def test_past_question(self):
        """
        - 30日前のQuestionを作成
        - indexへアクセス
        - querysetが'過去の問題'のQuestionと等しいかチェック
        """
        create_question(text="過去の問題", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['question'], ['<Question: 過去の問題>']
        )

    def test_future_question(self):
        """
        - 30日後のQuestionを作成
        - indexへアクアセス
        - レスポンスに文章が含まれているか確認
        - querysetが[]と等しいかチェック
        """
        create_question(text="未来の問題", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "投票はありません。")
        self.assertQuerysetEqual(response.context['question'], [])

    def test_future_question_and_past_question(self):
        """
        - 過去と未来のQuestionを作成
        - indexへアクアセス
        - querysetが'過去の問題'のQuestionと等しいかチェック
        """
        create_question(text="過去の問題", days=-30)
        create_question(text="未来の問題", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['question'], ['<Question: 過去の問題>']
        )

    def test_two_past_questions(self):
        """
        - 30日前と5日前のQuestionを作成
        - indexへアクアセス
        - querysetが[30日前, 5日前]と等しいかチェック
        """
        create_question(text="30日前の問題", days=-30)
        create_question(text="5日前の問題", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['question'],
            ['<Question: 5日前の問題>', '<Question: 30日前の問題>']
        )


# detail
class QuestionDetailViewTests(TestCase):
    
    def test_future_question(self):
        """
        - 5日後のQuestionを作成
        - Questionオブジェクトのurlを取得
        - 上記urlでGET requestしresponseを取得
        - httpステータスが404か確認
        """
        future_question = create_question(question_text='5日後の問題', days=5)
        url = reverse('polls:detail', args=(future_question.id))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        - 5日前のQuestionを作成
        - Questionオブジェクトのurlを取得
        - 上記urlでGET requestしresponseを取得
        - responseにQuestionのタイトルが含まれてるか確認
        """
        past_question = create_question(question_text='5日前の問題', days=-5)
        url = reverse('polls:detail', args=(past_question.id))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
