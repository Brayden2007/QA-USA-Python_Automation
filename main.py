# main.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import helpers
from pages import UrbanRoutesPage
import data
from helpers import retrieve_phone_code  # provided with the project

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # Performance logging is required by retrieve_phone_code()
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)

    def setup_method(self):
        # Fresh page for every test so tests stay independent
        self.driver.get(data.urban_routes_url)
        self.page = UrbanRoutesPage(self.driver)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    # Shared preconditions ------------------------------------------------
    def _route_and_supportive(self):
        self.page.set_route(data.address_from, data.address_to)
        self.page.click_call_taxi()
        self.page.select_supportive_plan()

    # 1. Address ----------------------------------------------------------
    def test_set_route(self):
        self.page.set_route(data.address_from, data.address_to)
        assert self.page.get_from() == data.address_from
        assert self.page.get_to() == data.address_to

    # 2. Supportive plan --------------------------------------------------
    def test_select_supportive_plan(self):
        self.page.set_route(data.address_from, data.address_to)
        self.page.click_call_taxi()
        self.page.select_supportive_plan()
        assert self.page.get_active_plan_name() == data.supportive_plan_name

    # 3. Phone number -----------------------------------------------------
    def test_fill_phone_number(self):
        self._route_and_supportive()
        self.page.fill_phone_flow(data.phone_number)
        assert self.page.get_phone() == data.phone_number

    # 4. Credit card ------------------------------------------------------
    def test_add_credit_card(self):
        self._route_and_supportive()
        self.page.open_add_card()
        self.page.enter_card(data.card_number, data.card_code)
        assert self.page.is_link_button_clickable()
        self.page.click_link_card()
        self.page.close_payment_modal()
        assert self.page.get_payment_method() == data.payment_method_card

    # 5. Comment for driver -----------------------------------------------
    def test_comment_for_driver(self):
        self._route_and_supportive()
        self.page.set_comment(data.message_for_driver)
        assert self.page.get_comment() == data.message_for_driver

    # 6. Blanket and handkerchiefs ----------------------------------------
    def test_order_blanket_and_handkerchiefs(self):
        self._route_and_supportive()
        self.page.add_blanket()
        assert self.page.is_blanket_selected() is True

    # 7. Two ice creams ---------------------------------------------------
    def test_order_two_ice_creams(self):
        self._route_and_supportive()
        self.page.add_ice_creams(data.ice_cream_quantity)
        assert self.page.get_ice_cream_count() == data.ice_cream_quantity

    # 8. Order a taxi -----------------------------------------------------
    def test_order_taxi_supportive_tariff(self):
        self._route_and_supportive()
        self.page.fill_phone_flow(data.phone_number)
        self.page.set_comment(data.message_for_driver)
        self.page.click_order()
        assert self.page.is_car_search_modal_displayed() is True

