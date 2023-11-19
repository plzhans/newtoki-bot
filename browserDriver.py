import random
import string
from time import sleep
from typing import Any, Dict
from selenium import webdriver
import urllib.parse

from telegramBotRepo import TelegramBotRepo

#
class BrowserDriver:

    __driver:webdriver.Remote
    __telegramBotRepo:TelegramBotRepo
    __newtokiUrl:string

    def __init__(self, telegramBotRepo:TelegramBotRepo):
        self.__driver = webdriver.Chrome('./tool/chromedriver-100.0.4896.60/chromedriver_win32/chromedriver.exe')
        self.__telegramBotRepo = telegramBotRepo
        self.__telegramChatID = 58087716

    # 메세지 받기
    def beginReceive(self):
        self.__telegramBotRepo.beginReceive()
        return True

    # 로그인
    def actionLogin(self):
        print("actionLogin start.")
        self.__newtokiUrl = "https://newtoki128.com/"

        # 홈으로 이동
        self.__driver.get(url=self.__newtokiUrl)

        # 로그인 페이지로 이동
        self.__driver.find_element_by_id("basic_outlogin").submit()

        # 로그인 데이터 채우기
        self.__driver.find_element_by_name("mb_id").send_keys("hans3019")
        self.__driver.find_element_by_name("mb_password").send_keys("swc39501!")

        # 캡챠 처리
        # 최종적으로 캡챠는 텔레그램으로 받자
        # 일단은 딜레이 주고 시간내에 입력하도록 유도
        #self.m_driver.find_element_by_name("auto_login").click()
        #self.m_driver.find_element_by_name("captcha_key").send_keys("")
        # 캡차 입력 시간 잠시 대기

        form = self.__driver.find_element_by_name("flogin")

        captcha = form.find_element_by_id("captcha")
        captcha_key = captcha.find_element_by_name("captcha_key")
        captcha_img = captcha.find_element_by_css_selector('img.captcha_img')
        captcha_png = captcha_img.screenshot_as_png

        # captcha 이미지 url 분석 t 추출
        captcha_img_src:string = captcha_img.get_attribute("src")
        captcha_url = urllib.parse.urlparse(captcha_img_src)
        captcha_t = urllib.parse.parse_qs(captcha_url.query)["t"][0]

        # 메세지 전송
        self.__telegramBotRepo.sendPhoto(self.__telegramChatID, captcha_png, "Captcha token : "+captcha_t+"\n(by Login)")

        while True:

            # 텔레그램 메세지 콜백에서 체크
            captcha_value = self.__telegramBotRepo.popCaptchaValue(captcha_t)
            if captcha_value != None:
                captcha_key.send_keys(captcha_value)
            else:
                # input box에서 확인
                captcha_value:string = captcha_key.get_attribute('value')

            # 4자리 입력 될때까지 대기
            if len(captcha_value) == 4:
                break
            print("actionLogin captcha wait. t="+captcha_t)
            sleep(1) 

        # 로그인 하기
        form.submit()

        print("actionLogin end.")
        return

    # 포인트 광산
    def actionMine(self):
        print("actionMine start.")

        # alert 창이 열려 있는 경우 닫는다.
        try:
            alert = self.__driver.switch_to.alert
            print("alert : "+alert.text)
            alert.accept()
        except:
            pass

        # 대상 url
        mineUrl = self.__newtokiUrl + "/mine"

        # 현재 브라우저가 목록에 있을 경우
        if self.__driver.current_url == mineUrl:
            # 새로 고침 한다
            self.__driver.refresh()

            # 게시글 중에 최상위에 있는 것을 클릭 한다
            listItems = self.__driver.find_element_by_name("fboardlist").find_elements_by_class_name("list-item")
            listItems[0].find_element_by_class_name("wr-subject").find_element_by_tag_name("a").click()        
        elif self.__driver.current_url != mineUrl:
            # 목록 페이지가 아닌 경우
            if self.__driver.current_url.startswith(mineUrl+"/"):
                # 이미 채굴 게시판에 들어가 있는 경우
                pass
            else:
                # 다른 곳에 위치한 경우 이동 해준다
                self.__driver.get(url=mineUrl)

                # 게시글 중에 최상위에 있는 것을 클릭 한다
                listItems = self.__driver.find_element_by_name("fboardlist").find_elements_by_class_name("list-item")
                listItems[0].find_element_by_class_name("wr-subject").find_element_by_tag_name("a").click()

        # 현재 채굴 페이지
        #current_url = self.__driver.current_url

        # 채굴 버튼 상태가 대기중이면 활성화 될때까지 대기

        # 채굴 방법 선택 : 1~3 랜덤, wr_player_mining_tool_1~6
        sleep(1)
        tool_id = str(random.randrange(2,5))
        self.__driver.find_element_by_id("wr_player_mining_tool_"+tool_id).click()

        # 버튼 클릭
        btnSubmit = self.__driver.find_element_by_id("btn_submit")
        if btnSubmit.text == '채굴':
            btnSubmit.click()
            
            try:
                # 2초 대기
                sleep(2)
                alert = self.__driver.switch_to.alert
                print("alert : "+alert.text)
                alert.accept()
            except:
                print("go no alert.")

                # 클릭 처리는 ajax 처리 되지만 결과값 반영을 위해 쿨하게 새로 고침
                self.__driver.refresh()
                print("actionMine end.")
                return True
        
        print("actionMine pass.")
        return False

    # 몬스터 광산
    def actionMonster(self):
        print("actionMonster start.")

        # alert 창이 열려 있는 경우 닫는다.
        try:
            alert = self.__driver.switch_to.alert
            print("alert : "+alert.text)
            alert.accept()
        except:
            pass

        # 대상 url
        monsterUrl = self.__newtokiUrl + "/monster"

        # 현재 브라우저가 목록에 있을 경우
        if self.__driver.current_url == monsterUrl:
            # 새로 고침 한다
            self.__driver.refresh()

            # 게시글 중에 최상위에 있는 것을 클릭 한다
            listItems = self.__driver.find_element_by_name("fboardlist").find_elements_by_class_name("list-item")
            listItems[0].find_element_by_class_name("wr-subject").find_element_by_tag_name("a").click()        
        elif self.__driver.current_url != monsterUrl:
            # 목록 페이지가 아닌 경우
            if self.__driver.current_url.startswith(monsterUrl+"/"):
                # 이미 채굴 게시판에 들어가 있는 경우
                pass
            else:
                # 다른 곳에 위치한 경우 이동 해준다
                self.__driver.get(url=monsterUrl)

                # 게시글 중에 최상위에 있는 것을 클릭 한다
                listItems = self.__driver.find_element_by_name("fboardlist").find_elements_by_class_name("list-item")
                topItem = listItems[0]
             
                wr_dates = topItem.find_elements_by_class_name("wr-date")
                wr_date_end:string = wr_dates[1].text
                wr_date_end = wr_date_end.strip()
                if wr_date_end != "":
                    return True

                topItem.find_element_by_class_name("wr-subject").find_element_by_tag_name("a").click()

        # 현재 채굴 페이지
        #current_url = self.__driver.current_url

        # 폼 처리
        form = None
        try:
            form = self.__driver.find_element_by_name("fviewcomment")
        except:
            self.__driver.get(url=monsterUrl)
            return True

        # 캡챠 있는지 체크
        captcha = None
        try:
            captcha = form.find_element_by_id("captcha")
        except:
            pass

        # 캡차가 있는 경우
        if captcha != None:
            captcha_key = captcha.find_element_by_id("captcha_key")
            captcha_img = captcha.find_element_by_css_selector('img.captcha_img')
            captcha_img_src = captcha_img.get_attribute("src")
            captcha_png = captcha_img.screenshot_as_png
           
            # captcha 이미지 url 분석 t 추출
            captcha_url = urllib.parse.urlparse(captcha_img_src)
            captcha_t = urllib.parse.parse_qs(captcha_url.query)["t"][0]

            # 메세지 전송
            self.__telegramBotRepo.sendPhoto(self.__telegramChatID, captcha_png, "Captcha token : "+captcha_t+"\n(by 몬스터 레이드)")
          
            while True:
                # 텔레그램 메세지 콜백에서 체크
                captcha_value = self.__telegramBotRepo.popCaptchaValue(captcha_t)
                if captcha_value != None:
                    captcha_key.send_keys(captcha_value)
                else:
                    # input box에서 확인
                    captcha_value:string = captcha_key.get_attribute('value')

                # 4자리 입력 될때까지 대기
                if len(captcha_value) == 4:
                    break
                print("actionMonster captcha wait.")
                sleep(1)
       
        # 버튼 클릭
        try:
            btnSubmit = form.find_element_by_css_selector("button[type='submit']")
        except:
            self.__driver.get(url=monsterUrl)
            return False

        # 공격 버튼 상태가 대기중이면 활성화 될때까지 대기
        if btnSubmit.text == '공격':

             # 공격 방법 선택 1~6 랜덤 : wr_player_attack_1~6
            sleep(1)
            attack_id = str(random.randrange(1,7))
            self.__driver.find_element_by_id("wr_player_attack_"+attack_id).click()
            
            btnSubmit.click()
            
            # 2초 대기
            sleep(2)
            alert = self.__driver.switch_to.alert
            print("alert : "+alert.text)
            alert.accept()

            print("actionMonster end.")
            return True
        
        print("actionMonster fail.")
        return False
