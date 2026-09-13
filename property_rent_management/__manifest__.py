{
    'name': 'Rent Property Management',
    'version': '19.0.1.0.0',
    'summary': 'Complete property, owner, renter, contract, payment and maintenance management | إدارة العقارات الإيجارية',
    'description': """
Rent Property Management | إدارة العقارات الإيجارية
====================================================
Manage your rental properties end-to-end:

* Properties with status tracking (available / rented / maintenance)
* Owner & renter profiles
* Rental contracts with full lifecycle (draft → active → expired)
* Payment scheduling and tracking (pending / paid / late)
* Maintenance requests workflow
* Mobile API keys and integration logs
* Operational dashboard with KPI counters

---

إدارة العقارات الإيجارية بشكل متكامل:

* تتبع العقارات حسب الحالة (متاح / مؤجر / تحت الصيانة)
* ملفات الملاك والمستأجرين
* عقود إيجار كاملة (مسودة → نشط → منتهٍ)
* جدولة المدفوعات وتتبعها (معلق / مدفوع / متأخر)
* سير عمل طلبات الصيانة
* مفاتيح API وسجلات التكامل للموبايل
* لوحة تحكم تشغيلية مع مؤشرات الأداء
    """,
    'category': 'Real Estate',
    'author': 'leapai.ai',
    'website': 'https://leapai.ai',
    'maintainer': 'Abdulkaraim Osman',
    'support': 'sales@leapai.ai',
    'depends': ['contacts', 'mail', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/property_property_views.xml',
        'views/property_owner_views.xml',
        'views/property_renter_views.xml',
        'views/property_contract_views.xml',
        'views/property_payment_views.xml',
        'views/property_maintenance_views.xml',
        'views/property_api_key_views.xml',
        'views/property_api_log_views.xml',
        'views/dashboard_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'images': [
        'static/description/main_screenshot.png',
        'static/description/screen_00_home.png',
        'static/description/screen_03_properties_kanban.png',
        'static/description/screen_05_owners.png',
        'static/description/screen_07_contracts_list.png',
        'static/description/screen_08_contract_form.png',
        'static/description/screen_09_payments.png',
        'static/description/screen_10_maintenance_kanban.png',
        'static/description/screen_11_api_keys.png',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
