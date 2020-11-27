# -*- coding: utf-8 -*-
{
    'name': "Redis Session Store",

    'summary': """
        This module is a module to store the session in redis""",

    'description': """
        This module stores the session on a redis (key value store) server to by able 
        to access the session objects from multiple instances.
    """,

    'author': "42 N.E.R.D.S.",
    'website': "https://www.42nerds.com",
    'category': 'Extra Tools',
    'version': '0.0.3',
    'depends': ['base',],
    'external_dependencies': {
      'python': ['redis'],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}