import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import helpers


class UrbanRoutesPage:

    # ---------- Locators ----------
    # Route / address
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    call_taxi_button = (By.XPATH, "//button[text()='Call a taxi' or text()='Заказать']")

    # Tariff cards
    tariff_cards = (By.CLASS_NAME, 'tcard')
    supportive_tariff = (By.XPATH, "//div[@class='tcard-title' and text()='Supportive']/..")

    # Phone number
    phone_field_trigger = (By.CLASS_NAME, 'np-text')
    phone_input = (By.ID, 'phone')
    phone_submit_button = (By.CSS_SELECTOR, 'button.button.full')
    sms_code_input = (By.ID, 'code')
    sms_code_confirm_button = (By.CSS_SELECTOR, 'button.button.full')

    # Payment / card
    payment_method_trigger = (By.CLASS_NAME, 'pp-text')
    add_card_button = (By.CLASS_NAME, 'pp-plus')
    card_number_input = (By.ID, 'number')
    card_code_input = (By.CSS_SELECTOR, "input#code.card-input")
    link_button = (By.XPATH, "//button[text()='Link']")
    close_payment_modal_button = (By.CLASS_NAME, 'close-button')

    # Comment for driver
    comment_field = (By.ID, 'comment')

    # Requirements
    blanket_switch = (
        By.XPATH,
        "//div[text()='Blanket and handkerchiefs']/following-sibling::div[contains(@class,'switch')]"
    )
    blanket_checkbox = (
        By.XPATH,
        "//div[text()='Blanket and handkerchiefs']/..//input[@type='checkbox']"
    )
    icecream_plus_button = (
        By.XPATH,
        "//div[text()='Ice cream']/../..//div[contains(@class,'counter-plus')]"
    )
    icecream_count_value = (
        By.XPATH,
        "//div[text()='Ice cream']/../..//div[contains(@class,'counter-value')]"
    )

    # Order confirmation
    order_button = (By.CLASS_NAME, 'smart-button')
    car_search_modal = (By.CLASS_NAME, 'order-header-title')

    # ---------- Init ----------
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # ---------- Route / address ----------
    def set_from(self, address_from):
        field = self.wait.until(EC.presence_of_element_located(self.from_field))
        field.clear()
        field.send_keys(address_from)

    def set_to(self, address_to):
        field = self.driver.find_element(*self.to_field)
        field.clear()
        field.send_keys(address_to)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def click_call_taxi_button(self):
        self.wait.until(EC.element_to_be_clickable(self.call_taxi_button)).click()

    # ---------- Tariff ----------
    def select_plan(self, plan_name='Supportive'):
        self.wait.until(EC.presence_of_element_located(self.tariff_cards))
        plan_card = self.wait.until(EC.element_to_be_clickable(self.supportive_tariff))

        # Only click if it isn't already selected, to avoid an unnecessary
        # click that could toggle it back off or hit a stale element.
        if not self.is_plan_selected(plan_name):
            plan_card.click()

    def is_plan_selected(self, plan_name='Supportive'):
        plan_card = self.driver.find_element(*self.supportive_tariff)
        return 'active' in plan_card.get_attribute('class')

    # ---------- Phone number ----------
    def click_phone_field(self):
        self.wait.until(EC.element_to_be_clickable(self.phone_field_trigger)).click()

    def enter_phone_number(self, phone_number):
        field = self.wait.until(EC.visibility_of_element_located(self.phone_input))
        field.send_keys(phone_number)

    def click_phone_submit_button(self):
        self.driver.find_element(*self.phone_submit_button).click()

    def enter_sms_code(self):
        code_field = self.wait.until(EC.visibility_of_element_located(self.sms_code_input))
        code = helpers.retrieve_phone_code(self.driver)
        code_field.send_keys(code)

    def click_sms_confirm_button(self):
        self.driver.find_element(*self.sms_code_confirm_button).click()

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_field_trigger).text

    # ---------- Payment / card ----------
    def click_payment_method(self):
        self.wait.until(EC.element_to_be_clickable(self.payment_method_trigger)).click()

    def click_add_card(self):
        self.wait.until(EC.element_to_be_clickable(self.add_card_button)).click()

    def enter_card_number(self, card_number):
        field = self.wait.until(EC.visibility_of_element_located(self.card_number_input))
        field.send_keys(card_number)

    def enter_card_code(self, card_code):
        field = self.driver.find_element(*self.card_code_input)
        field.send_keys(card_code)
        # The "Link" button doesn't become clickable until the CVV field
        # loses focus, so TAB away from it to trigger validation.
        field.send_keys(Keys.TAB)

    def click_link_button(self):
        self.wait.until(EC.element_to_be_clickable(self.link_button)).click()

    def close_payment_modal(self):
        self.wait.until(EC.element_to_be_clickable(self.close_payment_modal_button)).click()

    # ---------- Comment for driver ----------
    def enter_comment(self, comment):
        field = self.wait.until(EC.presence_of_element_located(self.comment_field))
        field.clear()
        field.send_keys(comment)

    def get_comment(self):
        return self.driver.find_element(*self.comment_field).get_property('value')

    # ---------- Blanket and handkerchiefs ----------
    def order_blanket_and_handkerchiefs(self):
        self.wait.until(EC.element_to_be_clickable(self.blanket_switch)).click()

    def is_blanket_ordered(self):
        checkbox = self.driver.find_element(*self.blanket_checkbox)
        return checkbox.is_selected()

    # ---------- Ice cream ----------
    def order_ice_cream(self, quantity=2):
        plus_button = self.wait.until(EC.element_to_be_clickable(self.icecream_plus_button))
        for _ in range(quantity):
            plus_button.click()
            time.sleep(0.3)  # brief pause so the counter has time to update between clicks

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.icecream_count_value).text)

    # ---------- Order the taxi ----------
    def click_order_taxi_button(self):
        self.wait.until(EC.element_to_be_clickable(self.order_button)).click()

    def is_car_search_modal_displayed(self):
        return self.wait.until(EC.visibility_of_element_located(self.car_search_modal)).is_displayed()