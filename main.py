# TASK 4
import data
import helpers
class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        from helpers import is_url_reachable
        if is_url_reachable(data.URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")


# TASK 3

    test_set_route(self)
        # Add in S8
        print('function created for set route')
        pass
    test_select_plan(self)
        # Add in S8
        print('function created for select plan')
        pass
    test_fill_phone_number(self)
        # Add in S8
        print('function created for fill phone number')
        pass
    test_fill_card(self)
        # Add in S8
        print('function created for fill card')
        pass
    test_comment_for_driver(self)
        # Add in S8
        print('function created for comment for driver')
        pass
    test_order_blanket_and_handkerchiefs(self)
        # Add in S8
        print('function created for order blanket and handkerchiefs')
        pass
 # TASK 5
    def test_order_2_ice_creams(self):
        for ice_creams in range(2):
            # Add in S8
            print("function created for order 2 ice creams")
            pass
    test_car_search_model_appears(self)
        # Add in S8
        print('function created for car search model appears')
        pass

