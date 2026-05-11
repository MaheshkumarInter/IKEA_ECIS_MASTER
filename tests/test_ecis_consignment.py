import allure
from testdata.ecis_consignment_data import (TEST_CREATE_CONSIGNMENT_DISPATCH)
@allure.feature("Consignment")
@allure.story("Creation of Consignment from Created to Dispatch")
def test_ecis_create_consignment(ecis_dashboard_page):
    dashboard_page, ecis_welcome_page, *_ ,ecis_consignment_page = ecis_dashboard_page

    data = TEST_CREATE_CONSIGNMENT_DISPATCH

    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_database(data["database"])
        ecis_welcome_page.select_supplier(data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on Consignment menu"):
        ecis_consignment_page.click_consignments_link()

    with allure.step("click on create button"):
        ecis_consignment_page.create_consignment()

    with allure.step("Select Receiver"):
        ecis_consignment_page.select_receiver(data["rvc_code"])

    with allure.step("click create new consignment button"):
        ecis_consignment_page.click_create_new_consignment()


def test_ecis_book_trip_consignment(ecis_dashboard_page):
    dashboard_page, ecis_welcome_page, *_, ecis_consignment_page = ecis_dashboard_page

    data = TEST_CREATE_CONSIGNMENT_DISPATCH

    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_database(data["database"])
        ecis_welcome_page.select_supplier(data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on Consignment menu"):
        ecis_consignment_page.click_consignments_link()

    with allure.step("select the consignment to book trip"):
        ecis_consignment_page.select_consignment_to_book_trip(data["rvc_code"])

    with allure.step("click on view consignment details and Book Trip"):
        ecis_consignment_page.view_consignment_details_book_trip()

def test_ecis_dispatch_consignment(ecis_dashboard_page):

    dashboard_page, ecis_welcome_page, *_, ecis_consignment_page = ecis_dashboard_page

    data = TEST_CREATE_CONSIGNMENT_DISPATCH

    with allure.step(f"Select supplier and database"):
        ecis_welcome_page.select_database(data["database"])
        ecis_welcome_page.select_supplier(data["scode"])
        ecis_welcome_page.click_continue()

    with allure.step("Maintenance Menu"):
        dashboard_page.dashboard_page()
        dashboard_page.click_maintenance()

    with allure.step("click on Consignment menu"):
        ecis_consignment_page.click_consignments_link()

    with allure.step("select the consignment to dispatch"):
        ecis_consignment_page.select_consignment_to_dispatch(data["rvc_code"])

    with allure.step("click on view consignment details and dispatch"):
        ecis_consignment_page.view_consignment_details_dispatch()









