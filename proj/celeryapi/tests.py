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


class Plot :
    def __init__(self, *args) -> None:
        self.name = args[0]
        self.id = args[1]
        self.price = args[2]
        self.test1 = args[3]
        self.test2 = args[4]
        self.test3 = args[5]
        self.test4 = args[6]
        self.test5 = args[7]
    
    def __str__(self) -> str:
        return (f"Plot : {self.name}, {self.id}, {self.price}, {self.test1}")

def retry_on_exception(retries, delay):
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

@retry_on_exception(3, 1)
def hasNext(driver) :
    if len(driver.find_elements(By.NAME, "webFormnn46")) != 0 :
        navigationEle = driver.find_element(By.CSS_SELECTOR, "[aria-label=pagenext]")
        navElements = navigationEle.find_elements(By.XPATH, ".//ul/li")

        if len(navElements) >= 2:
            nextPageBtn = navElements[-2]
        return True, nextPageBtn

    return False, None

@retry_on_exception(3, 1)
def safe_click_next(driver, next_btn):
    next_btn.click()
    wait = WebDriverWait(driver, 10)
    wait.until(expected_conditions.staleness_of(next_btn))
    return True

@retry_on_exception(3, 1)
def searchFor(driver, area):
    capchaInputEle = driver.find_element(By.ID, 'pass')
    confirmEle = driver.find_element(By.ID, 'GFG_Button')
    capchaEle = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/table/tbody/tr[1]/td[1]/strong/font/font')
    capchaInputEle.send_keys(capchaEle.text)
    regionEle = driver.find_element(By.NAME, 'region_name')
    ActionChains(driver)\
        .send_keys_to_element(regionEle, area)\
        .send_keys(Keys.ENTER)\
        .perform()

    confirmEle.click()
    print("redirecting...")

def getPlotInfo(area): 
    # driver = webdriver.Remote(command_executor = "http://localhost:4444", options = Options)

    options = Options()
    options.page_load_strategy = 'normal'
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options)

    driver.get('https://asset.led.go.th/newbidreg/')

    searchFor(driver, area)

    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.current_url != "https://asset.led.go.th/newbidreg/")

    page_number = 1
    
    while True:
        try:
            print(f"Processing page {page_number}")
            wait = WebDriverWait(driver, 10)
            allPlotEle = driver.find_elements(By.XPATH, "//*[@id='box-table-a']/table/tbody")
            
            for plot in allPlotEle :
                plotTableInfo = plot.find_elements(By.XPATH, ".//td")
                plot = Plot(plotTableInfo[0].text, plotTableInfo[1].text, plotTableInfo[2].text, plotTableInfo[3].text, plotTableInfo[4].text, plotTableInfo[5].text, plotTableInfo[6].text, plotTableInfo[7].text)
                print(plot.__str__())
                # for item in plotTableInfo :
                #     print(item.text)

            has_next, next_btn = hasNext(driver)
            if not has_next:
                print("Reached last page")
                break
                
            # Try to click next with retry mechanism
            if safe_click_next(driver, next_btn):
                page_number += 1
            else:
                print("Failed to navigate to next page")
                break
                
        except Exception as e:
            print(f"Unexpected error on page {page_number}: {str(e)}")
    
    print(f"Done looping! Processed {page_number} pages")

getPlotInfo('กระบี่')