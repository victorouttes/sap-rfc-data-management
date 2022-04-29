from pyrfc import ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError

from sap_rfc_data_management.sap_generic import SAP
from .exceptions import SAPException, DefaultException

class PMRequisition(SAP):
      def create(self, items = None, items_account = None):
        try:
          connection = self.connection.get_connection()
          if items:
            create = connection.call(
              'BAPI_REQUISITION_CREATE',
               REQUISITION_ITEMS=items,
               REQUISITION_ACCOUNT_ASSIGNMENT=items_account
            )
            return_messages = create['RETURN']
            
            for message in return_messages:
                if message['TYPE'] == 'E':
                    raise SAPException
                
            connection.call('BAPI_TRANSACTION_COMMIT')

            requisition_number = create['NUMBER']
            return requisition_number
          else:
            raise DefaultException('Items must be filled.')

        except (ABAPApplicationError, ABAPRuntimeError, CommunicationError, LogonError):
                raise SAPException
    


