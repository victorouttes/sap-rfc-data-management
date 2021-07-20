from .connection import SAPConnection
from .exceptions import SAPException
from pyrfc import ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError


class PMEquipment:
    def __init__(self,
                 host: str,
                 service: str,
                 group: str,
                 sysname: str,
                 client: str,
                 lang: str,
                 user: str,
                 password: str):
        self.connection = SAPConnection(
            host=host,
            service=service,
            group=group,
            sysname=sysname,
            client=client,
            lang=lang,
            user=user,
            password=password
        )

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
