from framework.base.vdisk import Vdisk
from framework.base.zdb import ZDB
from framework.base.vms import VM
from testcases.base_test import BaseTest
from nose_parameterized import parameterized
import time
import unittest
import requests
import random

class Vdisktest(BaseTest):

    @classmethod
    def setUpClass(cls):
        self = cls()
        super().setUpClass()

    def setUp(self):
        super().setUp()
    
    def tearDown(self):
        self.log('tear down vms')
        for uuid in self.vms:
            self.node_sal.client.kvm.destroy(uuid)
        self.vms.clear()

        self.log('tear down zdbs')
        for zdb in self.zdbs:
            namespaces = zdb.namespace_list()
            for namespace in namespaces:
                zdb.namespace_delete(namespace.name)
            self.node_sal.client.container.terminate(zdb.zerodb_sal.container.id)
        self.zdbs.clear()

    def test001_attach_vdisk_to_vm(self):
        """ SAL-026 create vdisk and attach it to vm.
        **Test Scenario:**
        #. Create zdb with default data.
        #. Create disk [D1] with default data.
        #. Create vm [VM1] with default values, should succeed.
        #. Add zerotier network to VM1, should succeed.
        #. Attach disk [D1] to vm [VM1].
        #. add port to create server on it.
        #. deploy vm [VM1].
        #. Check that disk [D1] is attached to vm [VM1], should succeed.
        #. Try to ssh [VM1], should succeed.
        #. create server.
        #. create file with specific size 10M.
        #. get file md5 of the created file.
        #. upload this file to the mount point on [VM1].
        #. check md5 of the uploaded file, should succeed.
        #. download it again and check md5, should succeed.
        
        """
        pass

        

    def test001_attach_vdisk_to_vm(self):
        """ SAL-026 create vdisk and attach it to vm.
        **Test Scenario:**
        #. Create zdb with default data.
        #. Create disk [D1] with default data.
        #. Create vm [VM1] with default values, should succeed.
        #. Add zerotier network to VM1, should succeed.
        #. Attach 10 disk to vm [VM1].
        #. deploy vm [VM1].
        #. if it succeed, use double number till it fail  
        