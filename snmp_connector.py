from pysnmp.hlapi import asyncore
from pysnmp.hlapi.varbinds import CommandGeneratorVarBinds

class SnmpConnector:

    """Generic Implementation of pysnmp for easy execution

    Usage::

         from snmp_connector import SnmpConnector
         object_types = [object_type, ...]
         conn = SnmpConnector(object_types=object_types, host='', port='', mibs_name='', mibs_path='')
         conn.execute()
         list_values = conn.results()

    :param object_types: list of objects types to search in mib file
    :param host: host of the snmp service
    :param port: port of the snmp service
    :param mibs_name: name of the mib
    :param mibs_path: path of the mib file

    :return a list of the return values for object_types
    """

    def __init__(self, object_types=[], host='', port='', mibs_name='', mibs_path=''):
        self.object_types = object_types
        self.host = host
        self.port = port
        self.mibs_name = mibs_name
        self.mibs_path = mibs_path
        self.__object_identities = []
        self.__list_results = []

    def cb_fun(self, snmp_engine, send_request_handle, error_indication, error_status, error_index, bind_table, cb_ctx):
        if error_indication:
            return False
        elif error_status:
            return False
        else:
            for row in bind_table:
                temp = []
                for c, col in enumerate(row):
                    if not self.object_identities[c].isPrefixOf(col[0]):
                        return False
                    temp.append([x.prettyPrint() for x in col][-1])
                self.list_results.append(temp)
        return True

    def execute(self):
        try:
            snmp_engine = asyncore.SnmpEngine()
            vbproc = CommandGeneratorVarBinds()
            self.object_identities = [
                x[0] for x in vbproc.makeVarBinds(snmp_engine, self.construct_object_types(
                    self.object_types, self.mibs_name, self.mibs_path))
            ]
            asyncore.nextCmd(snmp_engine,
                             asyncore.CommunityData('public', mpModel=1),
                             asyncore.UdpTransportTarget((self.host, self.port)),
                             asyncore.ContextData(), *self.construct_object_types(self.object_types,
                                                                                  self.mibs_name, self.mibs_path),
                             cbFun=self.cb_fun,
                             lookupMib=False)
            snmp_engine.transportDispatcher.runDispatcher()
        except Exception as error:
            raise error

    def results(self):
        if self.list_results:
            return self.list_results
        else:
            raise ValueError("Execute the execute() method before call results")

    @staticmethod
    def construct_object_types(list_of_oids, mibs_name, mibs_path):
        object_types = []
        for oid in list_of_oids:
            object_types.append(asyncore.ObjectType(asyncore.ObjectIdentity(mibs_name, oid)).addMibSource(mibs_path))
        return object_types

    @property
    def list_results(self):
        return self.__list_results

    @list_results.setter
    def list_results(self, list_results):
        self.__list_results = list_results

    @property
    def object_identities(self):
        return self.__object_identities

    @object_identities.setter
    def object_identities(self, object_identities):
        self.__object_identities = object_identities



