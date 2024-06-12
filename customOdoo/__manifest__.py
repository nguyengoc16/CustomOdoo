# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Hospital Management',
    'version' : '1.2',
    'summary': 'Hospital Management Software',
    'sequence': -100,
    'description': """ Hospital Management Software """,
    'author':'ngocdeptrai',
    'category': 'Productivity',
    'website': 'https://www.odoo.com/app/invoicing',
    'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends' : [
        'sale',
        'mail',
        'web',
        'report_xlsx',
    ],
    'data': [

        'security/ir.model.access.csv',

        'data/data.xml',

        'wizard/create_appointment_views.xml',
        'wizard/search_appointment_view.xml',
        'wizard/report_appointment_view.xml',
        'wizard/report_all_patients_views.xml',



        'views/patient_views.xml',
        'views/patient_gender_views.xml',
        'views/kid_views.xml',
        'views/doctor_view.xml',
        'views/sale_views.xml',
        'views/appointment_views.xml',
        'views/department_views.xml',
        'views/medicine_views.xml',
        'views/tax_views.xml',
        'views/res_config_settings_views.xml',
        'views/menu.xml',

        'report/report.xml',
        'report/patient_card.xml',
        'report/appointment_with_medicine_card.xml',
        'report/patient_details_template.xml',
        'report/report_appointment_details.xml',
        'report/report_all_patients_template.xml',



    ],
    'assets': {
       'web.assets_backend': [
           'om_hospital/static/src/css/custom_styles.css',
       ]
    },


    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
