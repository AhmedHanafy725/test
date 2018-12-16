
from testsuite.testcases.base_test import BaseTest
from Jumpscale import j
from unittest import TestCase
from nose_parameterized import parameterized
import random

currencies = j.clients.currencylayer.cur2usd

class SchemaTest(BaseTest):
    def setUp(self):
        super().setUp()

    
    
    
    def test001_validate_string_type(self):
        """
        SCM-001
        *Test case for validating string type *

        **Test Scenario:**

        #. Create schema with string parameter[P1], should succeed.
        #. Try to set parameter[P1] with non string type, should fail.
        #. Try to set parameter[P1] with string type, should succeed.
        """
        self.log("Create schema with string parameter[P1], should succeed.")
        schema = """
        @url = test.schema
        name = (S)
        """
        schema = self.schema(schema)
        schema_obj = schema.new()

        self.log("Try to set parameter[P1] with non string type, should fail.")
        with self.assertRaises(Exception) as e:
            schema_obj.name = 10

        with self.assertRaises(Exception) as e:
            schema_obj.name = 10.04

        with self.assertRaises(Exception) as e:
            schema_obj.name = [10, 15]

        with self.assertRaises(Exception) as e:
            schema_obj.name = {'name': self.random_string}

        self.log("Try to set parameter[P1] with string type, should succeed.")
        name = self.random_string()
        schema_obj.name = name
        self.assertEqual(schema_obj.name, name)

    def test002_validate_integer_type(self):
        """
        SCM-002
        *Test case for validating integer type *

        **Test Scenario:**

        #. Create schema with integer parameter[P1], should succeed.
        #. Try to set parameter[P1] with non integer type, should fail.
        #. Try to set parameter[P1] with integer type, should succeed.
        """
        self.log("Create schema with integer parameter[P1], should succeed.")
        schema = """
        @url = test.schema
        number = (I)
        """
        schema = self.schema(schema)
        schema_obj = schema.new()

        self.log("Try to set parameter[P1] with non integer type, should fail.")
        with self.assertRaises(Exception) as e:
            schema_obj.number = "10"

        with self.assertRaises(Exception) as e:
            schema_obj.number = 10.5
        
        with self.assertRaises(Exception) as e:
            schema_obj.number = "10.9"
        
        with self.assertRaises(Exception) as e:
            schema_obj.number = self.random_string()
        
        with self.assertRaises(Exception) as e:
            schema_obj.number = ["10", "20"]
        
        with self.assertRaises(Exception) as e:
            schema_obj.number = [10, 20]
        
        with self.assertRaises(Exception) as e:
            schema_obj.number = {'number': 10}

        self.log("Try to set parameter[P1] with integer type, should succeed.")
        rand_num = random.randint(1, 100)
        schema_obj.number = rand_num
        self.assertEqual(schema_obj.number, rand_num)

    def test003_validate_float_type(self):
        """
        SCM-003
        *Test case for validating float type *

        **Test Scenario:**

        #. Create schema with float parameter[P1], should succeed.
        #. Try to set parameter[P1] with non float type, should fail.
        #. Try to set parameter[P1] with float type, should succeed.
        """
        self.log("Create schema with float parameter[P1], should succeed.")
        schema = """
        @url = test.schema
        number = (F)
        """
        schema = self.schema(schema)
        schema_obj = schema.new()

        self.log("Try to set parameter[P1] with non float type, should fail.")
        with self.assertRaises(Exception) as e:
            schema_obj.number = "10"
        
        with self.assertRaises(Exception) as e:
            schema_obj.number = "10.9"
        
        with self.assertRaises(Exception) as e:
            schema_obj.number = self.random_string()
        
        with self.assertRaises(Exception) as e:
            schema_obj.number = ["10", "20"]
        
        with self.assertRaises(Exception) as e:
            schema_obj.number = [10.5, 20.9]
        
        with self.assertRaises(Exception) as e:
            schema_obj.number = {'number': 10.7}

        self.log("Try to set parameter[P1] with float type, should succeed.")
        rand_num = random.randint(1, 100)
        schema_obj.number = rand_num
        self.assertEqual(schema_obj.number, rand_num)
        schema_obj.number = 100.4529
        self.assertEqual(schema_obj.number, 100.4529)

    def test004_validate_boolean_type(self):
        """
        SCM-003
        *Test case for validating boolean type *

        **Test Scenario:**

        #. Create schema with boolean parameter[P1], should succeed.
        #. Try to set parameter[P1] with non boolean type, should fail.
        #. Try to set parameter[P1] with boolean type, should succeed.
        """
        self.log("Create schema with boolean parameter[P1], should succeed.")
        schema = """
        @url = test.schema
        check = (B)
        """
        schema = self.schema(schema)
        schema_obj = schema.new()

        self.log("Try to set parameter[P1] with non boolean type, should fail.")
        with self.assertRaises(Exception) as e:
            schema_obj.check = "10"
        
        with self.assertRaises(Exception) as e:
            schema_obj.check = "10.9"
        
        with self.assertRaises(Exception) as e:
            schema_obj.check = self.random_string()
        
        with self.assertRaises(Exception) as e:
            schema_obj.check = ["10", "20"]
        
        with self.assertRaises(Exception) as e:
            schema_obj.check = [10.5, 20.9]
        
        with self.assertRaises(Exception) as e:
            schema_obj.check = {'number': 10.7}

        self.log("Try to set parameter[P1] with boolean type, should succeed.")
        schema_obj.check = True
        self.assertEqual(schema_obj.check, True)

        schema_obj.check = False
        self.assertEqual(schema_obj.check, False)
        # schema_obj.check = 1
        # self.assertEqual(schema_obj.check, True)

    def test004_validate_mobile_type(self):
        """
        SCM-004
        *Test case for validating mobile type *

        **Test Scenario:**

        #. Create schema with mobile parameter[P1], should succeed.
        #. Try to set parameter[P1] with non mobile type, should fail.
        #. Try to set parameter[P1] with mobile type, should succeed.
        """
        self.log("Create schema with mobile parameter[P1], should succeed.")
        schema = """
        @url = test.schema
        mobile = (tel)
        """
        schema = self.schema(schema)
        schema_obj = schema.new()

        self.log("Try to set parameter[P1] with non mobile type, should fail.")
        
        with self.assertRaises(Exception) as e:
            schema_obj.mobile = "+faafa99"

        with self.assertRaises(Exception) as e:
            schema_obj.mobile = "10.9"
        
        with self.assertRaises(Exception) as e:
            schema_obj.mobile = self.random_string()
        
        with self.assertRaises(Exception) as e:
            schema_obj.mobile = ["10", "20"]
        
        with self.assertRaises(Exception) as e:
            schema_obj.mobile = [10.5, 20.9]
        
        with self.assertRaises(Exception) as e:
            schema_obj.mobile = {'number': 10.7}

        with self.assertRaises(Exception) as e:
            schema_obj.mobile = random.randint(1, 1000)

        self.log("Try to set parameter[P1] with mobile type, should succeed.")
        schema_obj.mobile = '154568847'
        self.assertEqual(schema_obj.mobile, '154568847')
        schema_obj.mobile = '+4564123854'
        self.assertEqual(schema_obj.mobile, '+4564123854')

    def test005_validate_email_type(self):
        """
        SCM-005
        *Test case for validating email type *

        **Test Scenario:**

        #. Create schema with email parameter[P1], should succeed.
        #. Try to set parameter[P1] with non email type, should fail.
        #. Try to set parameter[P1] with email type, should succeed.
        """
        self.log("Create schema with email parameter[P1], should succeed.")
        schema = """
        @url = test.schema
        email = (email)
        """
        schema = self.schema(schema)
        schema_obj = schema.new()

        self.log("Try to set parameter[P1] with non email type, should fail.")
        with self.assertRaises(Exception) as e:
            schema_obj.email = random.randint(1, 100)

        with self.assertRaises(Exception) as e:
            schema_obj.email = random.randint(1, 100) + 0.5
        
        with self.assertRaises(Exception) as e:
            schema_obj.email = self.random_string()

        with self.assertRaises(Exception) as e:
            schema_obj.email = 'example.com'

        with self.assertRaises(Exception) as e:
            schema_obj.email = 'example@com'
        
        with self.assertRaises(Exception) as e:
            schema_obj.email = ["10", "20"]
        
        with self.assertRaises(Exception) as e:
            schema_obj.email = [10.5, 20.9]
        
        with self.assertRaises(Exception) as e:
            schema_obj.email = {'number': 10.7}

        self.log("Try to set parameter[P1] with email type, should succeed.")
        schema_obj.email = 'test.example@domain.com'
        self.assertEqual(schema_obj.email, 'test.example@domain.com')

    def test006_validate_ipport_type(self):
        """
        SCM-006
        *Test case for validating ipport type *

        **Test Scenario:**

        #. Create schema with ipport parameter[P1], should succeed.
        #. Try to set parameter[P1] with non ipport type, should fail.
        #. Try to set parameter[P1] with ipport type, should succeed.
        """
        self.log("Create schema with ipport parameter[P1], should succeed.")
        schema = """
        @url = test.schema
        port = (ipport)
        """
        schema = self.schema(schema)
        schema_obj = schema.new()

        self.log("Try to set parameter[P1] with non ipport type, should fail.")
        with self.assertRaises(Exception) as e:
            schema_obj.port = random.randint(1, 100) + 0.5
        
        with self.assertRaises(Exception) as e:
            schema_obj.port = self.random_string()
        
        with self.assertRaises(Exception) as e:
            schema_obj.port = ["10", "20"]
        
        with self.assertRaises(Exception) as e:
            schema_obj.port = [10.5, 20.9]
        
        with self.assertRaises(Exception) as e:
            schema_obj.port = {'number': 10.7}

        self.log("Try to set parameter[P1] with ipport type, should succeed.")
        port = random.randint(1, 10000)
        schema_obj.port = port
        self.assertEqual(schema_obj.port, port)

    def test007_validate_ipaddr_type(self):
        """
        SCM-007
        *Test case for validating ipaddr type *

        **Test Scenario:**

        #. Create schema with ipaddr parameter[P1], should succeed.
        #. Try to set parameter[P1] with non ipaddr type, should fail.
        #. Try to set parameter[P1] with ipaddr type, should succeed.
        """
        self.log("Create schema with ipaddr parameter[P1], should succeed.")
        schema = """
        @url = test.schema
        ip = (ipaddr)
        """
        schema = self.schema(schema)
        schema_obj = schema.new()

        self.log("Try to set parameter[P1] with non ipaddr type, should fail.")
        with self.assertRaises(Exception) as e:
            schema_obj.ip = random.randint(1, 100)

        with self.assertRaises(Exception) as e:
            schema_obj.ip = random.randint(1, 100) + 0.5
        
        with self.assertRaises(Exception) as e:
            schema_obj.ip = self.random_string()

        with self.assertRaises(Exception) as e:
            schema_obj.ip = '10.20.256.1'
        
        with self.assertRaises(Exception) as e:
            schema_obj.ip = '10.20.1'
        
        with self.assertRaises(Exception) as e:
            schema_obj.ip = ["10", "20"]
        
        with self.assertRaises(Exception) as e:
            schema_obj.ip = [10.5, 20.9]
        
        with self.assertRaises(Exception) as e:
            schema_obj.ip = {'number': 10.7}

        self.log("Try to set parameter[P1] with ipaddr type, should succeed.")
        ip = '10.15.{}.1'.format(random.randint(0, 255))
        schema_obj.ip = ip
        self.assertEqual(schema_obj.ip, ip)

    def test008_validate_iprange_type(self):
        """
        SCM-008
        *Test case for validating iprange type *

        **Test Scenario:**

        #. Create schema with iprange parameter[P1], should succeed.
        #. Try to set parameter[P1] with non iprange type, should fail.
        #. Try to set parameter[P1] with iprange type, should succeed.
        """
        self.log("Create schema with iprange parameter[P1], should succeed.")
        schema = """
        @url = test.schema
        iprange = (iprange)
        """
        schema = self.schema(schema)
        schema_obj = schema.new()

        self.log("Try to set parameter[P1] with non iprange type, should fail.")
        with self.assertRaises(Exception) as e:
            schema_obj.iprange = random.randint(1, 100)

        with self.assertRaises(Exception) as e:
            schema_obj.iprange = random.randint(1, 100) + 0.5
        
        with self.assertRaises(Exception) as e:
            schema_obj.iprange = self.random_string()

        with self.assertRaises(Exception) as e:
            schema_obj.iprange = '10.20.256.1'
        
        with self.assertRaises(Exception) as e:
            schema_obj.iprange = '10.20.1'

        with self.assertRaises(Exception) as e:
            schema_obj.iprange = '10.20.1.0'
        
        with self.assertRaises(Exception) as e:
            schema_obj.iprange = '10.20.1.0/'

        with self.assertRaises(Exception) as e:
            schema_obj.iprange = ["10", "20"]
        
        with self.assertRaises(Exception) as e:
            schema_obj.iprange = [10.5, 20.9]
        
        with self.assertRaises(Exception) as e:
            schema_obj.iprange = {'number': 10.7}

        self.log("Try to set parameter[P1] with iprange type, should succeed.")
        iprange = '10.15.{}.1/24'.format(random.randint(0, 255))
        schema_obj.iprange = iprange
        self.assertEqual(schema_obj.iprange, iprange)
    
    def test009_validate_date_type(self):
        """
        SCM-009
        *Test case for validating date type *

        **Test Scenario:**

        #. Create schema with date parameter[P1], should succeed.
        #. Try to set parameter[P1] with non date type, should fail.
        #. Try to set parameter[P1] with date type, should succeed.
        """
        self.log("Create schema with date parameter[P1], should succeed.")
        schema = """
        @url = test.schema
        date = (D)
        """
        schema = self.schema(schema)
        schema_obj = schema.new()

        self.log("Try to set parameter[P1] with non date type, should fail.")
        with self.assertRaises(Exception) as e:
            schema_obj.date = random.randint(1, 100) + 0.5
        
        with self.assertRaises(Exception) as e:
            schema_obj.date = self.random_string()

        with self.assertRaises(Exception) as e:
            date = '{:02}/31'.format(random.choice([2, 4, 6, 9, 11]))
            schema_obj.date = date
            self.assertEqual(schema_obj.date, date)
        
        with self.assertRaises(Exception) as e:
            date = '2014/02/29'
            schema_obj.date = date
            self.assertEqual(schema_obj.date, date)

        with self.assertRaises(Exception) as e:
            date = '201/02/29'
            schema_obj.date = date
            self.assertEqual(schema_obj.date, date)

        with self.assertRaises(Exception) as e:
            date = '2014/{}/29'.format(random.randint(1, 9))
            schema_obj.date = date
            self.assertEqual(schema_obj.date, date)

        with self.assertRaises(Exception) as e:
            date = '2014/02/{}'.format(random.randint(1, 9))
            schema_obj.date = date
            self.assertEqual(schema_obj.date, date)
        
        with self.assertRaises(Exception) as e:
            date = '2014/02/01 {}{}:12'.format(random.choice(random.randint(13, 23), 0), random.choice('am', 'pm'))
            schema_obj.date = date
            self.assertEqual(schema_obj.date, date)

        with self.assertRaises(Exception) as e:
            schema_obj.date = ["10", "20"]
        
        with self.assertRaises(Exception) as e:
            schema_obj.date = [10.5, 20.9]
        
        with self.assertRaises(Exception) as e:
            schema_obj.date = {'date': 10.7}

        self.log("Try to set parameter[P1] with date type, should succeed.")
        date = 0
        schema_obj.date = date
        self.assertEqual(schema_obj.date, date)

        date = random.randint(1, 200)
        schema_obj.date = date
        self.assertEqual(schema_obj.date, date)

        date = '{:02}/{:02}'.format(random.randint(1, 12), random.randint(1, 28))
        schema_obj.date = date
        self.assertEqual(schema_obj.date, date)

        date = '{:02}/{:02} {:02}:{:02}'.format(random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59))
        schema_obj.date = date + '4h'
        self.assertEqual(schema_obj.date, date)

        date = '{}/{:02}/{:02}'.format(random.randint(1, 2020), random.randint(1, 12), random.randint(1, 28))
        schema_obj.date = date
        self.assertEqual(schema_obj.date, date)

        date = '2016/02/29'
        schema_obj.date = date
        self.assertEqual(schema_obj.date, date)

        date = '{}/{:02}/{:02} {:02}:{:02}'.format(random.randint(1, 2020), random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59))
        schema_obj.date = date
        self.assertEqual(schema_obj.date, date)

        date = '{:02}/{:02}/{:02}'.format(random.randint(1, 99), random.randint(1, 12), random.randint(1, 28))
        schema_obj.date = date
        self.assertEqual(schema_obj.date, date)

        date = '{:02}/{:02}/{:02} {:02}:{:02}'.format(random.randint(1, 99), random.randint(1, 12), random.randint(1, 28), random.randint(0, 23), random.randint(0, 59))
        schema_obj.date = date 
        self.assertEqual(schema_obj.date, date)

        date = '{}/{:02}/{:02} {:02}{}:{:02}'.format(random.randint(1, 2020), random.randint(1, 12), random.randint(1, 28), random.randint(1, 12), random.choice('am', 'pm'), random.randint(0, 59))
        schema_obj.date = date
        self.assertEqual(schema_obj.date, date)

        date = '{:02}/{:02}/{}'.format(random.randint(1, 28), random.randint(1, 12), random.randint(1, 2020))
        schema_obj.date = date
        self.assertEqual(schema_obj.date, date)

    def test010_validate_percent_type(self):
        """
        SCM-010
        *Test case for validating percent type *

        **Test Scenario:**

        #. Create schema with percent parameter[P1], should succeed.
        #. Try to set parameter[P1] with non percent type, should fail.
        #. Try to set parameter[P1] with percent type, should succeed.
        """
        self.log("Create schema with percent parameter[P1], should succeed.")
        schema = """
        @url = test.schema
        percent = (percent)
        """
        schema = self.schema(schema)
        schema_obj = schema.new()

        self.log("Try to set parameter[P1] with non percent type, should fail.")
        with self.assertRaises(Exception) as e:
            schema_obj.percent = self.random_string()

        with self.assertRaises(Exception) as e:
            schema_obj.percent = ["10", "20"]
        
        with self.assertRaises(Exception) as e:
            schema_obj.percent = [10.5, 20.9]
        
        with self.assertRaises(Exception) as e:
            schema_obj.percent = {'number': 10.7}

        self.log("Try to set parameter[P1] with percent type, should succeed.")
        percent = random.randint(0, 250)
        schema_obj.percent = percent
        self.assertEqual(schema_obj.percent, percent)
        
        percent = random.randint(0, 250) + 0.5
        schema_obj.percent = percent
        self.assertEqual(schema_obj.percent, percent)

        percent = '{}'.format(random.randint(1, 100))
        schema_obj.percent = percent
        self.assertEqual(schema_obj.percent, percent)

        percent = '{}%'.format(random.randint(1, 100))
        schema_obj.percent = percent
        self.assertEqual(schema_obj.percent, percent)

        percent = '{}'.format(random.randint(1, 100) + 0.09)
        schema_obj.percent = percent
        self.assertEqual(schema_obj.percent, percent)

        percent = '{}%'.format(random.randint(1, 100) + 0.4)
        schema_obj.percent = percent
        self.assertEqual(schema_obj.percent, percent)

    def test011_validate_url_type(self):
        """
        SCM-011
        *Test case for validating url type *

        **Test Scenario:**

        #. Create schema with url parameter[P1], should succeed.
        #. Try to set parameter[P1] with non url type, should fail.
        #. Try to set parameter[P1] with url type, should succeed.
        """
        self.log("Create schema with url parameter[P1], should succeed.")
        schema = """
        @url = test.schema
        site = (u)
        """
        schema = self.schema(schema)
        schema_obj = schema.new()

        self.log("Try to set parameter[P1] with non url type, should fail.")
        with self.assertRaises(Exception) as e:
            schema_obj.site = random.randint(1, 100)

        with self.assertRaises(Exception) as e:
            schema_obj.site = random.randint(1, 100) + 0.5
        
        with self.assertRaises(Exception) as e:
            schema_obj.site = self.random_string()

        with self.assertRaises(Exception) as e:
            schema_obj.site = 'example.com'

        with self.assertRaises(Exception) as e:
            schema_obj.site = 'example@com'
        
        with self.assertRaises(Exception) as e:
            schema_obj.site = ["10", "20"]
        
        with self.assertRaises(Exception) as e:
            schema_obj.site = [10.5, 20.9]
        
        with self.assertRaises(Exception) as e:
            schema_obj.site = {'number': 10.7}

        self.log("Try to set parameter[P1] with url type, should succeed.")
        schema_obj.site = 'test.example.com'
        self.assertEqual(schema_obj.site, 'test.example.com')

    def test012_validate_numeric_type(self):
        """
        SCM-011
        *Test case for validating numeric type *

        **Test Scenario:**

        #. Create schema with numeric parameter[P1], should succeed.
        #. Try to set parameter[P1] with non numeric type, should fail.
        #. Try to set parameter[P1] with numeric type, should succeed.
        """
        self.log("Create schema with numeric parameter[P1], should succeed.")
        schema = """
        @url = test.schema
        name = (N)
        currency = (N)
        """
        schema = self.schema(schema)
        schema_obj = schema.new()

        self.log("Try to set parameter[P1] with non numeric type, should fail.")    
        with self.assertRaises(Exception) as e:
            schema_obj.currency = random.randint(1, 1000)

        with self.assertRaises(Exception) as e:
            schema_obj.currency = random.randint(1, 1000) + 0.004
        
        with self.assertRaises(Exception) as e:
            schema_obj.currency = ["10", "20"]
        
        with self.assertRaises(Exception) as e:
            schema_obj.currency = [10.5, 20.9]
        
        with self.assertRaises(Exception) as e:
            schema_obj.currency = {'number': 10.7}

        self.log("Try to set parameter[P1] with numeric type, should succeed.")
        name = self.random_string()
        schema_obj.name = name
        self.assertEqual(schema_obj.name, name)

        currencies = j.clients.currencylayer.cur2usd
        currency = '{} USD'.format(random.randint(1, 100))
        schema_obj.currency = currency
        self.assertEqual(schema_obj.currency, currency)
        for curr in currencies:
            self.assertEqual(schema_obj.currnecy_cur(curr), currency*currencies[curr])

    def test013_validate_currency_conversion(self):
        """
        SCM-011
        *Test case for validating numeric type *

        **Test Scenario:**

        #. Create schema with numeric parameter[P1], should succeed.
        #. Try to set parameter[P1] with non numeric type, should fail.
        #. Try to set parameter[P1] with numeric type, should succeed.
        """
        self.log("Create schema with numeric parameter[P1], should succeed.")
        schema = """
        @url = test.schema
        name = (N)
        currency = (N)
        """
        schema = self.schema(schema)
        schema_obj = schema.new()

        
    

    # @parameterized.expand(['S', 'I', 'F'])
    # def test002_create_schema(self, type_):
    #     """
    #     SCM-002
    #     """
    #     schema = """
    #     @url = test.schema
    #     var = ({})
    #     """.format(type_)
    #     self.schema_object = j.data.schema.get(schema_text_path=schema)
    #     import ipdb; ipdb.set_trace()
    #     print(type(self.schema_object.var))
        

