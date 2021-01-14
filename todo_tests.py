import test_todo_lib
import logging

# create logger with 'todo application'
logger = logging.getLogger('TEST TODO APPLICATION')
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.CRITICAL)
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('todo.log', mode='w')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# NOTE: Run pytest using --capture=tee-sys option inorder to display standard output
# TODO: Improve logging messages

def test_basic_page(browser):
    """
    This test case is used to validate basic unit test of todo app
    """
    try:

        logger.info("Verify the application is up and running")
        assert test_todo_lib.checkServer() == True
        test_page = test_todo_lib.ToDoAppPage(browser)
        test_page.load()
        logger.info("1. Check the basic functions")
        logger.info("1.1 Check whether the header in the web-page is \"Todo list\"")
        assert test_page.get_page_info_by_class("Todo-header").text == "Todo list"

        # FIXME: I am not sure to inclue this in the test case, need to implement this a little better -
        # Dont use find_elemets in the test cases 
        logger.info("1.2 Check whether the page has \"Todo group\" to add all Todo-Item")
        assert test_page.check_todo_group_present() == True

        # NOTE: The following checks are not necessary just in case if we want to validate present 
        # elements of the page with automation
        logger.info("1.3 Check whether total count of tasks in to-do list to be greater than 0")
        assert test_page.get_total_task_count() > 0

        logger.info("1.4 Check whether total count of done tasks in to-do list to be greater than 0")
        assert test_page.get_total_done_task_count() > 0

        logger.info("1.5 Check whether total count of undone task in to-do list to be greater than 0")
        test_page.get_total_undone_task_count() > 0

        logger.info("1.6 Check whether there are proper close buttons for all the tasks")
        assert test_page.check_all_tasks_has_proper_close_button() == True

        logger.info("1.7 Check whether there are proper selection buttons for all the respective tasks")
        assert test_page.check_all_tasks_has_proper_selection_button() == True

        logger.info("1.8 Check whether add task text box is present")
        assert test_page.check_add_task_button_present() == True
    
    except Exception as e:
        logger.error("test_basic_page failed dut to ERROR: " + str(e))
        raise e


def test_check_add_task(browser):
    """
    This test case is used to add a task with same neme to the todo app
    """
    try:

        def task_check():
            logger.debug("Get the state of all the tasks before adding a new task")
            before_todo_add = test_page.get_page_state()
            logger.info("Add a new task")
            test_page.add_task("new")
            logger.debug("Get the state of all the tasks after adding a new task")
            after_todo_add = test_page.get_page_state()
            logger.info("Verify the task added")
            updated_page_state = test_todo_lib.get_elements_after_compare(after_todo_add, before_todo_add)
            assert len(updated_page_state) == 1
            assert ["new", "undone"] in updated_page_state
            logger.info("Change the task added task \"new\" to be done")
            test_page.change_task("new")
            after_todo_change = test_page.get_page_state()
            print(after_todo_change)

        logger.info("2. Verify the application is up and running")
        assert test_todo_lib.checkServer() == True
        test_page = test_todo_lib.TaskAction(browser)
        test_page.load()
        task_check()
        todo_task_check = test_page.get_page_state()
        #assert ["new", "done"] in todo_task_check
        #task_check()
        #assert todo_task_check.count(["new", "done"]) == 2

    except Exception as e:
        logger.error("test_check_add_task failed dut to ERROR: " + str(e))
        raise e

