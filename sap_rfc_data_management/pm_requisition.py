from pyrfc import ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError

from sap_rfc_data_management.sap_generic import SAP
from .exceptions import SAPException, DefaultException

class PMRequisition(SAP):
      def get(self, req_number):
        try:
            connection = self.connection.get_connection()
            response = connection.call(
                  'BAPI_REQUISITION_GETDETAIL',
                   NUMBER=req_number
                )
            
            return_messages = response['RETURN']
            
            for message in return_messages:
                if message['TYPE'] == 'E':
                    raise SAPException
       
            return response
        except (ABAPApplicationError, ABAPRuntimeError, CommunicationError, LogonError):
                raise SAPException


      def create(self, items = None, items_account = None):
        try:
          connection = self.connection.get_connection()
          if items:
            for index, item in enumerate(items):
                item_acctasscat = item['ACCTASSCAT']
                if item_acctasscat == 'P' and not 'WBS_ELEM_E' in items_account[index]:
                    raise DefaultException('WBS_ELEM_E must be filled.')
                if item_acctasscat == 'K' and not 'COST_CTR' in items_account[index]:
                    raise DefaultException('COST_CTR must be filled.')
                if item_acctasscat == 'F' and not 'ORDER_NO' in items_account[index]:
                    raise DefaultException('ORDER_NO must be filled.')
                        
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
    


