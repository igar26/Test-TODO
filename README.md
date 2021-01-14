# Test-TODO
* This test automation tool uses pytest frame work to test all the functionality of the todo application
1) Test environment configuration:
     * Install the following packages:
          - Python 3.7.3
          - webdriver for selenium
          - pytest   
     * set os.environ.get('DISPLAY_CHANGES') to "True" in order to check/verify is_displayed() flag .
2) The logs will be generated and stored in todo.log file.
3) TO run the module please use "pytest todo_tests.py --capture=tee-sys".
4) Cross browser testing can be done using pytest-xdist, but we are not using it now as it needs a special license. 
