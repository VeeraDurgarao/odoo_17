{
    'name': 'Bank Management',
    'version': '1.0',
    'summary': 'Bank Management System',
    'depends': ['base', 'mail', 'sale', 'stock'],
    'data': ['security/ir.model.access.csv',
             'security/recycle_account_groups.xml',
             # 'security/recycle_account_record_rules.xml',
             'data/CusSeq.xml',
             'data/EmailTemplate.xml',
             'data/schedule_action.xml',
             'data/CustomerEmailTemplate.xml',
             'wizard/demo.xml',
             'wizard/print.xml',
             'wizard/xlReport.xml',
             # 'reports/bank.template.xml',
             'reports/sale.commision-qweb.xml',
             'reports/customerPDF.xml',
             'views/customer.xml',
             'views/employee.xml',
             'views/account.xml',
             'views/loan.xml',
             'views/menu_view.xml',
             'views/transaction1.xml',
             'views/query.xml',
             'views/sale_report.xml',
             'views/branch.xml',
             'views/kanbana.xml',
             'views/recycle.xml',
            'views/sale_order_commission_view.xml',
'views/sale_line_oreder_commission.xml',
             'views/sale_inheritate_menu.xml'



             ]

}
