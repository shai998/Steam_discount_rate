#-*-coding: utf-8-*-
"""
Spyder Editor

This is a temporary script file.
"""
#필요한 라이브러리 임포트
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import signal
from PyQt5.QtWidgets import *
from PyQt5 import uic
from selenium import webdriver
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import time

#pyqt5 이용한 ui 만들기
form_class = uic.loadUiType("uitest.ui")[0]
page = 0
#url지정
url = 'https://store.steampowered.com/specials#p='+str(page)+'&tab=TopSellers'
html = urlopen(url)

#beautifulsoup 객체 생성
bs = BeautifulSoup(html, 'html.parser')

#크롬 제어를 위한 드라이버 위치 설정
driver = webdriver.Chrome('C://chd//chromedriver')

#필요한 정보 스크래핑(할인율, 게임타이틀, 게임가격)
discount_rate = bs.find('div', {'id':'TopSellersRows'}).find_all('div', {'class' : 'discount_pct'})
game_title = bs.find('div', {'id' : 'TopSellersRows'}).find_all('div', {'class' : 'tab_item_name'})
game_price = bs.find('div', {'id' : 'TopSellersRows'}).find_all('div', {'class' : 'discount_final_price'})


#현재시간 위에 표시해주기.
now = datetime.datetime.now()
nowdate = now.strftime('%Y')+'년 '+now.strftime('%m')+'월 '+now.strftime('%d')+'일'

#UI창 컨트롤 클래스
class MyWindow(QMainWindow, form_class):  
    #url은 위에 있는 url 사용함.
    global url
    
    #창이 켜졌을 때 메서드
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        
        #Datetime 이라는 라벨의 텍스트 설정
        self.Datetime.setText(nowdate)
        
        #객체의 이벤트에서 connect 함수를 호출하고 인자에 이벤트 처리기에서 수행하는 함수를 기재한다. 
        self.MoveToWeb.clicked.connect(self.btn_clicked)
        self.Search_Start.clicked.connect(self.btn2_clicked)
        self.Clear_button.clicked.connect(self.listbox_clear)
        self.game_title_listbox.itemDoubleClicked.connect(self.listbox_doubleclick)
        #self.pushButton_2.clicked.connect(self.btn2_clickced)
        #QMessageBox.about(self, "message", "clicked")
        
    #이동하기 버튼 클릭시    
    def btn_clicked(self):
        driver.get(url)
        
    def listbox_clear(self):
        self.game_title_listbox.clear()
        self.Dlc_list.clear()
        
    def listbox_doubleclick(self):
        self.Dlc_list.clear()
        QMessageBox.about(self, "검색", "검색을 시작합니다")
        selected_tag_a = driver.find_element_by_css_selector('input#store_nav_search_term.default')
        
        #row인덱스 확인하는 코드
        #listrow = self.game_title_listbox.currentRow()
        
        #현재 선택된 리스트를 텍스트로 받아옵니다.
        listitem = self.game_title_listbox.currentItem()
        #파싱도 한번 해주고
        listitem_split = listitem.text().split('] ')
        list_lstrip = listitem_split[2].lstrip(' [')
        listitem_allstrip = list_lstrip.rstrip(']')
        print(listitem_allstrip)
        #경과 확인을 위하여 콘솔창에 하나 프린트해줍니다.
        print('[' + listitem_allstrip + ']' +' 를 검색합니다')
    
        #검색할 내용이 input창에 들어간다.
        selected_tag_a.send_keys(listitem_allstrip)
        #\ue007은 엔터라는 뜻.
        selected_tag_a.send_keys('\ue007')
    
        #bs = BeautifulSoup(driver.page_source, 'html.parser')
    
        selected_selector = driver.find_element_by_css_selector('span.title')
        selected_selector.click()
        
        #뒤에서 첫번째 인덱스, 즉, 가장 마지막에 들어간 페이지의 핸들값 가져옴
        last_tab = driver.window_handles[-1]
        driver.switch_to.window(window_name=last_tab)
        
        print(driver.current_url)
        bshtml = urlopen(driver.current_url)
        new_bs = BeautifulSoup(bshtml, 'html.parser')
        '''
        item_count = 0
        items = new_bs.find_all('div', {'class' : 'game_area_dlc_name'})
        
        for temp1 in items:
            self.Dlc_list.addItem('[' + items[item_count].get_text() + ']')
            print(items[item_count])
            item_count = item_count+1
        '''
            
        try:
            item_count = 0
            items = new_bs.find_all('div', {'class' : 'game_area_dlc_name'})
            items_discount = new_bs.find_all('div', {'class':'game_area_dlc_price'})
            #items_final_price = new_bs.find_all('div', {'class' : 'discount_final_price'})
            
            for temp1 in items:
                if len(items) == 1:
                    items_lstrip = items[0].get_text().lstrip()
                    items_stripall = items_lstrip.rstrip()
                    
                    price_strip = items_discount[0].get_text().lstrip()
                    price_stripall = price_strip.rstrip()
     
                    #print(items_stripall)
                    self.Dlc_list.addItem('[' + price_stripall + '] ' 
                                          + items_stripall)
                elif len(items) == 0:
                    nodlc = '현재 선택된 게임은 DLC가 없습니다!'
                    self.Dlc_list.addItem(nodlc)
                else:
                    items_lstrip = items[item_count].get_text().lstrip()
                    items_stripall = items_lstrip.rstrip()
                    
                    price_strip = items_discount[item_count].get_text().lstrip()
                    price_stripall = price_strip.rstrip()
                    
                    self.Dlc_list.addItem('[' + price_stripall + '] ' 
                                          + items_stripall)
                    #print(items_split)
                    item_count = item_count+1
                    
        except:
            print('dlc loading error!')
            
    def btn2_clicked(self):        
        self.game_title_listbox.clear()
        x = '-' + self.Discount_Rate.currentText()
        #self.Imsi.setText('할인율 : ' + x + '%')
        im = 0    
        try:     
            for temp in game_title:   
                if int(discount_rate[im].get_text()[:3]) <= int(x):
                    #QMessageBox.about(self, game_title[im].get_text(), game_price[im].get_text())
                    self.game_title_listbox.addItem('['+discount_rate[im].get_text()+' 할인!] '
                                                    +'['+game_price[im].get_text()+']  '
                                                    +'['+game_title[im].get_text()+']')
                    #self.discount_rate_listbox.addItem(discount_rate[im].get_text())
                    #self.game_price_listbox.addItem(game_price[im].get_text())                  
                else:            
                    pass
                im = im+1

                #print("This title's 'discount rate is under 50%") 
                
        except Exception as e:
            print('website-error occured! ' + e)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()




    
    