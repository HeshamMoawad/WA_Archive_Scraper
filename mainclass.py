from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
from MyPyQt5 import QThread,QObject,pyqtSignal
import typing , sqlite3 , os


class Whatsapp(QObject):
    LeadSignal = pyqtSignal(list)

    MAX_SCROLL = """i = document.querySelector("div[class='_3Bc7H g0rxnol2 thghmljt p357zi0d rjo8vgbg ggj6brxn f8m0rgwh gfz4du6o ag5g9lrv bs7a17vp']");return i.scrollHeight;"""
    SCROLL_DOWN_TO = """ i.scrollTo(0,index);return index ;"""
    GET_NUMBERS_LIST = """numbers = document.querySelectorAll('div[class="gfz4du6o r7fjleex"] div[data-testid="cell-frame-container"]');return numbers"""
    SCRAPE_NUMBERS_CODE = """numbers = document.querySelectorAll("div[tabindex='0'] div._3uIPm.WYyr1 div.zoWT4");return numbers;"""
    CURRENT_HIGHT = """return i.scrollTop + i.clientHeight;"""
    MAX_HIGHT = """return i.scrollHeight ;"""
    GET_PHONE = """return numbers[index].querySelector("span[class='ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr i0jNr']").getAttribute("title") ;"""
    LAST_MSG = """return numbers[index].querySelector("span[class='Hy9nV']").textContent ;"""


    def __init__(self,headless,DarkMode:typing.Optional[bool]=False) -> None:
        self.cont = True
        self.headless = headless
        self.con = sqlite3.connect("Data\Database.db")
        self.cur = self.con.cursor()
        option = Options()
        option.headless = self.headless
        option.add_experimental_option("excludeSwitches", ["enable-logging"])
        option.add_argument('--disable-logging')
        option.add_argument("--force-dark-mode") if DarkMode != False else None
        dir_path = os.getcwd()
        profile = os.path.join(dir_path, "profiles", "SoudiNumber")
        option.add_argument(r"user-data-dir={}".format(profile))
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=option)
        self.driver.maximize_window()
        self.driver.get("https://web.whatsapp.com/")
        self.wait = WebDriverWait(self.driver, 500)
        self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@data-testid='chatlist-header']")))   
        self.leadCount = 0
        QThread.sleep(5)
        super().__init__()
    


    def exist(self,table,column,val):
        self.cur.execute(f"""SELECT * FROM {table} WHERE {column} = '{val}'; """)
        return True if self.cur.fetchall() != [] else False


    def add_to_db(self,table,**kwargs):
        """ Numbers --> Number , LastMsg  , Time  """
        try:
            self.cur.execute(f"""
            INSERT INTO {table} {str(tuple(kwargs.keys())).replace("'","")}
            VALUES {tuple(kwargs.values())}; """)
            self.con.commit()
        except Exception as e:
            print(f"\n{e} \nError in Database \n")



    def jscode(self,command):
        return self.driver.execute_script(command)


    def wait_elms(
        self,
        val:str,
        by:str=By.XPATH,
        timeout:int=30,
        )->typing.List[WebElement]:
        
        """ waiting elements """
        self.wait = WebDriverWait(self.driver, timeout=timeout)
        return self.wait.until(EC.presence_of_all_elements_located((by,val)))


    def wait_elm(self,val:str,by:str=By.XPATH,timeout:int=30)->WebElement:
        self.wait = WebDriverWait(self.driver, timeout=timeout)
        arg = (by,val)
        return self.wait.until(EC.presence_of_element_located(arg))


    def wait_clickable(self,val:str,by:str=By.XPATH,timeout:int=30)->WebElement:
        self.wait = WebDriverWait(self.driver, timeout=timeout)
        arg = (by,val)
        return self.wait.until(EC.element_to_be_clickable(arg))
        
    def scrape_Archive(self,max:int):
        QThread.sleep(5)
        self.wait_elm("//div[@class='_2nY6U _1frFQ'] //div[@class='_3OvU8']").click()
        maxhight = self.jscode(self.MAX_SCROLL)
        current = self.jscode(self.SCROLL_DOWN_TO.replace("index","0"))

        while current < maxhight and self.leadCount < max:
            self.wait_elms("//div[@data-testid='cell-frame-container']",timeout=10)
            ###
            elms = self.jscode(self.GET_NUMBERS_LIST)
            for index in range(len(elms)):
                if self.leadCount > max :
                    break
                phone = self.jscode(self.GET_PHONE.replace("index",f"{index}"))
                phone = "+"+(f"{phone}".split("+")[-1][:15]) if "+" in phone else phone
                last_msg = self.jscode(self.LAST_MSG.replace("index",f"{index}"))
                time = datetime.now()
                if not self.exist("Numbers","Number",f"{phone}"):

                    self.add_to_db(
                    table= "Numbers",
                    Number = phone,
                    LastMsg = last_msg ,
                    Time = f"{time.date()}-{time.hour}-{time.minute}-{time.second}"
                    )

                    if "+" in phone:
                        self.LeadSignal.emit([phone,last_msg])
                        self.leadCount = self.leadCount + 1
            ###
            self.jscode(self.SCROLL_DOWN_TO.replace("index",f"{self.jscode(self.CURRENT_HIGHT)+300}"))
            current = self.jscode(self.CURRENT_HIGHT)
            maxhight = self.jscode(self.MAX_HIGHT)


    def exit(self):
        try:
            self.wait_elm("//span[@data-testid='back']").click()
        except :
            pass
        self.wait_elm("//*[@id='app']/div/div/div[3]/header/div[2]/div/span/div[3]/div/span",timeout=5).click()
        self.wait_elm("//li[@data-testid='mi-logout menu-item'] //div[@class='_2oldI dJxPU'][@role='button']",timeout=5).click()
        self.wait_elm("//*[@data-testid='popup-controls-ok']",timeout=5).click()
        QThread.sleep(3)
        self.driver.quit()

