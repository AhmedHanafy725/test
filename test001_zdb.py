from framework.base.vdisk import Vdisk
from framework.base.zdb import ZDB
from framework.base.vms import VM
from testcases.base_test import BaseTest
from nose_parameterized import parameterized
import multiprocessing
import time
import unittest
import requests
import random
import subprocess
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
        

    def read_write_file(self, mount_path, guest_port, vm_zt_ip, i, result_dict):
        self.log("Download specific file with size 10M to vm[VM1].")
        file_name = self.random_string()
        cmd = 'cd {}; wget https://github.com/AhmedHanafy725/test/raw/master/test_file -O {}'.format(mount_path, file_name)
        self.ssh_vm_execute_command(vm_ip=vm_zt_ip, cmd=cmd)

        self.log("Get file md5 of the downloaded file.")
        cmd = 'cd {}; md5sum {}'.format(mount_path, file_name)
        result1 = self.ssh_vm_execute_command(vm_ip=vm_zt_ip, cmd=cmd)
        result1 = result1[:result1.find(' ')]

        self.log("Download this file from [VM1] to the test machine through the server[S1].")
        cmd = 'wget http://{}:{}/{}'.format(vm_zt_ip, guest_port, file_name)
        response = subprocess.run(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertFalse(response.returncode)

        self.log("Get file md5 of the downloaded file.")
        cmd = 'md5sum {}'.format(file_name)
        response = subprocess.run(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result2 = response.stdout.strip()
        result2 = result2[:result2.find(' ')]

        self.log("remove downloaded files")
        cmd = 'rm -f  {}'.format(file_name)
        response = subprocess.run(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertFalse(response.returncode)

        result_dict[i] = (result1, result2)

    @parameterized.expand(["btrfs", "ext4", "ext3", "ext2"])
    def test001_fill_disk_with_1T(self, filesystem):
        """ SAL-040 create vdisk and attach it to vm.

        **Test Scenario:**

        #. Create disk [D1] with default data and size 1000G.
        #. Create vm [VM1] with default values, should succeed.
        #. Add zerotier network to VM1, should succeed.
        #. Attach disk [D1] to vm [VM1].
        #. deploy vm [VM1].
        #. fill the disk with one tera byte.

        """
        self.log("Create zdb with default values.")
        zdb_name = self.random_string()
        zdb = self.zdb(node=self.node_sal)
        zdb.data = self.set_zdb_default_data(name=zdb_name)
        zdb.install()
        self.zdbs.append(zdb)
        
        self.log("Create disk [D1] with default data and size 1000G")
        disk = Vdisk(node=self.node_sal, zdb=zdb.zerodb_sal)
        disk.data = self.set_vdisk_default_data()
        mount_path = '/mnt/{}'.format(self.random_string())
        disk.data['mountPoint'] = mount_path
        disk.data['filesystem'] = filesystem
        if disk.data['max_size'] < 1000 :
            self.skipTest("Can't run this test on less than one tera byte disk")
        disk.data['size'] = 1000
        disk.install()

        self.log("Create vm [VM1] with default values, should succeed.")
        vm = self.vm(node=self.node_sal)
        vm.data = self.set_vm_default_values(os_type="ubuntu")
        vm.generate_vm_sal()

        self.log(" Add zerotier network to VM1, should succeed.")
        vm.add_zerotier_nics(network=self.zt_network)
        
        self.log("Attach disk [D1] to vm [VM1].")
        vm.add_disk(disk.disk)
        
        self.log("deploy vm [VM1].")
        vm.install()
        self.vms.append(vm.info()['uuid'])

        self.log("get ztIdentity and vm ip")
        ztIdentity = vm.data["ztIdentity"]
        vm_zt_ip = self.get_zerotier_ip(ztIdentity)

        for _ in range(100):
            file_name = self.random_string()
            cmd =  'cd {}; \
                    dd if=/dev/zero of={} count=1024 bs=10485760; \
                    echo test >> {}'.format(mount_path, file_name, file_name)
            self.ssh_vm_execute_command(vm_ip=vm_zt_ip, cmd=cmd)

    def test002_read_and_write_file_from_vdisk(self):
        """ SAL-041 create vdisk and attach it to vm.

        **Test Scenario:**

        #. Create zdb with default data.
        #. Create disk [D1] with default data.
        #. Create vm [VM1] with default values, should succeed.
        #. Add zerotier network to VM1, should succeed.
        #. Attach disk [D1] to vm [VM1].
        #. Add port to create server on it.
        #. Create server[S1], should succeed.
        #. Do this steps five times using multiprocessing:
            #. Download specific file with size 10M to vm[VM1].
            #. Get file md5 of the downloaded file.
            #. Download this file from [VM1] to the test machine through the server[S1].
            #. Get file md5 of the downloaded file.
        #. Download the same to the test machine.
        #. Check md5 of the those three files, should be the same.

        """
        self.log("Create zdb with default values.")
        zdb_name = self.random_string()
        zdb = self.zdb(node=self.node_sal)
        zdb.data = self.set_zdb_default_data(name=zdb_name)
        zdb.install()
        self.zdbs.append(zdb)
        
        self.log("Create disk [D1] with default data")
        disk = Vdisk(node=self.node_sal, zdb=zdb.zerodb_sal)
        disk.data = self.set_vdisk_default_data()
        mount_path = '/mnt/{}'.format(self.random_string())
        disk.data['mountPoint'] = mount_path
        disk.data['filesystem'] = 'ext4'
        disk.install()

        self.log("Create vm [VM1] with default values, should succeed.")
        vm = self.vm(node=self.node_sal)
        vm.data = self.set_vm_default_values(os_type="ubuntu")

        self.log("Update default data by adding type default nics")
        network_name = self.random_string()
        nics = {'nics': [{'name': network_name, 'type': 'default'}]}  
        vm.data = self.update_default_data(vm.data, nics)
        vm.generate_vm_sal()

        self.log("Add port to create server on it.")
        port_name = self.random_string()   
        host_port = random.randint(3000, 4000)
        guest_port = random.randint(5000, 6000)
        vm.add_port(name=port_name, source=host_port, target=guest_port)

        self.log(" Add zerotier network to VM1, should succeed.")
        vm.add_zerotier_nics(network=self.zt_network)
        
        self.log("Attach disk [D1] to vm [VM1].")
        vm.add_disk(disk.disk)

        self.log("deploy vm [VM1].")
        vm.install()
        self.vms.append(vm.info()['uuid'])
        
        self.log("get ztIdentity and vm ip")
        ztIdentity = vm.data["ztIdentity"]
        vm_zt_ip = self.get_zerotier_ip(ztIdentity)

        self.log("create server on the vm at port {}.".format(guest_port))
        cmd = 'cd {}; python3 -m http.server {} &> /tmp/server.log &'.format(disk.data['mountPoint'], guest_port)
        self.ssh_vm_execute_command(vm_ip=vm_zt_ip, cmd=cmd)
        time.sleep(10)
        
        self.log("Create dict to get data from multiprocess")
        manager = multiprocessing.Manager()
        result_dict = manager.dict()
        jobs = []
        for i in range(5):
            p = multiprocessing.Process(target=self.read_write_file, args=(mount_path, guest_port, vm_zt_ip, i, result_dict))
            jobs.append(p)
            p.start()

        self.log("wait till all processes finish")
        for proc in jobs:
            proc.join()
        
        self.log("Download the same to the test machine.")
        file_name2 = self.random_string()
        cmd = 'wget https://github.com/AhmedHanafy725/test/raw/master/test_file -O {}'.format(file_name2)
        response = subprocess.run(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertFalse(response.returncode)

        cmd = 'md5sum {}'.format(file_name2)
        response = subprocess.run(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = response.stdout.strip()
        result = result[:result.find(' ')]
        
        self.log("remove downoaded file")
        cmd = 'rm -f {}'.format(file_name2)
        response = subprocess.run(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertFalse(response.returncode)

        self.log("Check md5 of the those three files, should be the same")
        for i in range(5):
            self.assertEqual(result_dict[i][0], result)
            self.assertEqual(result_dict[i][1], result)
        
    def test003_attach_number_of_disks_to_vm(self):
        """ SAL-026 create vdisk and attach it to vm.

        **Test Scenario:**

        #. Create disk [D1] with default data.
        #. Create vm [VM1] with default values, should succeed.
        #. Add zerotier network to VM1, should succeed.
        #. Attach disk [D1] to vm [VM1].
        #. deploy vm [VM1].
        #. Check that disk [D1] is attached to vm [VM1], should succeed.
        #. (delete namespace/stop zdb).
        #. uninstall the vm, should fail.
        """
        self.log("Create zdb with default values.")
        zdb_name = self.random_string()
        zdb = self.zdb(node=self.node_sal)
        zdb.data = self.set_zdb_default_data(name=zdb_name)
        zdb.install()
        self.zdbs.append(zdb)

        self.log("Create vm [VM1] with default values, should succeed.")
        vm = self.vm(node=self.node_sal)
        vm.data = self.set_vm_default_values(os_type="ubuntu")
        vm.generate_vm_sal()
        
        self.log(" Add zerotier network to VM1, should succeed.")
        vm.add_zerotier_nics(network=self.zt_network)
        vm.memory = 7168

        for _ in range(1):
            self.log("Create disk [D1] with default data")
            disk = Vdisk(node=self.node_sal, zdb=zdb.zerodb_sal)
            disk.data = self.set_vdisk_default_data()
            mount_path = '/mnt/{}'.format(self.random_string())
            disk.data['mountPoint'] = mount_path
            disk.data['filesystem'] = 'ext4'
            disk.install()

            self.log("Attach disk [D1] to vm [VM1].")
            vm.add_disk(disk.disk)

        self.log("deploy vm [VM1].")
        import ipdb; ipdb.set_trace()
        vm.install()

        self.log("get ztIdentity and vm ip")
        ztIdentity = vm.data["ztIdentity"]
        vm_zt_ip = self.get_zerotier_ip(ztIdentity)

        self.vms.append(vm.info()['uuid'])
        

    @parameterized.expand(['namespace', 'zdb'])    
    def test004_delete_namespace_or_zdb_of_vdisk(self, delete):
        """ SAL-026 create vdisk and attach it to vm.

        **Test Scenario:**

        #. Create disk [D1] with default data.
        #. Create vm [VM1] with default values, should succeed.
        #. Add zerotier network to VM1, should succeed.
        #. Attach disk [D1] to vm [VM1].
        #. Try to write on disk mounting point, should succeed.
        #. Delete (namespace/zdb) and try to write again, should fail.
        """
        self.log("Create zdb with default values.")
        zdb_name = self.random_string()
        zdb = self.zdb(node=self.node_sal)
        zdb.data = self.set_zdb_default_data(name=zdb_name)
        zdb.install()
        self.zdbs.append(zdb)
        

        self.log("Create disk [D1] with default data")
        disk = Vdisk(node=self.node_sal, zdb=zdb.zerodb_sal)
        disk.data = self.set_vdisk_default_data()
        mount_path = '/mnt/{}'.format(self.random_string())
        disk.data['mountPoint'] = mount_path
        disk.data['filesystem'] = 'ext4'
        disk.install()

        self.log("Create vm [VM1] with default values, should succeed.")
        vm = self.vm(node=self.node_sal)
        vm.data = self.set_vm_default_values(os_type="ubuntu")
        vm.generate_vm_sal()

        self.log(" Add zerotier network to VM1, should succeed.")
        vm.add_zerotier_nics(network=self.zt_network)
        
        self.log("Attach disk [D1] to vm [VM1].")
        vm.add_disk(disk.disk)

        self.log("deploy vm [VM1].")
        vm.install()
        self.vms.append(vm.info()['uuid'])
        ztIdentity = vm.data["ztIdentity"]
        vm_zt_ip = self.get_zerotier_ip(ztIdentity)
        
        self.log("Try to write on disk mounting point, should succeed.")
        cmd = 'echo {} > {}/{}'.format(self.random_string(), mount_path, self.random_string())
        result = self.ssh_vm_execute_command(vm_ip=vm_zt_ip, cmd=cmd)

        self.log("Delete (namespace/zdb) and try to write again, should fail.")
        if delete == 'zdb':
            zdb.stop()
        else:
            zdb.namespace_delete(disk.data['name'])

        cmd = 'echo {} > {}/{}'.format(self.random_string(), mount_path, self.random_string())
        result = self.execute_command(ip=vm_zt_ip, cmd=cmd)
        self.assertTrue(result.returncode)
