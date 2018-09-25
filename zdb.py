from jumpscale import j
import copy
from termcolor import colored



class ZDB:

    def __init__(self, node, guid=None, data=None):
        self.guid = guid 
        self.data = data
        self.node_sal = node
        self.zdb = None

    @property
    def _zerodb_sal(self):
        data = self.data.copy()
        self.zdb = self.node_sal.primitives.from_dict('zerodb', data)

    def _deploy(self):
        self.zdb.deploy()
        self.data['nodePort'] = self.zdb.node_port
        self.data['ztIdentity'] = self.zdb.zt_identity

    def install(self):
        print(colored('Installing zerodb %s' % self.data['name'], 'white'))
        self._deploy()

    def start(self):
        """
        start zerodb server
        """
        print(colored('Starting zerodb %s' % self.data['name'], 'white'))
        self.start()

    def stop(self):
        """
        stop zerodb server
        """
        print(colored('Stopping zerodb %s' % self.data['name'], 'white'))
        self.zdb.stop()

    def upgrade(self):
        """
        upgrade 0-db
        """
        self.stop()
        self.start()

    def info(self):
        """
        Return disk information
        """
        return self.zdb.info

    def namespace_list(self):
        """
        List namespace
        :return: list of namespaces ex: ['namespace1', 'namespace2']
        """
        return self.zdb.namespaces

    def namespace_info(self, namespace):
        """
        Get info of namespace
        :param name: namespace name
        :return: dict
        """
        return namespace.info().to_dict()

    def namespace_url(self, namespace):
        """
        Get url of the namespace
        :param name: namespace name
        :return: dict
        """
        
        return namespace.url

    def namespace_private_url(self, namespace):
        """
        Get private url of the namespace
        :param name: namespace name
        :return: dict
        """       
        return namespace.private_url

    def namespace_create(self, name, size=None, password=None, public=True):
        """
        Create a namespace and set the size and secret
        :param name: namespace name
        :param size: namespace size
        :param password: namespace password
        :param public: namespace public status
        """
        print(colored("create namespace %s"%name, 'white'))
        namespace = self.zdb.namespace.add(name=name, size=size, password=password, public=public)
        self._deploy()
        return namespace

    def namespace_set(self, namespace, prop, value):
        """
        Set a property of a namespace
        :param name: namespace name
        :param prop: property name
        :param value: property value
        """
        namespace.set_property(prop, value)

    def namespace_delete(self, namespace):
        """
        Delete a namespace
        """
        self.zdb.namespace.remove(namespace.name)
        self._deploy()

    def connection_info(self):
        return {
            'ip': self.node_sal.public_addr,
            'port': self.data['nodePort']
        }