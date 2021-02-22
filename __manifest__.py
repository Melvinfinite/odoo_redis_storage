# -*- coding: utf-8 -*-
{
    'name': "Redis Session Store",

    'summary': """
        This stores the session in redis""",

    'description': """
        This module stores the session on a redis (key value store) cluster to be able 
        to access the session objects from multiple instances.
    """,

    'author': "Melvin Hildebrandt",
    'website': "https://github.com/Melvinfinite",
    'category': 'Extra Tools',
    'version': '1.0.0',
    'depends': ['base',],
    'external_dependencies': {
      'python': ['redis'],
    },
    'installable': True,
    'application': True,
    'auto_install': True,
}