"""
This Selenium script downloads the latest account transactions from
Consorsbank. To use this program set the following environment variables:
ACCOUNT: Your account number to login (e.g. 12345)
ACCOUNT-WEB: The CSS selector for the account on Kontoübersicht, e.g.:
             /ev/Mein-Konto-und-Depot/Konten/Umsaetze-und-Zahlungsverkehr/Umsaetze?accountNo=12345
"""

import os
import time

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


class Browser():
    """A simple wraper class for Selenium"""

    def __init__(self):
        self.driver = Chrome()
        self.timeout = 50

    def wait_for(self, selector, trigger, by):
        """Waits for HTML element defined by CSS"""
        try:
            el = WebDriverWait(self.driver, self.timeout).until(
                trigger((by, selector))
            )
            return el
        except Exception:
            print('Could not find element by: ' + selector)

    def click(self, selector, by):
        """Clicks on element"""
        el = self.wait_for(selector, EC.element_to_be_clickable, by)
        el.click()

    def go_to(self, url):
        """Navigates to URL"""
        self.driver.get(url)

    def select(self, selector, text, by):
        """Interacts iwth SELECT elements"""
        el = self.wait_for(selector, EC.presence_of_element_located, by)
        select = Select(el)
        select.select_by_visible_text(text)

    def type_into(self, name, text, by):
        """Types into a form input"""
        el = self.wait_for(name, EC.presence_of_element_located, by)
        el.send_keys(text)

    def quit(self):
        """Close the browser"""
        self.driver.quit()


# Initialize Chrome
b = Browser()

# Open Browser and accept cookies
b.go_to("https://consorsbank.de")
b.click('#popin_tc_privacy_button', By.CSS_SELECTOR)

# Login to Consorsbank
b.click('#header-login-button', By.CSS_SELECTOR)
b.type_into('username', os.getenv('ACCOUNT'), By.NAME)
b.type_into('username', Keys.TAB, By.NAME)
b.wait_for('.ev-login-meta-content',
           EC.presence_of_element_located, By.CSS_SELECTOR)
# Navigate to account
b.click('[href="' + os.getenv('ACCOUNT-WEB') + '"', By.CSS_SELECTOR)

# Set filter and wait
b.select('dateRange', 'Dieses Jahr', By.NAME)

# Click export button
time.sleep(5)
b.click('[ng-show="csv"]', By.CSS_SELECTOR)
time.sleep(5)
b.quit()
