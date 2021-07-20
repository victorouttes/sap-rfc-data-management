from pyrfc import ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError

from sap_rfc_data_management.sap_generic import SAP
from .exceptions import SAPException


class PMEquipment(SAP):
    def change(self,
               equipment: str,
               abc_code: str):
        try:
            equipment = equipment.zfill(18)
            connection = self.connection.get_connection()
            change = connection.call(
                'BAPI_EQUI_CHANGE',
                EQUIPMENT=equipment,
                DATA_GENERAL={
                    'ABCINDIC': abc_code.upper()
                },
                DATA_GENERALX={
                    'ABCINDIC': 'X',
                },
                DATA_SPECIFIC={},
                DATA_SPECIFICX={},
            )

            return_messages = change['RETURN']
            if return_messages['TYPE'] == 'E':
                raise SAPException

            connection.call('BAPI_TRANSACTION_COMMIT')
        except (ABAPApplicationError, ABAPRuntimeError, CommunicationError, LogonError):
            raise SAPException
