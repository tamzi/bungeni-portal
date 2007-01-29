# We add default content for the Bungeni product.
DEPENDENCIES = ['Bungeni', ]

DEFAULT_SITE_CONTENT = (
        {'id': 'business', 'title': 'Business', 'type': 'Folder', 'children': (
            {'id': 'index_html', 'title': 'Business', 'type': 'Document',
            'text': 'Documents about parliamentary business', },
            {'title': 'Chamber', 'type': 'Folder', 'children': (
                {'title': 'Business Bulletin', 'type': '«»', 'children': ()}, 
                {'title': 'Debate Report', 'type': '«»', 'children': ()}, 
                {'title': 'Minutes of Proceedings', 'type': '«»', 'children': ()}, 
                {'title': 'Tabled Documents', 'type': '«»', 'children': ()}, 
                {'title': 'Voting Records', 'type': '«»', 'children': ()}, 
                {'title': 'Attendance List', 'type': '«»', 'children': ()}, 
                ),},
            {'title': 'Committees', 'type': 'Topic',  # TODO add criteria for smart folder to select committees
            'children': (),},
            {'title': 'Bills', 'type': '«»', 'children': (),},
            {'title': 'Motions', 'type': '«»', 'children': (),},
            {'title': 'Questions', 'type': '«»', 'children': (),},
            {'title': 'Events', 'type': '«»', 'children': (),},
            ),
        },
        {'id': 'people', 'type': 'Folder', 'children': (
            {'id': 'index_html', 'type': 'Document', 
            'text': 'Lists the MPs and staff. Use RichTopic?', },
            )
        },
        {'id': 'about', 'type': 'Folder', 'children': (
            {'id': 'index_html', 'type': 'Document', 
            'text': 'Background information about the parliament',},
            {'title': 'How it works', 'type': 'Folder', 'children': (
                {'id': 'index_html', 'title': 'How it works', 'type': 'Dynamic Page'},
                {'title': 'Parliamentary Procedure', 'type': 'Document'}, 
                {'title': 'Standing Orders', 'type': 'Document'}, 
                {'title': 'The Legislative Process', 'type': 'Document'}, 
                {'title': 'Oversight', 'type': 'Document'}, 
                {'title': 'Guides', 'type': 'LongDocument', 'children': (
                    {'title': 'Guide on Public Bills', 'type': 'LongDocumentPage'}, 
                    {'title': 'Guide on Private Bills', 'type': 'LongDocumentPage'}, 
                    {'title': 'Guide for Motions', 'type': 'LongDocumentPage'}, 
                    {'title': 'Guide for Parliamentary Questions', 'type': 'LongDocumentPage'}, 
                    {'title': 'Guide for Committee Conveners', 'type': 'LongDocumentPage'}, 
                    {'title': 'Guide on Committees', 'type': 'LongDocumentPage'}, 
                    )}, 
                )}, 
            {'title': 'History', 'type': 'Document'}, 
            {'title': 'How to visit', 'type': 'Document'}, 
            {'title': 'How to participate', 'type': 'Document'}, 
            {'title': 'Learning resources', 'type': 'Document'}, 
            {'title': 'Pictures', 'type': 'Folder', 'layout': 'atct_album_view'},
            )
        },
        {'id': 'publications', 'type': 'Folder', 'children': (
            {'id': 'index_html', 'type': 'Document', 
            'text': 'Publications include legislation and hansard.'},
            )
        },
        {'id': 'organisation', 'type': 'Folder', 'children': (
            {'id': 'index_html', 'type': 'Document', 
            'text': 'The parliament is structured as follows ...',
            'children': ()},
            )
        },
        )
