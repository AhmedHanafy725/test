cd /root/test; pytest -v testcase.py --junitxml=/test.xml -o junit_suite_name=mytest
cd /root/test; nosetests3 -v testcase.py --with-xunit --xunit-file=/test.xml --xunit-testsuite-name=mytest
