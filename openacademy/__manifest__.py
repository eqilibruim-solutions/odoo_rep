{
    'name': "openacademy",
    'sequence': -100,

    'description': """
        Module for coureses managment by belk1ng
    """,

    'author': "belk1ng",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': [
        'base'
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/groups.xml'
    ],
    'application': True,
    'installable': True,
}
