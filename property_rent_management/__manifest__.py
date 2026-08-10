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
    'maintainer': 'a.osman@bab.com.sa',
    'support': 'abdzoro89@gmail.com',
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
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
