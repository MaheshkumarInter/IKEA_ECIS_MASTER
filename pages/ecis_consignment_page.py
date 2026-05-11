from playwright.sync_api import expect
import allure
from allure_commons.types import AttachmentType


class EcisConsignmentPage:
    def __init__(self, page):
        self.page = page
        self.consignments_link = page.locator("a[href = '../Consignment/ConsignmentSummary.aspx']").first
        self.create_consignment_button = page.locator("#btnCreate")
        self.select_receiver_code = page.locator("#btnddlRcvCode")
        self.create_new_consignment_button = page.locator("#btnCreateNew")
        self.dispatch_date = page.locator("#dtpPlanDisp")
        self.lu_type = page.locator("#btnddlLUT")
        self.consignment_grid = page.locator("#grdCsm")
        self.view_btn = page.locator("#btnView")

    def click_consignments_link(self):
        # expect(self.consignments_link).to_be_visible(timeout=10000)
        self.consignments_link.click()
        self.page.wait_for_timeout(2000)
        self.page.wait_for_load_state("networkidle", timeout=15000)
        self._screenshot_after("Click Consignments Link")

    def create_consignment(self):
        self.create_consignment_button.click()
        self.page.wait_for_timeout(4000)
        self._screenshot_after("Add Consignments")

    def select_receiver(self, receiver_code):
        self.select_receiver_code.click()
        receiver_grid = self.page.locator("#tblCombo_ddlRcvCode tbody tr")
        row_count = receiver_grid.count()
        for i in range(row_count):
            row = receiver_grid.nth(i)
            receiver_text = row.locator("td").nth(0).inner_text().split("-")[0].strip()
            if receiver_text == receiver_code:
                row.click()
                break
        self.page.wait_for_timeout(2000)
        self._screenshot_after("Receiver Selection")

    def click_create_new_consignment(self):
        with self.page.expect_popup() as popup_info:
            self.create_new_consignment_button.click()
        popup = popup_info.value

        expect(popup).to_have_url(
            "https://ecis-ofp.apps.ikeadt.com/Consignment/Consignment.aspx"
        )

        popup.wait_for_load_state("networkidle")

        # Screenshot 1 – page opened
        allure.attach(
            popup.screenshot(full_page=True),
            name="Create New Consignment - Opened",
            attachment_type=AttachmentType.PNG
        )

        # Click Add Order
        popup.locator("#btnAddOrder").click()
        popup.wait_for_timeout(2000)

        # Screenshot 2 – after Add Order click
        allure.attach(
            popup.screenshot(full_page=True),
            name="After Clicking Add Order",
            attachment_type=AttachmentType.PNG
        )

        #  Select first order checkbox
        row = popup.locator("#grdOrderMod tbody tr").first
        row.locator("td").first.locator("input").check()
        popup.wait_for_timeout(2000)

        #  Screenshot 3 – order selected
        allure.attach(
            popup.screenshot(full_page=True),
            name="Order Selected",
            attachment_type=AttachmentType.PNG
        )

        # Click Add Lines
        popup.locator("#btnAddLines").click()
        popup.wait_for_timeout(2000)

        # Screenshot 4 – lines added
        allure.attach(
            popup.screenshot(full_page=True),
            name="Order Lines Added to Consignment",
            attachment_type=AttachmentType.PNG
        )

    def select_consignment_to_dispatch(self, rce_code):
        screenshot_bytes = self.page.screenshot(full_page=True)
        consignment_row = self.consignment_grid.locator("tbody tr")
        row_count = consignment_row.count()
        for i in range(row_count):
            row = consignment_row.nth(i)
            rce_text = row.locator("td").nth(2).inner_text().strip()
            imported_text = row.locator("td").nth(10).inner_text().strip()
            status_text = row.locator("td").nth(4).inner_text().strip()
            if rce_code in rce_text and status_text == "Trp Booked":
                checkbox = row.locator("td").first.locator("input")
                checkbox.check()  # safer than click()
                break

            self.page.wait_for_timeout(1000)
            allure.attach(
                screenshot_bytes,
                name="Consignment Selection - Dispatch",
                attachment_type=AttachmentType.PNG
            )

    def select_consignment_to_book_trip(self, rce_code):
        self.screenshot_before("Select Consignment to Book Trip")

        consignment_row = self.consignment_grid.locator("tbody tr")
        row_count = consignment_row.count()

        for i in range(row_count):
            row = consignment_row.nth(i)

            rce_text = row.locator("td").nth(2).inner_text().strip()
            imported_text = row.locator("td").nth(10).inner_text().strip()

            if rce_code in rce_text and imported_text == "Missing":
                checkbox = row.locator("td").first.locator("input")
                checkbox.check()  # safer than click()

                self._screenshot_after(
                    f"Consignment Selected for Book Trip - {rce_text}"
                )
                break

    def view_consignment_details_book_trip(self):
        self.page.wait_for_timeout(2000)

        with self.page.expect_popup() as popup_info:
            self.view_btn.click()
        popup = popup_info.value

        expect(popup).to_have_url(
            "https://ecis-ofp.apps.ikeadt.com/Consignment/Consignment.aspx"
        )
        popup.wait_for_load_state("networkidle")

        allure.attach(
            popup.screenshot(full_page=True),
            name="Book Trip - Popup Opened",
            attachment_type=allure.attachment_type.PNG
        )

        from datetime import datetime
        today = datetime.today().strftime("%d-%m-%Y")

        popup.locator("#dtpPlanDisp").fill(today)
        popup.wait_for_timeout(1000)

        allure.attach(
            popup.screenshot(full_page=True),
            name="Book Trip - Planned Dispatch Date Selected",
            attachment_type=allure.attachment_type.PNG
        )
        popup.locator("#btnddlLUT").click()
        popup.wait_for_timeout(1000)
        allure.attach(
            popup.screenshot(full_page=True),
            name="Book Trip - LU Type Dropdown Opened",
            attachment_type=allure.attachment_type.PNG
        )
        popup.locator("#tblCombo_ddlLUT tbody tr").nth(1).click()
        popup.wait_for_timeout(1000)

        allure.attach(
            popup.screenshot(full_page=True),
            name="Book Trip - LU Type Selected",
            attachment_type=allure.attachment_type.PNG
        )

        def handle_dialog(dialog):
            assert "Do you really want to book transport for" in dialog.message
            dialog.accept()

        popup.on("dialog", handle_dialog)

        popup.locator("#btnBookTrp").click()
        popup.wait_for_timeout(2000)

        allure.attach(
            popup.screenshot(full_page=True),
            name="Book Trip - After Clicking Book Transport",
            attachment_type=allure.attachment_type.PNG
        )

    def view_consignment_details_dispatch(self):
        self.page.wait_for_timeout(2000)

        # ---------- Open main consignment popup ----------
        with self.page.expect_popup() as popup_info:
            self.view_btn.click()
        popup = popup_info.value

        expect(popup).to_have_url(
            "https://ecis-ofp.apps.ikeadt.com/Consignment/Consignment.aspx"
        )
        popup.wait_for_load_state("networkidle")

        allure.attach(
            popup.screenshot(full_page=True),
            name="Dispatch - Consignment Popup Opened",
            attachment_type=AttachmentType.PNG
        )

        from datetime import datetime
        today = datetime.today().strftime("%d-%m-%Y")

        # ---------- UI preparation ----------
        popup.evaluate("document.body.style.zoom = '80%'")
        popup.wait_for_timeout(1000)

        allure.attach(
            popup.screenshot(full_page=True),
            name="Dispatch - Zoom Adjusted",
            attachment_type=AttachmentType.PNG
        )

        # ---------- Select consignment lines ----------
        popup.locator("#grdCsmLines_btnSelectAll").click()
        allure.attach(
            popup.screenshot(full_page=True),
            name="Dispatch - All Consignment Lines Selected",
            attachment_type=AttachmentType.PNG
        )

        # ---------- Fill carrier arrival ----------
        popup.locator("#dtpCarArrDate").fill(today)
        popup.locator("#ddlCarArrTimeHrMin_spinUpButton").click(click_count=2)
        popup.wait_for_timeout(1000)
        allure.attach(
            popup.screenshot(full_page=True),
            name="Dispatch - Carrier Arrival Date & Time Set",
            attachment_type=AttachmentType.PNG
        )
        with popup.expect_popup() as new_popup_info:
            popup.locator("#btnChange").click()
        new_popup = new_popup_info.value

        expect(new_popup).to_have_url(
            "https://ecis-ofp.apps.ikeadt.com/Consignment/ConsignmentLines.aspx"
        )
        new_popup.wait_for_load_state("networkidle")
        allure.attach(
            new_popup.screenshot(full_page=True),
            name="Dispatch - Consignment Lines Popup Opened",
            attachment_type=AttachmentType.PNG
        )

        # ---------- Select all lines ----------
        new_popup.locator("#grdCsmLines_btnSelectAll").click()
        allure.attach(
            new_popup.screenshot(full_page=True),
            name="Dispatch - Lines Selected (Lines Popup)",
            attachment_type=AttachmentType.PNG
        )

        # ---------- Set Production Week ----------
        new_popup.locator("#dtpProdWeek").fill(today)
        new_popup.locator("#btnProdWeek").click()
        new_popup.wait_for_timeout(1000)
        allure.attach(
            new_popup.screenshot(full_page=True),
            name="Dispatch - Production Week Set",
            attachment_type=AttachmentType.PNG
        )

        new_popup.close()

        # ---------- Handle dispatch confirmation ----------
        def handle_dialog(dialog):
            assert "Do you really want to dispatch consignment" in dialog.message
            allure.attach(
                popup.screenshot(full_page=True),
                name="Dispatch - Confirmation Alert",
                attachment_type=AttachmentType.PNG
            )
            dialog.accept()

        popup.on("dialog", handle_dialog)

        # ---------- Final dispatch ----------
        popup.locator("#dtpDispDate").fill(today)
        popup.locator("#ddlDispTimeHrMin_spinUpButton").click(click_count=3)
        popup.locator("#txtSealNo1").click()

        popup.locator("#btnDispatch").click()
        popup.wait_for_timeout(2000)
        allure.attach(
            popup.screenshot(full_page=True),
            name="Dispatch - Consignment Dispatched",
            attachment_type=AttachmentType.PNG
        )

    def select_planned_dispatch_date(self):
        from datetime import datetime
        today = datetime.today().strftime("%d-%m-%Y")

        self.screenshot_before("Planned Dispatch Date Selection")

        self.dispatch_date.fill(today)
        self.page.wait_for_timeout(2000)

        self._screenshot_after("Planned Dispatch Date Selected")

    def select_lu_type(self):
        self.screenshot_before("LU Type Selection")

        self.lu_type.click()
        select_all_btn = self.page.locator("#tblCombo_ddlLUT tbody tr").nth(1)
        select_all_btn.click()
        self.page.wait_for_timeout(2000)
        self._screenshot_after("LU Type Selected")

    def screenshot_before(self, step_name: str):
        try:
            allure.attach(
                self.page.screenshot(full_page=True),
                name=f"BEFORE - {step_name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass

    def _screenshot_after(self, step_name: str):
        try:
            allure.attach(
                self.page.screenshot(full_page=True),
                name=f"AFTER - {step_name}",
                attachment_type=allure.attachment_type.PNG
            )
        except Exception:
            pass