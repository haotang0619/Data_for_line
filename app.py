from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import random
import os

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('iQYo262WUqoCx3fP+1OTHVCl7EpUgTv4eG8oQZVbupv1Vz9k08ytnW4+7orj1/VftxQkM3TfrXNC5YHTKv1jLhIpfxU8Odot7G/KEd73YhmCbBz57jFe5Xo5xTxq67N7hJpl0VT/cJFnqHhXsJPoWAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('dac067c748c3e48b504f313170ef42c1')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    received = event.message.text
    if '客製化\n' == received[0:4] :
        with open('./old/tmp.txt','w') as tmp :
            tmp.write(received[4:])
        os.system("python3 ./old/make_old.py")
        with open('./old/link.txt') as lin :
            image_url = lin.read()
        message = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
        line_bot_api.reply_message(event.reply_token, message)
    
    elif '查姓名 ' == received[0:4] :
        name = received[4:]
        bubble = BubbleContainer(
            direction='ltr',
            body = BoxComponent(
                layout = 'vertical',
                contents=[
                    TextComponent(text='防治洗錢資料庫來源: 新聞',color='#00bfff',size='md'),
                    TextComponent(text=name,color='#000000',size='xxl'),
                    TextComponent(text='查獲3筆資料 危險程度: 60%',color='#ff0000',size='sm'),
                    SeparatorComponent(margin='xl'),
                    TextComponent(text='犯罪類別: 洗錢',color='#00bfff',size='md'), 
                    TextComponent(text='犯罪描述',color='#00bfff',size='md'),
                    TextComponent(text='1.經XX機關查獲，'+name+'有洗錢嫌疑，...',color='#000000',size='md'),
                    TextComponent(text='2.'+name+'於今日被查獲有洗錢嫌疑，XX...',color='#000000',size='md'),
                    SeparatorComponent(margin='xl'),
                    TextComponent(text='犯罪類別: 賄賂',color='#00bfff',size='md'),
                    TextComponent(text='犯罪描述',color='#00bfff',size='md'),
                    TextComponent(text='1.'+name+'在今年向XX議員涉有行賄嫌疑，經...',color='#000000',size='md'),
                    SeparatorComponent(margin='xl'),
                    ButtonComponent(
                        style='link',
                        action = URIAction(label='用google搜尋',uri='https://www.google.com/search?q=' + name)
                    )
                ]
            )
        )
        message = FlexSendMessage(alt_text="姓名搜尋結果", contents=bubble);
        line_bot_api.reply_message(event.reply_token, message)
    
    elif 'Search by name' == received :
        message = TextSendMessage(text='請按照以下格式輸入以搜尋：\n------------------------------------------------\n查姓名 你想查詢的姓名\n------------------------------------------------\n(注意：「查姓名」的後面只能放一個空格喔)\n\n範例圖片如下：') 
        image_url = 'https://i.imgur.com/hfXVCCW.png'
        example = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
        line_bot_api.reply_message(event.reply_token, [message, example])
    
    elif '查罪名 ' == received[0:4] :
        crime = received[4:]
        bubble = BubbleContainer(
            direction='ltr',
            body = BoxComponent(
                layout = 'vertical',
                contents=[
                    TextComponent(text='防治洗錢資料庫來源: 判決',color='#00bfff',size='md'),
                    TextComponent(text=crime,color='#000000',size='xxl'),
                    TextComponent(text='顯示前5筆姓名',color='#ff0000',size='sm'),
                    SeparatorComponent(margin='xl'),
                    ButtonComponent(
                        style='link',
                        action = MessageAction(label='陳XX',text='查姓名 陳XX')
                    ),
                    ButtonComponent(
                        style='link',
                        action = MessageAction(label='林XX',text='查姓名 林XX')
                    ),
                    ButtonComponent(
                        style='link',
                        action = MessageAction(label='許XX',text='查姓名 許XX')
                    ),
                    ButtonComponent(
                        style='link',
                        action = MessageAction(label='黃XX',text='查姓名 黃XX')
                    ),
                    ButtonComponent(
                        style='link',
                        action = MessageAction(label='吳XX',text='查姓名 吳XX')
                    ),
                    SeparatorComponent(margin='xl'),
                    ButtonComponent(
                        style='link',
                        action = URIAction(label='用google搜尋',uri='https://www.google.com/search?q=' + crime)
                    )
                ]
            )
        )
        message = FlexSendMessage(alt_text="罪名搜尋結果", contents=bubble);
        line_bot_api.reply_message(event.reply_token, message)
    
    elif 'Search by crime' == received :
        message = TextSendMessage(text='請按照以下格式輸入以搜尋：\n------------------------------------------------\n查罪名 你想查詢的罪名\n------------------------------------------------\n(注意：「查罪名」的後面只能放一個空格喔)\n\n範例圖片如下：') 
        image_url = 'https://i.imgur.com/vDAxPyb.png'
        example = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
        line_bot_api.reply_message(event.reply_token, [message, example])
    
    elif '我要客製化' == received :
        message = TextSendMessage(text='(輸入「我要客製化」即可看到本訊息，目前只支援長輩圖背景喔)\n\n請按照以下格式輸入以自行製圖：\n------------------------------------------------\n客製化\n你想放入圖片的文字\n------------------------------------------------\n(注意：「客製化」的後面不能有任何空格，要直接換行喔)\n\n範例圖片如下：') 
        image_url = 'https://i.imgur.com/uGkQtFz.png'
        example = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
        line_bot_api.reply_message(event.reply_token, [message, example])
    
    elif '派大星' in received :
        Carousel_template = TemplateSendMessage(
        alt_text='派大星目錄',
        template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url='https://i.ytimg.com/vi/zjFssJpLFs4/maxresdefault.jpg',
                title='派大星逗你',
                text='生活很無聊嗎，派大星來逗你玩~',
                actions=[
                    MessageTemplateAction(
                        label='派大星讚美你',
                        text='讚美我'
                    ),
                    MessageTemplateAction(
                        label='派大星語錄',
                        text='來句名言'
                    ),
                    MessageTemplateAction(
                        label='負能量派大星',
                        text='來點負能量'
                    )
                ]
            ),
            CarouselColumn(
                thumbnail_image_url='https://pbs.twimg.com/media/DCxyCxKUIAAuZY2.jpg',
                title='圖像派大星',
                text='讓派大星為你提供各種圖片吧~',
                actions=[
                    MessageTemplateAction(
                        label='梗圖派大星',
                        text='來張梗圖'
                    ),
                    MessageTemplateAction(
                        label='早安派大星',
                        text='來張早安圖'
                    ),
                    MessageTemplateAction(
                        label='我要客製化',
                        text='我要客製化'
                    )
                ]
            )
        ]
        )
        )
        line_bot_api.reply_message(event.reply_token,Carousel_template)
    
    elif '讚美' in received or '稱讚' in received :
        with open('./good.txt') as goo :
            tot = goo.read().split('\n')
            which = random.randint(0,len(tot) - 2)
            message = TextSendMessage(text=tot[which])
            line_bot_api.reply_message(event.reply_token, message)
    
    elif '名言' in received or '語錄' in received :
        with open('./famous.txt') as fam :
            tot = fam.read().split('\n')
            which = random.randint(0,len(tot) - 2)
            message = TextSendMessage(text=tot[which])
            line_bot_api.reply_message(event.reply_token, message)
    
    elif '負能量' in received :
        with open('./bad.txt') as bad :
            tot = bad.read().split('\n')
            which = random.randint(0,len(tot) - 2)
            message = TextSendMessage(text=tot[which])
            line_bot_api.reply_message(event.reply_token, message)
    
    elif '梗圖' in received :
        with open('./laugh.txt') as lau :
            tot = lau.read().split('\n')
            which = random.randint(0,len(tot) - 2)
            image_url = 'https://raw.githubusercontent.com/howard919901/Data_for_line/master/laugh/' + tot[which]
            message = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
            line_bot_api.reply_message(event.reply_token, message)
    
    elif '早安' in received :
        with open('./morning.txt') as mor :
            tot = mor.read().split('\n')
            which = random.randint(0,len(tot) - 2)
            image_url = 'https://raw.githubusercontent.com/howard919901/Data_for_line/master/morning/' + tot[which]
            message = ImageSendMessage(original_content_url=image_url, preview_image_url=image_url)
            line_bot_api.reply_message(event.reply_token, message)
    
    else :
        message = TextSendMessage(text='I\'m Patrick !')
        patrick = TextSendMessage(text='輸入「派大星」獲得更多資訊......')
        # line_bot_api.reply_message(event.reply_token, [message, patrick])

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
