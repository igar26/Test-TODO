import test_todo_lib
import logging
import pytest
import random

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
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

result = dict()


# NOTE: Run pytest using --capture=tee-sys option inorder to display standard output
# TODO: Improve logging messages

def add_task_test(test_page, task):

    logger.debug("Get the state of all the tasks before adding a new task")
    before_todo_add = test_page.get_page_state()
    logger.info("Add a new task")
    test_page.add_task(task)
    logger.debug("Get the state of all the tasks after adding a new task")
    after_todo_add = test_page.get_page_state()
    logger.info("Verify the task added")
    updated_page_state = test_todo_lib.get_elements_after_compare(after_todo_add, before_todo_add)
    assert len(updated_page_state) == 1
    assert ['' if task.isspace() else task, "undone"] in updated_page_state
    logger.info("Change the task added task \"{}\" to be done".format(task))
    test_page.change_task('' if task.isspace() else task)
    logger.debug("Get the state of all the tasks after changing the added task to \
        done to validate nothing changed in the state page")
    after_todo_change = test_page.get_page_state()
    assert ['' if task.isspace() else task, "done"] in after_todo_change


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
        result["TEST_CASE1"] = "PASSED"
    except Exception as e:
        logger.error("test_basic_page failed due to ERROR: " + str(e))
        result["TEST_CASE1"] = "FAILED"
        raise e


def test_check_add_task(browser):
    """
    This test case is used to add a task with same name to the todo app
    """
    try:

        logger.info("2. Verify the application is up and running")
        assert test_todo_lib.checkServer() == True
        test_page = test_todo_lib.TaskAction(browser)
        test_page.load()
        add_task_test(test_page, task="new")
        logger.info("Add teh same task again and check it works fine")
        add_task_test(test_page, task="new")
        result["TEST_CASE2"] = "PASSED"

    except Exception as e:
        logger.error("test_check_add_task failed due to ERROR: " + str(e))
        result["TEST_CASE1"] = "FAILED"
        raise e


def test_check_add_task_special_char(browser):
    """
    This test case is used to add a task with same neme to the todo app
    """
    try:

        logger.info("3. Verify the application is up and running")
        assert test_todo_lib.checkServer() == True
        test_page = test_todo_lib.TaskAction(browser)
        test_page.load()
        add_task_test(test_page, task="           ")
        logger.info("Add the same task again and check it works fine")
        add_task_test(test_page, task="           ")
        add_task_test(test_page, task="$$$$$$$$$$$$$")
        logger.info("Add the same task again and check it works fine")
        add_task_test(test_page, task="$$$$$$$$$$$$$")
        add_task_test(test_page, task="eyuewgwu*$#@%^&")
        logger.info("Add the same task again and check it works fine")
        add_task_test(test_page, task="eyuewgwu*$#@%^&")
        add_task_test(test_page, task="\"its a task with space\"")
        logger.info("Add the same task again and check it works fine")
        add_task_test(test_page, task="\"its a task with space\"")
        #FIXME- Wrapping is not working - need to debug further
        logger.info("Add a task with really long task name with spaces")
        add_task_test(test_page, task="\"really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long\"")
        logger.info("Add the same task again and check it works fine")
        add_task_test(test_page, task="\"really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long task really long\"")
        logger.info("Add a task with really long task name without any spaces")
        add_task_test(test_page, task="\"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"")
        logger.info("Add the same task again and check it works fine")
        add_task_test(test_page, task="\"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"")

        result["TEST_CASE3"] = "PASSED"

    except Exception as e:
        logger.error("test_check_add_task failed due to ERROR: " + str(e))
        result["TEST_CASE3"] = "FAILED"
        raise e

#@pytest.mark.skip(reason="no way of currently testing this as we cannot delete more than one task")
def test_delete_task(browser):
    """
    This test case is used to delete all tasks on the page
    """
    try:

        logger.info("4. Verify the application is up and running")
        assert test_todo_lib.checkServer() == True
        test_page = test_todo_lib.TaskAction(browser)
        test_page.load()
        test_page.delete_task(all=True)
        result["TEST_CASE4"] = "PASSED"

    except Exception as e:
        logger.error("test_check_add_task failed due to ERROR: " + str(e))
        result["TEST_CASE4"] = "FAILED"
        raise e

#@pytest.mark.skip(reason="no way of currently testing this as page crashs")
def test_funcitonal_to_add_delete_modify_task(browser):
    """
    This test case is used to test whether add/modify/delate actions work as expected
    """
    try:

        logger.info("5. Verify the application is up and running")
        assert test_todo_lib.checkServer() == True
        test_page = test_todo_lib.TaskAction(browser)
        test_page.load()
        logger.info("Add a new task to the page")
        test_page.add_task(task_name=["test_task_add1", "test_task_add2", "test_task_add3", "test_task_add4", "test_task_add5",
                                      "test_task_add6", "test_task_add7", "test_task_add8", "test_task_add9", "test_task_add10"])
        logger.info("Get all the tasks from the page and pick a random task to delete")
        for _ in range(0, 4):
            gt_pg_state = test_page.get_page_state()
            task_to_delete = random.choice(gt_pg_state)
            logger.info("Delete task: {}".format(task_to_delete[0]))
            test_page.delete_task(task_name=task_to_delete[0])
        for _ in range(0, 4):
            logger.info("Get all the tasks from the page and pick a random task to modify")
            gt_pg_state1 = test_page.get_page_state()
            task_to_modify = random.choice(gt_pg_state)
            logger.info("Modify task: {}".format(task_to_modify[0]))
            test_page.change_task(task_name=task_to_modify[0])

        result["TEST_CASE5"] = "PASSED"

    except Exception as e:
        logger.error("test_check_add_task failed due to ERROR: " + str(e))
        result["TEST_CASE5"] = "FAILED"
        raise e


def test_performance_to_add_delete_modify_task(browser):
    """
    This test case is used to check the performance of the app.
    Add a task 100 times, modify it and then delete it.
    """
    try:

        logger.info("5. Verify the application is up and running")
        assert test_todo_lib.checkServer() == True
        test_page = test_todo_lib.TaskAction(browser)
        test_page.load()
        for _ in range(0, 100):
            logger.info("Add a new task to the page")
            test_page.add_task(task_name="test_task_add")
            logger.info("Modify \"test_task_add\"")
            test_page.change_task(task_name="test_task_add")
            logger.info("Modify \"test_task_add\" task again")
            test_page.change_task(task_name="test_task_add")
            logger.info("Delete task: \"test_task_add\"")
            test_page.delete_task(task_name="test_task_add")
        logger.info("Add 100 new task to the page, modify all and then delete all the tasks")
        logger.info("Add a 100 new task to the page")
        task_list = ["task"+str(i) for i in range(0, 100)]
        test_page.add_task(task_name=task_list)
        logger.info("Modify all 100 tasks")
        test_page.change_task(task_name=task_list)
        logger.info("Modify all 100 tasks again")
        test_page.change_task(task_name=task_list)
        logger.info("Delete tall 100 tasks")
        test_page.delete_task(task_name=task_list)

        for _ in range(0, 3):
            logger.info("Now try adding a 100 new task and delete it wihout modifying it")
            test_page.add_task(task_name=task_list)
            logger.info("Try deleting all the 100 tasks")
            test_page.delete_task(task_name=task_list)

        result["TEST_CASE6"] = "PASSED"

    except Exception as e:
        logger.error("test_check_add_task failed due to ERROR: " + str(e))
        result["TEST_CASE6"] = "FAILED"
        raise e

# Dont know if this is necessary - had to fix it.
def test_screenshot(browser):
    """
    This test case is used to check whether we aree able to take a screen shot without any I/O ERROR.
    """
    try:

        logger.info("5. Verify the application is up and running")
        assert test_todo_lib.checkServer() == True
        test_page = test_todo_lib.TaskAction(browser)
        test_page.load()
        logger.info("Add 100 new task to the page, modify all and then delete all the tasks")
        logger.info("Add a 100 new task to the page")
        task_list = ["task"+str(i) for i in range(0, 100)]
        test_page.add_task(task_name=task_list)
        logger.info("Modify all 100 tasks")
        test_page.change_task(task_name=task_list)
        logger.info("Try to take a screenshot of the page, there should be no I/O Error")
        test_page.screentshot_task(task_name="task8")
        result["TEST_CASE7"] = "PASSED"

    except Exception as e:
        logger.error("test_check_add_task failed due to ERROR: " + str(e))
        result["TEST_CASE7"] = "FAILED"
        raise e

def test_screen_shot():
    print("", end="\n")
    for r in result:
        print(str(r) +"............................" + result[r], end="\n")