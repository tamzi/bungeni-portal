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
        {'title': 'Help', 'type': 'HelpFolder', 'children': (
                {'id': 'index_html', 'title': 'Help', 'type': 'Document', 'text': 'Some helpful text to explain how to get around in the site. '},
                {'title': 'FAQ', 'type': 'HelpCenterFAQFolder', 'children': (
                    {'title': 'How can I find out the name of my Member of Parliament?', 'answer': 'Use our Find your MP service to identify the name of your MP.', 'type': 'HelpCenterFAQ'},
                    {'title': 'Who is the youngest MP?', 'answer': 'The youngest MP is Jo Swinson, MP for East Dunbartonshire (DOB 05.02.80)', 'type': 'HelpCenterFAQ'},
                    {'title': 'How can I contact my Member of Parliament?', 'answer': '''MPs may be contacted at the House of Commons, London, SW1A 0AA. It is usually a good idea to write to your MP in the first instance, so that you can explain things clearly and so that your MP will have written details of your case. However, if you would like to speak to your MP's office at the House of Commons, please telephone the switchboard (020 7219 3000) and ask to be transferred to the appropriate office. The switchboard can also take a message for your MP.\n\nIf you wish to e-mail your MP, please check the Alphabetical List of Members of Parliament. Where MPs have requested a link to their e-mail, it is given in the right-hand column.''', 'type': 'HelpCenterFAQ'}
                    )},
                {'title': 'Glossary', 'type': 'HelpCenterGlossary', 'children': (
                    {'title': 'Abstain', 'description': 'To abstain is to refuse to take sides in a vote.  However, abstentions are not officially recorded in the House of Commons or House of Lords.', 'type': 'HelpCenterDefinition'},
                    {'title': 'Yeomen of the Guard (Beefeaters)', 'description': '''Before the State Opening of Parliament, the Yeomen of the Guard search the cellars of the Palace of Westminster to ensure that there is no repeat of the Gunpowder Conspiracy, when Guy Fawkes was arrested in the cellars attempting to blow up the Palace.\n\nThe Yeomen of the Guard are a military corps founded by Henry VII in 1485 and since then they have been the bodyguard of the Monarch although their duties today are purely ceremonial.''', 'type': 'HelpCenterDefinition'}
                    )}
                )
        },
        )

DEFAULT_WORKSPACES = (
        {'id': 'workspace', 'title': 'Committee workspaces', 'type': 'Folder', 'children': (
            {'title': "House Business Committee", 'type': 'TeamSpace'},
            {'title': "Public Accounts Committee", 'type': 'TeamSpace'},
            {'title': "Public Investments Committee", 'type': 'TeamSpace'},
            {'title': "Speaker's Committee", 'type': 'TeamSpace'},
            {'title': "Standing Orders Committee", 'type': 'TeamSpace'},
            {'title': "Liaison Committee", 'type': 'TeamSpace'},
            {'title': "Powers and Privileges Committee", 'type': 'TeamSpace'},
        )},
        )

# Some members to play with
DEFAULT_MEMBERS = (
        {'salutation': 'Mr', 'firstname': '', 'surname': "Smith", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Prof.', 'firstname': '', 'surname': "Mzee", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Kofa", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Manga", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Mak'Onyango", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Manduku", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Achola", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Criticos", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Aluoch", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Nthenge", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Moiben", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Barmasai", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Nyagah", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Maore", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Obwocha", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Shikuku", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Col.', 'firstname': '', 'surname': "Kiluta", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Karan", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Dr.', 'firstname': '', 'surname': "Lwali-Oyondi", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Farah", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Falana", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'R.K.', 'firstname': '', 'surname': "Mungai", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Angatia", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Wetangula", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        {'salutation': 'Mr.', 'firstname': '', 'surname': "Wako", 'type': 'MemberOfParliament', 'email': 'jean.jordaan@gmail.com'},
        )

# Some committees to play with
DEFAULT_TEAMS = (
        {'title': "Members: House Business Committee", 'description': "prepares and manages the programme of the business of the House on a weekly basis;", 'type': 'Team', 'children': (
            {'firstname': '', 'surname': "Smith", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Mzee", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Kofa", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Manga", 'type': 'Team Membership'},
        )},
        {'title': "Members: Public Accounts Committee", 'description': "examines reports by the Controller and Auditor-General on Central Government expenditure and fund accounts;", 'type': 'Team', 'children': (
            {'firstname': '', 'surname': "Farah", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Falana", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Mungai", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Angatia", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Wetangula", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Wako", 'type': 'Team Membership'},
        )},
        {'title': "Members: Public Investments Committee", 'description': "examines reports by the Auditor-General (Corporations) on accounts of state corporations;", 'type': 'Team', 'children': (
            {'firstname': '', 'surname': "Mak'Onyango", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Shikuku", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Kiluta", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Karan", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Lwali-Oyondi", 'type': 'Team Membership'},
        )},
        {'title': "Members: Speaker's Committee", 'description': "examines matters relating to the welfare of Members and staff of the National Assembly;", 'type': 'Team', 'children': (
            {'firstname': '', 'surname': "Manduku", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Maore", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Obwocha", 'type': 'Team Membership'},
        )},
        {'title': "Members: Standing Orders Committee", 'description': "examines matters relating to and makes periodic reviews of the Standing Orders as necessary", 'type': 'Team', 'children': (
            {'firstname': '', 'surname': "Achola", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Nyagah", 'type': 'Team Membership'},
        )},
        {'title': "Members: Liaison Committee", 'description': "examines and co-ordinates matters relating to operations of the Departmental Committees; and", 'type': 'Team', 'children': (
            {'firstname': '', 'surname': "Moiben", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Barmasai", 'type': 'Team Membership'},
        )},
        {'title': "Members: Powers and Privileges Committee", 'description': "is established under the National Assembly (Powers and Privileges) Act, (Cap 6, Laws of Kenya), and deals with issues regarding privileges of the House, Members and staff.", 'type': 'Team', 'children': (
            {'firstname': '', 'surname': "Criticos", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Aluoch", 'type': 'Team Membership'},
            {'firstname': '', 'surname': "Nthenge", 'type': 'Team Membership'},
        )},
        )
