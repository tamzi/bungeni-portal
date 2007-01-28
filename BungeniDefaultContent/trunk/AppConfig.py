# We add default content for the Bungeni product.
DEPENDENCIES = ['Bungeni', ]

DEFAULT_SITE_CONTENT = (
        {'id': 'business', 'title': 'Business', 'type': 'Folder', 
        'children': (
            {'id': 'index_html', 'title': 'Business', 'type': 'Document',
            'text': 'Documents about parliamentary business', 
            'children': ()},
            {'id': 'chamber', 'title': 'Chamber', 'type': 'Folder', 'children': (
                {'title': 'Business Bulletin', 'type': '«»', 'children': ()}, 
                {'title': 'Debate Report', 'type': '«»', 'children': ()}, 
                {'title': 'Minutes of Proceedings', 'type': '«»', 'children': ()}, 
                {'title': 'Tabled Documents', 'type': '«»', 'children': ()}, 
                {'title': 'Voting Records', 'type': '«»', 'children': ()}, 
                {'title': 'Attendance List', 'type': '«»', 'children': ()}, 
                ),},
            {'id': 'committees', 'title': 'Committees', 'type': 'Topic',  # TODO add criteria for smart folder to select committees
            'children': (),},
            {'id': 'bills', 'title': 'Bills', 'type': '«»', 'children': (),},
            {'id': 'motions', 'title': 'Motions', 'type': '«»', 'children': (),},
            {'id': 'questions', 'title': 'Questions', 'type': '«»', 'children': (),},
            {'id': 'events', 'title': 'Events', 'type': '«»', 'children': (),},
            ),
        },
        {'id': 'people', 'type': 'Folder', 'children': (
            {'id': 'index_html', 'type': 'Document', 
            'text': 'Lists the MPs and staff. Use RichTopic?',
            'children': ()},
            )
        },
        {'id': 'about', 'type': 'Folder', 'children': (
            {'id': 'index_html', 'type': 'Document', 
            'text': 'Background information about the parliament',
            'children': (
                {'title': 'How it works', 'type': '«»', 'children': (
                    {'title': 'Parliamentary Procedure', 'type': 'Document', 'children': ()}, 
                    {'title': 'Standing Orders', 'type': 'Document', 'children': ()}, 
                    {'title': 'The Legislative Process', 'type': 'Document', 'children': ()}, 
                    {'title': 'Oversight', 'type': 'Document', 'children': ()}, 
                    {'title': 'Guides', 'type': 'Document', 'children': ()}, 
                    {'title': 'Guide on Public Bills', 'type': 'Document', 'children': ()}, 
                    {'title': 'Guide on Private Bills', 'type': 'Document', 'children': ()}, 
                    {'title': 'Guide for Motions', 'type': 'Document', 'children': ()}, 
                    {'title': 'Guide for Parliamentary Questions', 'type': 'Document', 'children': ()}, 
                    {'title': 'Guide for Committee Conveners', 'type': 'Document', 'children': ()}, 
                    {'title': 'Guide on Committees', 'type': 'Document', 'children': ()}, 
                    )}, 
                {'title': 'History', 'type': '«»', 'children': ()}, 
                {'title': 'How to visit it', 'type': '«»', 'children': ()}, 
                {'title': 'How to participate', 'type': '«»', 'children': ()}, 
                {'title': 'Learning resources', 'type': '«»', 'children': ()}, 
                {'title': 'Pictures', 'type': '«»', 'children': ()}, 
                )},
            )
        },
        {'id': 'publications', 'type': 'Folder', 'children': (
            {'id': 'index_html', 'type': 'Document', 
            'text': 'Publications include legislation and hansard.',
            'children': ()},
            )
        },
        {'id': 'organisation', 'type': 'Folder', 'children': (
            {'id': 'index_html', 'type': 'Document', 
            'text': 'The parliament is structured as follows ...',
            'children': ()},
            )
        },
        )
