from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from functools import wraps
import logging

import sys
import os

# Add the parent directory of the current script to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
sys.path.append(parent_dir)

# from plot import Plot

class Plot :
    def __init__(self, **kwargs) -> None:
        self.name = kwargs["name"]
        self.id = kwargs["id"]
        self.price = kwargs["id"]
        self.id = kwargs["id"]
        self.id = kwargs["id"]
        self.id = kwargs["id"]
        self.id = kwargs["id"]
        self.id = kwargs["id"]

def getPlotInfo(area): 
    # driver = webdriver.Remote(command_executor = "http://localhost:4444", options = Options)

    options = Options()
    options.page_load_strategy = 'normal'
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    driver.get('https://asset.led.go.th/newbidreg/')

    # This is the CAPCHA input box element
    capchaInputEle = driver.find_element(By.ID, 'pass')
    # This is CAPCHA confirm button
    confirmEle = driver.find_element(By.ID, 'GFG_Button')
    # This is the answer to CAPCHA input element. We take this and put it inside CAPCHA input box.
    capchaEle = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/table/tbody/tr[1]/td[1]/strong/font/font')
    capchaInputEle.send_keys(capchaEle.text)
    # Set region to the selected region for scraping
    regionEle = driver.find_element(By.NAME, 'region_name')

    ActionChains(driver)\
        .send_keys_to_element(regionEle, area)\
        .send_keys(Keys.ENTER)\
        .perform()

    confirmEle.click()

    # Wait until Selenium redirected to main page

    print("redirecting...")
    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.current_url != "https://asset.led.go.th/newbidreg/")

    # Set up last page variable to iterate over all plot objects in the website

    allPlotEle = driver.find_element(By.XPATH, "//*[@id='box-table-a']/table")

    while hasNext(driver)[0] :

        # headers = ['ชุดที่', 'ลำดับที่การขาย', 'หมายเลขคดี', 'ประเภททรัพย์', 'ไร่', 'งาน', 'ตารางวา', 'ราคาประเมิน', 'ตำบล', 'อำเภอ', 'จังหวัด']
        # p = []
        # for row in allPlotEle.find_elements(By.CSS_SELECTOR, 'tr'):
        #     p.clear()
        #     for cell in row.find_elements(By.CSS_SELECTOR, 'td'):
        #         p.append(cell.text)

        #     if len(p) > 9 and (cell.get_attribute('bgcolor') != '#E74C3C' and row.get_attribute('bgcolor') == None) :
        #         WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable(row)).click()
        #         driver.switch_to.window(driver.window_handles[1])
                
        #         wait2 = WebDriverWait(driver, 2).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/div')))
        #         try:
        #             detailGeneral = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[4]/div/div')
        #             detailPrice1 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[7]/div')
        #             detailPrice2 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[8]')
        #             detailSaleSchedule = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[6]/div/table')
        #             detailSaleDate = driver.find_element(By.TAG_NAME, 'h6').find_element(By.TAG_NAME, 'font')
        #             detailPicture = driver.find_element(By.ID, 'lightgallery').find_element(By.XPATH, './div')
        #             detailMap = driver.find_element(By.ID, 'lightgallery3').find_element(By.XPATH, './div')

        #             tempSaleSchedule = ''
        #             # print(detailGeneral.text)
        #             # print(detailPrice1.text)
        #             # print(detailPrice2.text)
        #             # print(detailSaleDate.text.replace('วันที่ประกาศขึ้นเว็บ ', ''))
        #             for row in detailSaleSchedule.find_elements(By.TAG_NAME, 'td'):
        #                 # todayDate = date.today()
        #                 try :
        #                     checkDate = datetime.strptime(row.text.replace(' ', ''), "%d/%m/%Y")
                            
        #                     if checkDate.date().replace(year = checkDate.year - 543) > date.today():
        #                         tempSaleSchedule = checkDate.date()
        #                         break
        #                 except ValueError:
        #                     pass

        #             pictureLink = ('https://asset.led.go.th' + detailPicture.get_attribute('data-responsive'))
        #             mapLink = ('https://asset.led.go.th' + detailMap.get_attribute('data-responsive'))
        #             tempArea = int(p[4])*1600 + int(p[5])*400 + float(p[6])*4
        #             tempPrice = float(p[7].replace(',', ''))
        #             currentplot = Plot('','')
        #             currentplot.setCaseNumber(p[2])
        #             # create('plot_case')
        #             # create('plots')
        #             # create('plot_picture')
        #             # create('plot_map')
        #             # create('plot_sale')
        #             # create('plot_price')
        #             # insert_plots('api_plotcase', case_number = currentplot.getCaseNumber(), case_province = p[10], case_district = p[8], case_sub_district = p[9])
        #             # insert_plots('api_plot', plot_id = currentplot.getID(), plot_case_id = p[2], plot_lot_number = p[0], plot_sale_order = p[1], plot_type = p[3], plot_size = tempArea, plot_upload_date = detailSaleDate.text)
        #             # insert_plots('api_plotpicture', picture_link = pictureLink, picture_plot_id = currentplot.getID(), picture_id = gen_random_uuid())
        #             # insert_plots('api_plotmap', map_link = mapLink, map_plot_id = currentplot.getID(), map_id = gen_random_uuid())
        #             # insert_plots('api_plotsale', sale_date = tempSaleSchedule, sale_status = '-', sale_plot_id = currentplot.getID(), sale_id = gen_random_uuid())
        #             # insert_plots('api_plotprice', price_plot_id = currentplot.getID(), price_enforcer = tempPrice)


        #             # query.create('plots')
        #             # query.insert('plots',p[0],p[1],p[2],p[3],tempArea,tempPrice,p[8],p[9],p[10],detailSaleDate.text,str(tempSaleSchedule),pictureLink,mapLink)

        #         except NoSuchElementException:
        #             pass

                # driver.close()
                # driver.switch_to.window(driver.window_handles[0])

        # for ele in lastPage.find_elements(By.CSS_SELECTOR, 'a'):
        #     if ele.text == '[หน้าสุดท้าย]':
        #         lastPage.find_element(By.LINK_TEXT, '[Next]').click()
        #         allPlotEle = driver.find_element(By.XPATH, '//*[@id="box-table-a"]/table')
        #         lastPage = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/table[1]/tbody/tr')
        #         lastPageExist = len(lastPage.find_elements(By.LINK_TEXT, '[หน้าสุดท้าย]')) != 0
        #         break
        hasNext(driver)[1].click()
        # wait.until(lambda driver: driver.current_url != 'https://asset.led.go.th/newbidreg/')
        # /html/body/div[4]/div/div[2]/table[1]/tbody/tr/td[3]/div/nav/ul/li[8]/form/a
    print("done looping!")

def hasNext(driver) :

    if len(driver.find_elements(By.NAME, "webFormnn37")) != 0 :
        navigationEle = driver.find_element(By.CSS_SELECTOR, "[aria-label=pagenext]")
        navElements = navigationEle.find_elements(By.XPATH, ".//ul/li")

        if len(navElements) >= 2:
            nextPageBtn = navElements[-2]
        return True, nextPageBtn

    return False, None

def retry_on_exception(retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except (TimeoutException, StaleElementReferenceException) as e:
                    if attempt == retries - 1:  # Last attempt
                        print(f"Failed after {retries} attempts. Error: {e}")
                        raise  # Re-raise the last exception
                    print(f"Attempt {attempt + 1} failed. Retrying in {delay} seconds...")
                    sleep(delay)
            return None
        return wrapper
    return decorator

@retry_on_exception(retries=3, delay=2)
def safe_click_next(driver, next_btn, current_element):
    next_btn.click()
    wait = WebDriverWait(driver, 10)
    wait.until(expected_conditions.staleness_of(current_element))
    # Short sleep to let the new page start loading
    sleep(1)
    return True

getPlotInfo('กระบี่')