from datetime import datetime
from time import sleep
from tokibot import TokiBot

# 봇 생성
bot = TokiBot()

# 반복
while True:
    bot.update()
    sleep(1)
