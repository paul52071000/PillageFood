from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import sys
import time
import requests
from datetime import datetime

#宣告帳號密碼 網址
MoonshineCafeLoginPath = 'https://cafe.moonshine.tw/login'
Executables_path = 'C:/Users/MoonShine/Desktop/chromedriver-win64/chromedriver.exe'
account_path = '//*[@id="__next"]/div[1]/main/div/section/form/div[1]/input'
password_path = '//*[@id="__next"]/div[1]/main/div/section/form/div[2]/input'
signin_Path = '//*[@id="__next"]/div[1]/main/div/section/form/button/span[1]'
Sign_inError = '//*[@id="headlessui-dialog-panel-:r5:"]/div/button/span[1]'
ClickTeaPath = '//*[@id="__next"]/div[1]/main/div/div/div/section/div/section/a[2]/div'
accountInput = "paul52071000"
passwordInput = "zxcv123"
RealTimeOrder = '//*[@id="__next"]/div[1]/nav/div/div[2]/a/div[2]'
Tea_IcePath = '//*[@id="__next"]/div[1]/main/div/div/section/div[2]/div/div[3]/section/form/div/main/section[1]/div/label[1]'
Tea_BuyButton = '//*[@id="__next"]/div[1]/main/div/div/section/div[2]/section/form/footer/button[1]'
ReserveButton = '//*[@id="__next"]/div[1]/nav/div/div[3]'
LunchBeafButton = '//*[@id="__next"]/div[1]/main/div/div[1]/div/div/section/div/section[2]/a[1]/div'
LunchBeafRice = '//*[@id="__next"]/div[1]/main/div/div[1]/div/section/div[2]/div/div[3]/section/form/div/main/section/div/label[1]/div'
lunchBeafOrderButton = '//*[@id="__next"]/div[1]/main/div/div[1]/div/section/div[2]/div/div[3]/section/form/footer/button[1]'
shopping_cart = '//*[@id="__next"]/div[1]/nav/div/div[4]/a'
ConfirmCheckOut = '//*[@id="__next"]/div[1]/main/div/div/div/div/section[2]/div/div/button[1]'
import pickle
#驗證網址是否連接正常
def ConfirmPath(confirmValue):
    resp = requests.get(confirmValue)
    if resp.status_code != 200:
        print('無法連接' + confirmValue)
        return
#登入帳號
def LogIn(WebBrowser,account,password):


    accountpath = WebBrowser.find_element_by_xpath(account_path)
    accountpath.clear()
    accountpath.send_keys(account)

    passwordpath = WebBrowser.find_element_by_xpath(password_path)
    passwordpath.clear()
    passwordpath.send_keys(password)

    WebBrowser.find_element_by_xpath(signin_Path).click()
#搶午餐
def PilliageLunch(WebBrowser):

    WebDriverWait(WebBrowser, 3).until(
        EC.element_to_be_clickable((By.XPATH, ReserveButton))
    ).click()

    WebDriverWait(WebBrowser, 3).until(
        EC.element_to_be_clickable((By.XPATH, LunchBeafButton))
    ).click()

    WebDriverWait(WebBrowser, 3).until(
        EC.element_to_be_clickable((By.XPATH, LunchBeafRice))
    ).click()

    WebDriverWait(WebBrowser, 3).until(
        EC.element_to_be_clickable((By.XPATH, lunchBeafOrderButton))
    ).click()



    return
#搶早餐
def PillageBreakFast(WebBrowser,ClickTeaPath,Tea_IcePath,Tea_BuyButton):
    try:
        WebDriverWait(WebBrowser, 3).until(
            EC.element_to_be_clickable((By.XPATH, RealTimeOrder))
        ).click()
        WebDriverWait(WebBrowser, 3).until(
            EC.element_to_be_clickable((By.XPATH, ClickTeaPath))
        ).click()
        WebDriverWait(WebBrowser, 3).until(
            EC.element_to_be_clickable((By.XPATH, Tea_IcePath))
        ).click()
        WebDriverWait(WebBrowser, 3).until(
            EC.element_to_be_clickable((By.XPATH, Tea_BuyButton))
        ).click()
    except TimeoutException:
        print("PillageBreakFast_按鈕點擊失敗：等待超時")
    except NoSuchElementException:
        print("PillageBreakFast_按鈕點擊失敗：找不到元素")
    except Exception as e:
        print(f"PillageBreakFast_按鈕點擊失敗：{str(e)}")
#結帳
def CheckOut(WebBrowser):
    WebDriverWait(WebBrowser, 5).until(
        EC.element_to_be_clickable((By.XPATH, shopping_cart))
    ).click()
    WebDriverWait(WebBrowser, 5).until(
        EC.element_to_be_clickable((By.XPATH, ConfirmCheckOut))
    ).click()

def GetFood():
    try:
        #驗證
        ConfirmPath(MoonshineCafeLoginPath)
        #設定目標時間是09:00
        target_time = datetime.strptime('09:00:00', '%H:%M:%S').time()
        #算開始的時間
        current_time =  datetime.now().time()
        print(f'程式開始時間：{datetime.now().strftime("%H:%M:%S.%f")[:-3]}')
        start_time = time.time()
        #找自動化測試chrome的本地端位置 執行無介面操作
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        chrome = webdriver.Chrome(executable_path=Executables_path)
        chrome.get(MoonshineCafeLoginPath)
        #登入
        LogIn(chrome,accountInput,passwordInput)
        #測試用
       # WebDriverWait(chrome, 3).until(
        ## ).click()
   #     if current_time > target_time :
        PillageBreakFast(chrome, ClickTeaPath, Tea_IcePath, Tea_BuyButton)
        #PilliageLunch(chrome)

        #結帳
        CheckOut(chrome)


    except TimeoutException:
        print("GetFood_等待超時，可能是元素未出現或操作時間過長。")

    except NoSuchElementException:
        print("GetFood_找不到元素，請確保元素的 XPath 正確。")

    except Exception as e:
        print(f"GetFood_發生未預期的錯誤：{str(e)}")

    finally:
        # 顯示結束時間與運行時間
        print(f'程序结束时间：{datetime.now().strftime("%H:%M:%S.%f")[:-3]}')
        End_time = time.time()
        ProcessTime = End_time - start_time
        print(f'程序運行时间：{ProcessTime:.3f} 秒')
        chrome.quit()
        sys.exit(1)
if __name__ == "__main__":
    GetFood()