import datetime

from pyrfc import ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError

from sap_rfc_data_management.sap_generic import SAP
from .exceptions import SAPException


class PMNotification(SAP):
    def create(self,
               notification_type: str,
               equipment: str,
               maintenance_plant: str,
               title: str,
               reported_by: str,
               priority: str,
               workcenter_id: str,
               date_malfunction: datetime.date):
        try:
            connection = self.connection.get_connection()
            create = connection.call(
                'BAPI_ALM_NOTIF_CREATE',
                NOTIFHEADER={
                    'EQUIPMENT': equipment.zfill(18),
                    'MAINTPLANT': maintenance_plant,
                    'SHORT_TEXT': title,
                    'REPORTEDBY': reported_by,
                    'NOTIF_DATE': datetime.date.today().strftime('%Y%m%d'),
                    'STRMLFNDATE': date_malfunction.strftime('%Y%m%d'),
                    'PRIORITY': priority,
                    'PM_WKCTR': workcenter_id
                },
                NOTIF_TYPE=notification_type
            )

            return_messages = create['RETURN']
            if return_messages:
                raise SAPException

            temporary_code = create['NOTIFHEADER_EXPORT']['NOTIF_NO']
            save = connection.call(
                'BAPI_ALM_NOTIF_SAVE',
                NUMBER=temporary_code
            )
            notification_number = save['NOTIFHEADER']['NOTIF_NO']

            return_messages = save['RETURN']
            if return_messages:
                raise SAPException

            connection.call('BAPI_TRANSACTION_COMMIT')
            return str(int(notification_number))
        except (ABAPApplicationError, ABAPRuntimeError, CommunicationError, LogonError):
            raise SAPException
