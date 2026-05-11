

def test_ecis_dashboard_page_is_displayed(ecis_dashboard_page):
    dashboard_page, ecis_welcome_page = ecis_dashboard_page
    # ---------- Database & Supplier ----------
    ecis_welcome_page.select_database("Production")
    ecis_welcome_page.select_supplier("23231")
    ecis_welcome_page.click_continue()

    dashboard_page.dashboard_page()
    dashboard_page.click_menu_file()











