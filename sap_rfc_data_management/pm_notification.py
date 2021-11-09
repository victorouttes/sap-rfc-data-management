import datetime

from pyrfc import ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError

from sap_rfc_data_management.sap_generic import SAP
from .exceptions import SAPException, DefaultException


class PMNotification(SAP):
    def create(self,
               notification_type: str,
               maintenance_plant: str,
               title: str,
               reported_by: str,
               priority: str,
               workcenter_id: str,
               date_malfunction: datetime.date = datetime.date.today(),
               equipment: str = None,
               functional_location: str = None,
               longtext: str = None):
        try:
            connection = self.connection.get_connection()
            if equipment:
                header = {
                    'EQUIPMENT': equipment.zfill(18),
                    'MAINTPLANT': maintenance_plant,
                    'SHORT_TEXT': title,
                    'REPORTEDBY': reported_by,
                    'NOTIF_DATE': datetime.date.today().strftime('%Y%m%d'),
                    'STRMLFNDATE': date_malfunction.strftime('%Y%m%d'),
                    'PRIORITY': priority,
                    'PM_WKCTR': workcenter_id
                }
            elif functional_location:
                header = {
                    'FUNCT_LOC': functional_location,
                    'MAINTPLANT': maintenance_plant,
                    'SHORT_TEXT': title,
                    'REPORTEDBY': reported_by,
                    'NOTIF_DATE': datetime.date.today().strftime('%Y%m%d'),
                    'STRMLFNDATE': date_malfunction.strftime('%Y%m%d'),
                    'PRIORITY': priority,
                    'PM_WKCTR': workcenter_id
                }
            else:
                raise DefaultException('Equipment or functional location must be filled.')
            if longtext:
                longtext_object = []
                splitted = [longtext[i:i+130] for i in range(0, len(longtext), 130)]
                for sp in splitted:
                    longtext_object.append(
                        {
                            'OBJTYPE': 'QMEL',
                            'TEXT_LINE': sp
                        }
                    )
                create = connection.call(
                    'BAPI_ALM_NOTIF_CREATE',
                    NOTIFHEADER=header,
                    LONGTEXTS=longtext_object,
                    NOTIF_TYPE=notification_type
                )
            else:
                create = connection.call(
                    'BAPI_ALM_NOTIF_CREATE',
                    NOTIFHEADER=header,
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
