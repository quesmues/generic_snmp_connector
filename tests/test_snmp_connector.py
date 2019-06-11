import logging
from snmp_connector import SnmpConnector

logging.basicConfig(format='%(asctime)s\t%(levelname)s -- %(processName)s: '
                           '%(filename)s:%(lineno)s -- %(funcName)s -- %(message)s',
                    level=logging.INFO)

object_types = ['jmsDestinationRuntimeName', 'jmsDestinationRuntimeConsumersCurrentCount',
                'jmsDestinationRuntimeMessagesPendingCount']
conn = SnmpConnector(object_types=object_types, host='', port='',
                     mibs_name='BEA-WEBLOGIC-MIB', mibs_path='mib')
conn.execute()
list_values = conn.results()

print(list_values)
