import time
import data
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import helpers
class UrbanRoutesPage:
    # ---- Locators -------------------------------------------------------
    FROM_FIELD = (By.ID, "from")
    TO_FIELD = (By.ID, "to")
    CALL_TAXI_BUTTON = (By.CSS_SELECTOR, ".button.round")

    SUPPORTIVE_PLAN = (By.XPATH, '//div[@class="tcard-title" and text()="Supportive"]/parent::div')
    ACTIVE_PLAN_TITLE = (By.XPATH, '//div[contains(@class, "tcard") and contains(@class, "active")]'
                                   '//div[@class="tcard-title"]')

    PHONE_FIELD_OPEN = (By.CLASS_NAME, "np-text")
    PHONE_INPUT = (By.ID, "phone")
    PHONE_NEXT_BUTTON = (By.XPATH, '//button[text()="Next"]')
    SMS_CODE_INPUT = (By.XPATH, '//div[@class="section active"]//input[@id="code"]')
    SMS_CONFIRM_BUTTON = (By.XPATH, '//button[text()="Confirm"]')

    PAYMENT_METHOD_BUTTON = (By.CLASS_NAME, "pp-button")
    PAYMENT_METHOD_TEXT = (By.CLASS_NAME, "pp-value-text")
    ADD_CARD_BUTTON = (By.CLASS_NAME, "pp-plus-container")
    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CODE_INPUT = (By.XPATH, '//div[@class="card-code-input"]/input[@id="code"]')
    CARD_LINK_BUTTON = (By.XPATH, '//button[text()="Link"]')
    PAYMENT_CLOSE_BUTTON = (By.XPATH, '//div[@class="payment-picker open"]'
                                      '//button[contains(@class, "close-button")]')

    COMMENT_INPUT = (By.ID, "comment")

    BLANKET_SLIDER = (By.XPATH, '//div[@class="r-sw-label"][text()="Blanket and handkerchiefs"]'
                                '/following-sibling::div//span[@class="slider round"]')
    BLANKET_CHECKBOX = (By.XPATH, '//div[@class="r-sw-label"][text()="Blanket and handkerchiefs"]'
                                  '/following-sibling::div//input[@class="switch-input"]')

    ICE_CREAM_PLUS = (By.XPATH, '//div[@class="r-counter-label"][text()="Ice cream"]'
                                '/following-sibling::div//div[@class="counter-plus"]')
    ICE_CREAM_COUNT = (By.XPATH, '//div[@class="r-counter-label"][text()="Ice cream"]'
                                 '/following-sibling::div//div[@class="counter-value"]')

    ORDER_BUTTON = (By.CLASS_NAME, "smart-button-main")
    CAR_SEARCH_MODAL = (By.CLASS_NAME, "order-body")

    # ---- Setup ----------------------------------------------------------
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    # ---- Addresses ------------------------------------------------------
    def set_from(self, address):
        self._visible(self.FROM_FIELD).send_keys(address)

    def set_to(self, address):
        self._visible(self.TO_FIELD).send_keys(address)

    def get_from(self):
        return self.driver.find_element(*self.FROM_FIELD).get_property("value")

    def get_to(self):
        return self.driver.find_element(*self.TO_FIELD).get_property("value")

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    def click_call_taxi(self):
        self._clickable(self.CALL_TAXI_BUTTON).click()

    # ---- Plan -----------------------------------------------------------
    def select_supportive_plan(self):
        # Only click if it isn't already active
        active = self.driver.find_elements(*self.ACTIVE_PLAN_TITLE)
        if active and active[0].text == data.supportive_plan_name:
            return
        self._clickable(self.SUPPORTIVE_PLAN).click()

    def get_active_plan_name(self):
        return self._visible(self.ACTIVE_PLAN_TITLE).text

    # ---- Phone ----------------------------------------------------------
    def set_phone(self, phone):
        self._clickable(self.PHONE_FIELD_OPEN).click()
        self._visible(self.PHONE_INPUT).send_keys(phone)
        self._clickable(self.PHONE_NEXT_BUTTON).click()

    def confirm_sms_code(self):
        code = helpers.retrieve_phone_code(self.driver)
        self._visible(self.SMS_CODE_INPUT).send_keys(code)
        self._clickable(self.SMS_CONFIRM_BUTTON).click()

    def fill_phone_flow(self, phone):
        self.set_phone(phone)
        self.confirm_sms_code()

    def get_phone(self):
        return self._visible(self.PHONE_FIELD_OPEN).text

    # ---- Payment card ---------------------------------------------------
    def open_add_card(self):
        self._clickable(self.PAYMENT_METHOD_BUTTON).click()
        self._clickable(self.ADD_CARD_BUTTON).click()

    def enter_card(self, number, code):
        self._visible(self.CARD_NUMBER_INPUT).send_keys(number)
        code_field = self._visible(self.CARD_CODE_INPUT)
        code_field.send_keys(code)
        code_field.send_keys(Keys.TAB)  # move focus so "Link" becomes enabled

    def is_link_button_clickable(self):
        try:
            self._clickable(self.CARD_LINK_BUTTON)
            return True
        except Exception:
            return False

    def click_link_card(self):
        self._clickable(self.CARD_LINK_BUTTON).click()

    def close_payment_modal(self):
        self._clickable(self.PAYMENT_CLOSE_BUTTON).click()

    def add_card(self, number, code):
        self.open_add_card()
        self.enter_card(number, code)
        self.click_link_card()
        self.close_payment_modal()

    def get_payment_method(self):
        return self._visible(self.PAYMENT_METHOD_TEXT).text

    # ---- Driver comment -------------------------------------------------
    def set_comment(self, message):
        field = self._visible(self.COMMENT_INPUT)
        field.send_keys(message)

    def get_comment(self):
        return self.driver.find_element(*self.COMMENT_INPUT).get_property("value")

    # ---- Extras ---------------------------------------------------------
    def add_blanket(self):
        self._clickable(self.BLANKET_SLIDER).click()

    def is_blanket_selected(self):
        return self.driver.find_element(*self.BLANKET_CHECKBOX).get_property("checked")

    def add_ice_creams(self, quantity):
        for _ in range(quantity):
            self._clickable(self.ICE_CREAM_PLUS).click()

    def get_ice_cream_count(self):
        return int(self._visible(self.ICE_CREAM_COUNT).text)

    # ---- Order ----------------------------------------------------------
    def click_order(self):
        self._clickable(self.ORDER_BUTTON).click()

    def is_car_search_modal_displayed(self):
        return self._visible(self.CAR_SEARCH_MODAL).is_displayed()
