{
    'name': "Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "Yusheng Wang",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        # 'views/mymodule_view.xml',
        'security/ir.model.access.csv'
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'application': True,
}