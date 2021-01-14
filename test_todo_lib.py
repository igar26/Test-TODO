import logging
import http.client
import os
module_logger = logging.getLogger('TEST TODO APPLICATION')
# Not using this to get better practice with selenium webdriver API
# from bs4 import BeautifulSoup 
# Can use find_elements_by_css_selector for most of the web elements but prefer practicing all
is_display_flag = True if os.environ.get('DISPLAY_CHANGES') == "True" else False

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


def get_elements_after_compare(l1, l2):
    """
    This function returns the difference between two lists.
    """
    # NOTE: I could not use dict or set as the code gets too complicated also there are no uniquie 
    # elemets to create a dictionary in the todo-item
    # Also todo list can contain same elements multiple times, so the best way is to 
    # use list
    ml = l1 if len(l1) > len(l2) else l2
    sl = l2 if ml == l1 else l1
    diff = [item for item in ml if not item in sl]
    return diff

class ToDoAppPage:
    
    URL = 'http://localhost:3000/'

    def __init__(self, browser):  
        self.browser = browser
        self.total_tasks = 0
        self.total_done_task = 0
        self.total_undone_task = 0
        self.current_task_state_in_page = list()

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
        return True
    
    def get_page_state(self):
        """
        This function is used to get each tasks item and store it in a dictionary.
        params: None
        """
        module_logger.debug("This function collects all the tasks from the page and return the state as dictionary")
        elemnts = self.browser.find_elements_by_css_selector('li.Todo-item')
        self.current_task_state_in_page = list()
        for ele in elemnts:
            task_state = ele.find_element_by_css_selector('span.icon').text
            task_name = ele.find_element_by_css_selector('div').text.strip()
            self.current_task_state_in_page.append([task_name, "done" if "X" in  task_state else "undone"])
        return self.current_task_state_in_page
    

class TaskAction(ToDoAppPage):

    def __init__(self, browser):

        super(TaskAction, self).__init__(browser)
    
    def add_task(self, task_name):
        """
        This function is used to add a new task.
        params: task_name: Task to be added, can be passed as  a list or string
        """
        if not isinstance(task_name, list):
            task_name = [task_name]

        for task in task_name:
            module_logger.debug("Adds task: {}".format(task))
            add_ele = self.browser.find_element_by_tag_name("input")
            add_ele.send_keys(task)
            find_ele = self.browser.find_element_by_class_name("submit")
            find_ele.submit()
            module_logger.debug("Check added task {} is visible to the user".format(task))
            if is_display_flag:
                assert find_ele.is_displayed() == True
    
    def change_task(self, task_name=[], all=False):
        """
        This function is used to modify any/all task/tasks state to done/undone.
        params: task_name: Task to be modified, can be passed as  a list or string
                all = True: If user needs to change the state of all the tasks
        """
        if not isinstance(task_name, list):
            task_name = [task_name]

        elemnts = self.browser.find_elements_by_css_selector('li.Todo-item')
        if not all:
            for task in task_name:
                for ele in elemnts:
                    name = ele.find_element_by_css_selector('div').text.strip()
                    if name == task:
                        ele.find_element_by_css_selector('span.icon').click()
                        if is_display_flag:
                            assert ele.is_displayed() == True
                        break
        else:
            for ele in elemnts:
                ele.find_element_by_css_selector('span.icon').click()
                if is_display_flag:
                    assert ele.is_displayed() == True

    # NOTE: This can change and delete can be combined for user readability its maintained in different function
    def delete_task(self, task_name=[], all=False):
        """
        This function is used to delete any/all task/tasks.
        params: task_name: Task to be deleted, can be passed as  a list or string
                all = True: If user needs to delete all the tasks
        """
        if not isinstance(task_name, list):
            task_name = [task_name]

        elemnts = self.browser.find_elements_by_css_selector('li.Todo-item')
        if not all:
            for task in task_name:
                for ele in elemnts:
                    name = ele.find_element_by_css_selector('div').text.strip()
                    if name == task:
                        ele.find_element_by_css_selector('button').click()
                        if is_display_flag:
                            assert ele.is_displayed() == True
                        break
        else:
            for ele in elemnts:
                ele.find_element_by_css_selector('button').click()
                if is_display_flag:
                        assert ele.is_displayed() == True
    
    def screentshot_task(self, task_name):
        """
        This function is used to take a screenshot of a particular element.
        params: task_name: Task to be used to take a screenshot
        """
        if not isinstance(task_name, str):
            raise AttributeError

        elemnts = self.browser.find_elements_by_css_selector('li.Todo-item')
        try:
            if not all:
                for ele in elemnts:
                    name = ele.find_element_by_css_selector('div').text.strip()
                    if name == task_name:
                        assert ele.find_element_by_css_selector('div').screenshot("~/name-{}.png".format(random_choice(range(0, 100)))) == True
                        break
        # Need to remove the screenshot file to be done
        finally:
            pass
        

        
