from django.conf import settings
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Sum
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from line import models as db
import random
#import pytz,datetime

#請分別輸入自己的CHANNEL_ACCESS_TOKEN和CHANNEL_SECRET，可在此文中學習如何取得
line_bot_api = LineBotApi('JPlu3jyq5vdy8Jniic54utrIKDp0Yte/tRYxb/HrcSebvTZUIo4foDxbqoA3jq6c1Q63Q8b5vHfqQWAne+zQHN0KM6eFoEN5Bhe8Fkp23JRjJnaI8UrXRcLaVYGHvpBzBbzmb7iLed+vb7UqHlwKMwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('897223a1ae5697b6f0772ca3bc433a88')
text = ['白痴喔打錯了啦','你好怪，這個都會打錯','胖子連字都不會打喔','用點心啊胖子']
tp = ['支出','收入']
#tz = pytz.timezone('Asia/Taipei')
# Create your views here.
class LineReplyView(View):
    def get(self, request):
        return HttpResponse()

    def post(self,request:HttpRequest) -> HttpRequest:
        signature = request.META['HTTP_X_LINE_SIGNATURE']

            # get request body as text
        body = request.body.decode('utf-8')

            # handle webhook body
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseBadRequest()

        return HttpResponse()


    @handler.add(MessageEvent, message=TextMessage)
    def message_text(event: MessageEvent):
        user_id = db.LineUser.objects.values('id').filter(userId = event.source.user_id)
        if len(user_id) == 0:
            insert_user_id = db.LineUser(userId = event.source.user_id)
            insert_user_id.save()
            message = "Welcome"
        else:
            if event.message.text == '查詢':
                
                income = db.LineRecord.objects.filter(userId = user_id[0]['id'],recordType = 1).aggregate(Sum("recordCount"))
                outlay = db.LineRecord.objects.filter(userId = user_id[0]['id'],recordType = 0).aggregate(Sum("recordCount"))
                message = f"這個月的收入為 {income['recordCount__sum']} , 支出為 {outlay['recordCount__sum']} , 剩餘 {income['recordCount__sum']-outlay['recordCount__sum']}"
            else:
                try:
                    if '收入' in event.message.text:
                        temp = event.message.text.replace('收入','',1).split()
                        recordCount = temp[0]
                        recordContent = temp[1]
                        recordType = 1
                    else:
                        temp = event.message.text.split()
                        recordCount = temp[1]
                        recordContent = temp[0]
                        recordType = 0

                    message = f'紀錄成功，{tp[recordType]}：{recordCount}，項目為{recordContent}'
                    insert_content = db.LineRecord(userId = user_id[0]['id'], recordType = recordType, recordContent = recordContent, recordCount = recordCount)
                    insert_content.save()
                except:
                    message = random.choice(text)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=message)
        )
    """
    {"message": {"id": "11808555483075", "text": "\u55e8", "type": "text"},
     "mode": "active",
     "replyToken": "7fd86057f71b4fc39994c80b45145436", 
     "source": {"type": "user", "userId": "U217edfc99fef29581aac21d6e6577f6b"},
      "timestamp": 1587198184250,
       "type": "message"}
    """