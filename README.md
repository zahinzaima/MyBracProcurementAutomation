What to do first:

  1. Install Pycharm Community Edition to your system
  2. Install Python to your system
  3. Install Git to your system
  4. Clone the repository to your system
  5. Open the cloned folder in Pycharm IDE
  6. Open a terminal, and run 'pip install -r requirements.txt'


What are being installed here:

  - Playwright   ->   An automation library to perform end-to-end web testing or web automation.
                 ->   https://playwright.dev/python/
     
  - Pytest       ->   A test framework.
                 ->   https://docs.pytest.org/en/stable/
     
  - Rich         ->   Renders Python tracebacks with syntax highlighting and formatting.
                 ->   https://rich.readthedocs.io/en/stable/traceback.html


What will we do:

  
  - We will be using POM design pattern here, where we will create web pages and store them in /pages folder,
  
  - write our tests [test cases or test suites] in /tests folder,
  
  - store our resources required in /resources folder,
  
  - write commonly used methods to interact with in /utils folder.


How to run test:

  Run following command in Pycharm Terminal for preferred test run:
  
    -> To run all tests from /tests folder: pytest
    
    -> To run a selected test file from /tests folder: pytest /tests/your_desired_test_file_name.py
