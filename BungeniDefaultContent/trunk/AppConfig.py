# We add default content for the Bungeni product.
DEPENDENCIES = ['Bungeni', ]

LOREM_IPSUM = """

Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec euismod accumsan neque. Curabitur sollicitudin faucibus ipsum. Aliquam erat volutpat. Phasellus arcu. Vestibulum vulputate tempus neque. Nulla arcu felis, interdum sed, auctor ut, pellentesque in, purus. Phasellus cursus. Quisque mauris odio, tincidunt tempor, porttitor sit amet, interdum ut, nisi. Cras leo tortor, auctor sed, aliquet aliquet, luctus vitae, quam. Vivamus viverra facilisis justo. Morbi posuere nulla vel ligula. Sed vitae ante in magna volutpat pharetra. Fusce eget justo et turpis ultrices vulputate. Praesent sapien diam, hendrerit et, accumsan a, molestie a, mi. Nullam porta feugiat metus. Aenean rhoncus velit ac enim.

Fusce rutrum leo nec ligula. Phasellus in leo vel nibh iaculis iaculis. Suspendisse potenti. Fusce placerat eros ac mi. Duis nec ante eget lacus porttitor ornare. Praesent porta, mauris in rhoncus molestie, magna libero lobortis mauris, ut volutpat libero risus ut lectus. Donec blandit ornare diam. Donec fermentum venenatis lectus. Ut et diam in mauris sodales egestas. Aenean arcu dui, condimentum et, convallis vel, faucibus nec, enim. Nam sagittis accumsan tellus. Aliquam diam nisi, ultricies id, sollicitudin at, bibendum in, sem. Quisque ut elit sed erat luctus iaculis. Ut bibendum enim et leo convallis sodales. Phasellus auctor metus ut magna. Vivamus sed leo. Fusce eget eros. Etiam varius auctor est. Cras nunc.

Cras lobortis dui eget ipsum. Aenean sollicitudin accumsan lacus. Duis justo arcu, euismod vestibulum, tempor eu, interdum vitae, mauris. Aenean ut nisi. Mauris at urna a dolor porta ultricies. Nunc tempor. Integer quis eros sit amet enim faucibus lacinia. Sed non nisi vitae metus imperdiet scelerisque. Proin lorem dolor, pellentesque sed, blandit non, mollis ut, turpis. Nullam adipiscing libero sit amet nisl. Maecenas ipsum diam, condimentum et, tempus id, condimentum in, urna. Donec non lorem eu erat vestibulum dictum.

Morbi rhoncus mi ac lacus. Aenean orci nunc, dictum nec, ornare id, porttitor at, sapien. Praesent eget nibh quis lectus scelerisque condimentum. Nam hendrerit, augue a scelerisque fringilla, nisi mauris volutpat metus, malesuada dapibus orci ligula vel nibh. Sed id nunc. Fusce vitae nulla ac arcu tincidunt commodo. Nullam facilisis accumsan massa. Fusce nibh justo, euismod a, eleifend vitae, commodo vel, nulla. Nam eros. Integer arcu nunc, egestas vel, eleifend vel, dignissim eu, mi.

Fusce venenatis nisi eget mauris. Donec mattis. Vestibulum vitae lorem. Pellentesque iaculis tortor ac enim. Suspendisse lacus. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Cras pulvinar pharetra augue. Aenean vitae quam. Cras porta nunc at erat. Nullam non nisl. Proin ante lectus, convallis ut, pretium vel, iaculis in, risus. Vestibulum posuere, ligula sed egestas ultricies, erat erat nonummy ante, nec consequat odio pede id mi. Proin sit amet nisi eget eros pharetra porttitor. Maecenas odio quam, ultricies ac, lacinia at, molestie at, leo. Fusce dignissim tortor fermentum erat. Nam sodales consequat metus. Praesent auctor placerat ante. Praesent blandit nunc ac ipsum. Vivamus nunc. Cras porta erat id arcu.
"""

DEFAULT_SITE_CONTENT = (
        {'title': 'Business', 'type': 'Folder', 'children': (
            {'id': 'index_html', 'title': 'Business', 'type': 'Document', 'text': 'Documents about parliamentary business'+LOREM_IPSUM, },
            {'title': 'Chamber', 'type': 'Folder', 'children': (
                {'title': 'Business Bulletin', 'text': 'Text about Business Bulletin'+LOREM_IPSUM, 'type': 'Document'}, 
                {'title': 'Debate Report', 'text': 'Text about Debate Report'+LOREM_IPSUM, 'type': 'Document'}, 
                {'title': 'Minutes of Proceedings', 'text': 'Text about Minutes of Proceedings'+LOREM_IPSUM, 'type': 'Document'}, 
                {'title': 'Tabled Documents', 'text': 'Text about Tabled Documents'+LOREM_IPSUM, 'type': 'Document'}, 
                {'title': 'Voting Records', 'text': 'Text about Voting Records'+LOREM_IPSUM, 'type': 'Document'}, 
                {'title': 'Attendance List', 'text': 'Text about Attendance List'+LOREM_IPSUM, 'type': 'Document'}, 
                ),},
            {'title': 'Committees', 'type': 'Topic', 'children': (
                # {'field': 'Type', 'type': 'ATPortalTypeCriterion', 'value': 'Team', 'operator': 'and'},
                ),},
            {'title': 'Bills', 'text': 'Text about Bills'+LOREM_IPSUM, 'type': 'Document'},
            {'title': 'Motions', 'text': 'Text about Motions'+LOREM_IPSUM, 'type': 'Document'},
            {'title': 'Questions', 'text': 'Text about Questions'+LOREM_IPSUM, 'type': 'Document'},
            {'title': 'Events', 'text': 'Text about Events'+LOREM_IPSUM, 'type': 'Document'},
            ),
        },
        {'title': 'People', 'type': 'Folder', 'children': (
            {'id': 'index_html', 'title': 'Parliament People', 'type': 'Document', 'text': 'Lists the MPs and staff. Use RichTopic?'+LOREM_IPSUM, },
            )
        },
        {'title': 'About', 'type': 'Folder', 'children': (
            {'id': 'index_html', 'title': 'About the parliament', 'type': 'Document', 'text': 'Background information about the parliament'+LOREM_IPSUM,},
            {'title': 'How it works', 'type': 'Folder', 'children': (
                {'id': 'index_html', 'title': 'How it works', 'type': 'Document'},
                # {'id': 'index_html', 'title': 'How it works', 'type': 'Dynamic Page'},
                {'title': 'Parliamentary Procedure', 'text': 'Text about Parliamentary Procedure'+LOREM_IPSUM, 'type': 'Document'}, 
                {'title': 'Standing Orders', 'text': 'Text about Standing Orders'+LOREM_IPSUM, 'type': 'Document'}, 
                {'title': 'The Legislative Process', 'text': 'Text about The Legislative Process'+LOREM_IPSUM, 'type': 'Document'}, 
                {'title': 'Oversight', 'text': 'Text about Oversight'+LOREM_IPSUM, 'type': 'Document'}, 
                {'title': 'Guides', 'type': 'LongDocument', 'children': (
                    {'title': 'Guide on Public Bills', 'text': 'Text about Guide on Public Bills'+LOREM_IPSUM, 'type': 'LongDocumentPage'}, 
                    {'title': 'Guide on Private Bills', 'text': 'Text about Guide on Private Bills'+LOREM_IPSUM, 'type': 'LongDocumentPage'}, 
                    {'title': 'Guide for Motions', 'text': 'Text about Guide for Motions'+LOREM_IPSUM, 'type': 'LongDocumentPage'}, 
                    {'title': 'Guide for Parliamentary Questions', 'text': 'Text about Guide for Parliamentary Questions'+LOREM_IPSUM, 'type': 'LongDocumentPage'}, 
                    {'title': 'Guide for Committee Conveners', 'text': 'Text about Guide for Committee Conveners'+LOREM_IPSUM, 'type': 'LongDocumentPage'}, 
                    {'title': 'Guide on Committees', 'text': 'Text about Guide on Committees'+LOREM_IPSUM, 'type': 'LongDocumentPage'}, 
                    )}, 
                )}, 
            {'title': 'History', 'text': 'Text about History'+LOREM_IPSUM, 'type': 'Document'}, 
            {'title': 'How to visit', 'text': 'Text about How to visit'+LOREM_IPSUM, 'type': 'Document'}, 
            {'title': 'How to participate', 'text': 'Text about How to participate'+LOREM_IPSUM, 'type': 'Document'}, 
            {'title': 'Learning resources', 'text': 'Text about Learning resources'+LOREM_IPSUM, 'type': 'Document'}, 
            {'title': 'Pictures', 'type': 'Folder', 'layout': 'atct_album_view'},
            )
        },
        {'title': 'Publications', 'type': 'Folder', 'children': (
            {'id': 'index_html', 'title': 'Publications', 'type': 'Document', 'text': 'Publications include legislation and hansard.'+LOREM_IPSUM},
            )
        },
        {'title': 'Organisation', 'type': 'Folder', 'children': (
            {'id': 'index_html', 'title': 'Organisation', 'type': 'Document', 'text': 'The parliament is structured as follows ...'+LOREM_IPSUM, },
            )
        },
        )

# Some committees to play with
DEFAULT_TEAMS = (
        # {'title': 'Committee 1', 'type': 'Team',},
        )
