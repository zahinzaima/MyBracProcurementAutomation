# this is an object of samplePage to automate, which contains all elements
# and actions could be performed, like input, verify etc.
from utils.basic_actions import BasicActions
from playwright.sync_api import expect


class ProcurementPageNavigationBar(BasicActions):
    def __init__(self, page):
        super().__init__(page)
        # write down all the elements here with locator format

        self.requisition = page.get_by_text("Requisition", exact=True)
        #under requisition
        self.create_requisition = page.get_by_role("link", name="Create Requisition")
        self.requisition_initiator_list = page.get_by_role("link", name="Requisition Initiator List")
        self.requisition_list = page.get_by_role("link", name="Requisition List")
        self.requisition_approval_list = page.get_by_role("link", name="Requisition Approve List")
        self.requisition_assign= page.locator("#wrapper").get_by_text("Requisition Assign", exact=True) #will show assign unassign and others options
        self.undo_requisition_review = page.get_by_role("link", name="Undo Requisition Review")
        self.framework_active_list = page.get_by_role("link", name="Framework Active List")
        #under requisition assign
        self.requisition_accept_list= page.get_by_role("link", name="Requisition Accept List")
        self.unassign_requisition = page.get_by_role("link", name="Unassign Requisition")
        self.assigrequisition_bpd_list = page.get_by_role("link", name="Requisition BPD List")

        self.procurement_process = page.locator("#wrapper").get_by_text("Procurement Process")
        #under procurement process
        self.creare_tender_initiation = page.get_by_role("link", name="Create Tender Initiation")
        self.tender_initiation_list = page.get_by_role("link", name="Tender Initiation List")
        self.tender_committee_formation = page.get_by_role("link", name="Tender Committee Formation")
        self.tender_time_extension = page.locator("#wrapper").get_by_text("Tender Time Extension")
        #under time extension
        self.time_extention_list = page.get_by_role("link", name="Time Extension List")
        self.create_time_extension = page.get_by_role("link", name="Create Time Extension")

        self.pre_bid_meeting = page.get_by_role("link", name="Pre Bid Meeting")
        self.change_purchase_approver = page.get_by_role("link", name="Change Purchase Approver")
        self.lock_unlock_requisition_item = page.locator("#wrapper").get_by_text("Lock Unlock Requisition Item")
        #under lock unlock requisition item
        self.create_lock_item = page.get_by_role("link", name="Create Lock Item")
        self.locked_item_list = age.get_by_role("link", name="Locked Item List", exact=True)
        self.create_unlock_item = page.get_by_role("link", name="Create Unlock Item")
        self.unlock_item_list = page.get_by_role("link", name="Unlocked Item List")

        self.expression_of_interest = page.get_by_role("link", name="Expression of Interest")
        self.noal_list = page.get_by_role("link", name="NOAL List")
        self.create_framework_initiation = page.get_by_role("link", name="Create Framework Initiation")
        
        self.purchase_order = page.locator("#wrapper").get_by_text("Purchase Order")
        #under purchase order
        self.work_order = page.locator("#wrapper").get_by_text("Work Order", exact=True)
        #under work order
        self.create_work_order = page.get_by_role("link", name="Create Work Order")
        self.work_order_list = page.get_by_role("link", name="Work Order List")
        self.ps_info_verify = page.get_by_role("link", name="Ps Info Verify")
        self.order_time_extention_tools = page.get_by_role("link", name="Order Time Extension Tools")

        self.direct_purchase = page.locator("#wrapper").get_by_text("Direct Purchase", exact=True)
        #under direct purchase
        self.Create_direct_purchase = page.get_by_role("link", name="Create Direct Purchase")
        self.direct_purchase_list = page.get_by_role("link", name="Direct Purchase List")






        
        
