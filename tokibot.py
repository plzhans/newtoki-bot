from asyncio import sleep
from datetime import datetime, timedelta
from enum import Enum
from browserDriver import BrowserDriver
from telegramBotRepo import TelegramBotRepo

#
class BOT_STEP(Enum):
    INIT = 1
    LOGINING = 2
    LOGINED = 3
    READY = 4
    AUTO_MINE = 5
    AUTO_MONSTER = 6

#
class TokiBot:
    
    #
    __telegramBotRepo:TelegramBotRepo
    
    # 브라우저 드라이버
    __m_browser:BrowserDriver = None

    # 봇 단계
    __m_botStep = BOT_STEP.INIT

    # 다음 포인트 광산 시간
    __m_nextMineTime = None

    # 다음 몬스터 레이드 시간
    __m_nextMonsterTime = None

    # 생성자 초기화
    def __init__(self):
        self.__telegramBotRepo = TelegramBotRepo("5111877415:AAHPELfQGf8mb9vQLVGngNS5m9VZOR5t72w")
        self.__m_browser = BrowserDriver(self.__telegramBotRepo)

    # 업데이트
    def update(self):
        if self.__m_botStep == BOT_STEP.INIT:
            self.__m_botStep = self.__update_init()
        elif self.__m_botStep == BOT_STEP.LOGINING:
            self.__m_botStep = self.__update_logining()
        elif self.__m_botStep == BOT_STEP.LOGINED:
            self.__m_botStep = self.__update_logined()
        elif self.__m_botStep == BOT_STEP.READY:
            if self.__update_auto_mine() == True:
                return
            elif self.__update_auto_monster() == True:
                return

    # 초기화
    def __update_init(self):

        self.__telegramBotRepo.beginReceive()

        # next step
        return BOT_STEP.LOGINING

    # 로그인 시도
    def __update_logining(self):
        #
        self.__m_browser.actionLogin()

        # next step
        return BOT_STEP.LOGINED

    # 로그인 완료
    def __update_logined(self):

        # next step
        return BOT_STEP.READY

    # 포인트 광산
    def __update_auto_mine(self):
        #return False
        # 시간 체크
        if self.__m_nextMineTime != None:
            now = datetime.now()
            if now < self.__m_nextMineTime:
                return False

        #
        if self.__m_browser.actionMine() == True:
            # 성공하면 다은 시간(21초)에 한번씩 시도
            now = datetime.now()
            self.__m_nextMineTime = now + timedelta(seconds=21)
            return True
        
        return False

    # 몬스터 레이드
    def __update_auto_monster(self):
        return False
        # 시간 체크
        if self.__m_nextMonsterTime != None:
            now = datetime.now()
            if now < self.__m_nextMonsterTime:
                return False

        #
        if self.__m_browser.actionMonster() == True:
            # 성공하면 다은 시간(30초)에 한번씩 시도
            now = datetime.now()
            self.__m_nextMonsterTime = now + timedelta(seconds=30)
            return True
        
        return False