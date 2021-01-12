import logging
import http.client
module_logger = logging.getLogger('TEST TODO APPLICATION')
# Not using this to get better practice with selenium webdriver API
#from bs4 import BeautifulSoup 

def checkServer(host="localhost", port=3000):

    module_logger.debug("Check localhost is running in-order to confirm application is up")
    hh = None
    connectionType = http.client.HTTPConnection
    try:
        hh = connectionType(host, port)
        hh.request('GET', '/_ah/admin')
        resp = hh.getresponse()
        headers = resp.getheaders()
        if headers:
            if (('Connection', 'keep-alive') in headers):
                return True
    except http.client.socket.error:
        return False
    except http.client.BadStatusLine:
        return False
    finally:
        if hh:
            hh.close()
    return False


class ToDoAppPage:
    
    URL = 'http://localhost:3000/'

    def __init__(self, browser):  
        self.browser = browser
        self.total_tasks = 0
        self.total_done_task = 0
        self.total_undone_task = 0

    def load(self):
        """
        This function is used to load the URL under test
        """
        module_logger.debug("Loading URL {} page".format(self.URL))
        self.browser.get(self.URL)

    def get_total_task_count(self):
        """
        This function is used to get how many total tasks are present in the page
        params: None
        """
        module_logger.debug("Get the count of Toto-items")
        total_tasks = len(self.browser.find_elements_by_xpath("//ul[@class='Todo-group']/li[@class='Todo-item']"))
        self.total_tasks = total_tasks
        return total_tasks
    
    def get_total_done_task_count(self):
        """
        This function is used to get how many tasks are marked as done in the page
        params: None
        """
        module_logger.debug("Get the count of Toto-items which are marked as done")
        total_done_tasks = len(self.browser.find_elements_by_xpath("//li[@class='Todo-item']/div[@class='done']"))
        self.total_done_tasks = total_done_tasks
        return total_done_tasks
    
    def get_total_undone_task_count(self):
        """
        This function is used to get how many tasks are marked as undone in the page
        params: None
        """
        module_logger.debug("Get the count of Toto-items which are marked as undone")
        total_undone_task_count = len(self.browser.find_elements_by_xpath("//li[@class='Todo-item']/div[@class='undone']"))
        self.total_undone_task_count = total_undone_task_count
        return total_undone_task_count

    def check_todo_group_present(self):
        """
        This function is used to search for any class item \"Todo-group\", 
            just to make sure we have a group to add items
        params: None
        """
        module_logger.debug("Check todo group present in the page, this is done by comparing \
        the number of total tasks with length of todo group items.")
        l = len(self.browser.find_elements_by_xpath("//ul[@class='Todo-group']/li[@class='Todo-item']"))
        assert l == self.get_total_task_count()
        return True

    def get_page_info_by_class(self, header):
        """
        This function is used to search for any class item in the webpage and return the element, 
        user can extract the text and verify for the text they are searching
        params: header: The text that needs to be serched in the class object
        """
        module_logger.debug("This function finds the webelemets by class name and returns the web-object")
        tex = self.browser.find_element_by_class_name(header)
        return tex
    
    def check_all_tasks_has_proper_close_button(self):
        """
        This function is used to search for any class item in the webpage and check proper
        close buttons are present
        params: None
        """
        module_logger.debug("This function validates whether proper close buttons are present in each task")
        cls_butn_cnt = [x.text for x in self.browser.find_elements_by_xpath("//button[@class='close']")]
        assert cls_butn_cnt.count('×') == self.get_total_task_count()
        return True

    def check_all_tasks_has_proper_selection_button(self):
        """
        This function is used to search for any class item in the webpage and check proper
        selection buttons are present
        params: None
        """
        module_logger.debug("This function validates whether proper selection buttons are present in each task")
        sel_butn_cnt = [x.text for x in self.browser.find_elements_by_xpath("//span[@aria-hidden='true']")]
        assert sel_butn_cnt.count('[ ]') == self.get_total_undone_task_count()
        assert sel_butn_cnt.count('[X]') == self.get_total_done_task_count()
        return True
    
    def check_add_task_button_present(self):
        """
        This function is used to verify add text box is present and has a add button to add tasks
        params: None
        """
        module_logger.debug("This function validates add task test box present")
        assert len(self.browser.find_elements_by_xpath("//form[@class='form-inline']/input[@type='text']")) == 1
        assert len(self.browser.find_elements_by_xpath("//form[@class='form-inline']/button[@type='submit']")) == 1
        add_button = [x.text for x in self.browser.find_elements_by_xpath("//button[@class='submit']")]
        assert len(add_button) == 1
        assert add_button.count('+') == 1
        print([x.text for x in self.browser.find_elements_by_xpath("//form[@class='form-inline']")])
        print(self.get_page_info_by_class(header="submit").text)
        return True
