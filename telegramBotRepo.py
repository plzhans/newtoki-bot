from typing import Any, Dict
import telegram
import telegram.ext
import telegram.update
import telegram.message

class TelegramBotRepo:

    __bot:telegram.Bot
    __updater:telegram.ext.Updater

    __captchaDict:Dict[str, Any]

    #
    def __init__(self, token):
        self.__bot = telegram.Bot(token=token)
        self.__updater = telegram.ext.Updater(token=token, use_context=True)

        self.__captchaDict = dict()

    #
    def __telegram_update_handler(self, update:telegram.update.Update, context):

        user_message:telegram.message.Message = update.message
        if user_message.reply_to_message != None:
            reply_message = user_message.reply_to_message
            if reply_message.caption.startswith("Captcha token : "):
                captcha_t = reply_message.caption[16:reply_message.caption.rindex('\n')]
                self.__captchaDict[captcha_t] = user_message.text
        pass

    # 
    def getCaptchaValue(self, captcha_t:str):
        if captcha_t in self.__captchaDict:
            captcha_value = self.__captchaDict[captcha_t]
            return captcha_value
        return None

    #
    def popCaptchaValue(self, captcha_t:str):
        if captcha_t in self.__captchaDict:
            captcha_value = self.__captchaDict.pop(captcha_t)
            return captcha_value
        return None

    # 메세지 받기
    def beginReceive(self):
        
        dispatcher = self.__updater.dispatcher
        self.__updater.start_polling()

        echo_handler = telegram.ext.MessageHandler(telegram.ext.Filters.text, self.__telegram_update_handler)
        dispatcher.add_handler(echo_handler)

        return True
    
    # 텍스트 보내기
    def sendText(self, chat_id, text):

        self.__bot.send_message(chat_id=chat_id, text=text)
        return False

    # 이미지 보내기
    def sendPhoto(self, chat_id, photo, caption):

        self.__bot.send_photo(chat_id=chat_id, photo=photo, caption=caption)
        return False