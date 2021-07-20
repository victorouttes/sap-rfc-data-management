# SAP RFC data management

Lib to perform some SAP ERP modifications.

# Requirements

You need to install Cython before install this lib:
```
pip install Cython
```

# Install
```
pip install sap-rfc-data-management
```

# Usage
### Create PM notification:
```python
from sap_rfc_data_management.pm_notification import PMNotification

runner = PMNotification(
    host=SAP_HOST,
    service=SAP_SERVICE,
    group=SAP_GROUP,
    sysname=SAP_SYSNAME,
    client=SAP_CLIENT,
    lang=SAP_LANG,
    user=SAP_USER,
    password=SAP_PASSWORD
)
number = runner.create(
    title='notification title',
    notification_type='notification type',
    priority='notification priority',
    equipment='notification equipment number',
    reported_by='notification reported user (or some other text)',
    date_malfunction='malfunction datetime',
    maintenance_plant='notification plant',
    workcenter_id='notification workcenter'
)
print(number)  # created notification's number
```

### Change PM equipment ABC code:
```python
from sap_rfc_data_management.pm_equipment import PMEquipment

runner = PMEquipment(
    host=SAP_HOST,
    service=SAP_SERVICE,
    group=SAP_GROUP,
    sysname=SAP_SYSNAME,
    client=SAP_CLIENT,
    lang=SAP_LANG,
    user=SAP_USER,
    password=SAP_PASSWORD
)
runner.change(
    equipment='equipment number to be changed',
    abc_code='new abc code (1 character)'
)
```
