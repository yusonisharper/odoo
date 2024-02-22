{
    'name': "Car Clue",
    'version': '1.0',
    'depends': ['base'],
    'author': "Yusheng Wang",
    'category': 'Category',
    'description': """
    Identify interested vehicles.
    """,
    # data files always loaded at installation
    'data': [
        'views/vehicle_views.xml',
        'views/vehicle_list_menus.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        # 'demo/demo_data.xml',
    ],
    'application': True,
    'license': 'LGPL-3'
}