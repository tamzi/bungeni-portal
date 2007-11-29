SET TRACE_LEVEL_FILE 1;       
SET WRITE_DELAY 500;          
SET CLUSTER '';               
SET DEFAULT_TABLE_TYPE 0;     
SET DEFAULT_LOCK_TIMEOUT 1000;
SET TRACE_LEVEL_SYSTEM_OUT 0; 
SET CACHE_SIZE 16384;         
;             
CREATE USER IF NOT EXISTS SA SALT '639c4703c5386f70' HASH '8a14c49558709d0202b9712aa71bd64dee9494450b6b3a06f89e409ac7ae0bae' ADMIN;           
CREATE SEQUENCE PUBLIC.SYSTEM_SEQUENCE_113DAF61_DFF7_4070_A19A_8CEBEBC694F7 START WITH 3 BELONGS_TO_TABLE;    
CREATE CACHED TABLE PUBLIC.METADATA_SOURCES(
    ID INT DEFAULT (NEXT VALUE FOR PUBLIC.SYSTEM_SEQUENCE_113DAF61_DFF7_4070_A19A_8CEBEBC694F7) NOT NULL NULL_TO_DEFAULT SEQUENCE PUBLIC.SYSTEM_SEQUENCE_113DAF61_DFF7_4070_A19A_8CEBEBC694F7,
    DISPLAY_NAME VARCHAR(100),
    TABLE_NAME VARCHAR(100)
);     
-- 2 = SELECT COUNT(*) FROM PUBLIC.METADATA_SOURCES;          
INSERT INTO PUBLIC.METADATA_SOURCES(ID, DISPLAY_NAME, TABLE_NAME) VALUES(1, 'Members of Parliament', 'members_of_parliament');
INSERT INTO PUBLIC.METADATA_SOURCES(ID, DISPLAY_NAME, TABLE_NAME) VALUES(2, 'Tabled Documents', 'tabled_documents');          
CREATE PRIMARY KEY ON PUBLIC.METADATA_SOURCES(ID);            
CREATE CACHED TABLE PUBLIC.EDITOR_MACROS(
    PROG_LANGUAGE CHAR(20) NOT NULL,
    LIBRARY_NAME VARCHAR(100) NOT NULL,
    MACRO_NAME VARCHAR(100) NOT NULL,
    NO_OF_PARAMS INT
);          
-- 21 = SELECT COUNT(*) FROM PUBLIC.EDITOR_MACROS;            
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'AddSectionInsideSectionWithStyle', 4);         
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'SearchAndReplace', 2);         
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'AddSectionInsideSection', 2);  
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'InsertHTMLDocumentIntoSection', 3);            
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'CursorInSection', 0);          
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'AddSectionInsideSectionWithAttributes', 4);    
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'SearchAndReplaceWithAttributes', 4);           
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'InsertArrayAsBulletList', 3);  
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'SearchAndReplace2', 4);        
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'AddTextSection', 3);           
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'InsertDocumentIntoSection', 3);
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'AddImageIntoSection', 2);      
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'SetInputFieldValue', 2);       
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'SetReferenceInputFieldValue', 3);              
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'SetSectionMetadata', 3);       
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'RenameSection', 2);            
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'ReplaceLinkInSectionByName', 5);               
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'MoveSection', 4);              
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'InsertSectionAfterSection', 3);
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'InsertSectionAfterSectionWithStyle', 5);       
INSERT INTO PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME, NO_OF_PARAMS) VALUES('Basic', 'BungeniLibs.Common', 'RemoveSectionAndContents', 2); 
CREATE PRIMARY KEY ON PUBLIC.EDITOR_MACROS(PROG_LANGUAGE, LIBRARY_NAME, MACRO_NAME);          
CREATE CACHED TABLE PUBLIC.ACTION_PARENT(
    DOC_TYPE VARCHAR(100) NOT NULL,
    ACTION_NAME VARCHAR(100) NOT NULL,
    PARENT_ACTION VARCHAR(100) NOT NULL
);               
-- 18 = SELECT COUNT(*) FROM PUBLIC.ACTION_PARENT;            
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makePrayerMarkup', 'makePrayerSection');       
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makePaperMarkup', 'makePaperSection');         
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makePaperDetailsMarkup', 'makePaperSection');  
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeNoticeOfMotionMarkup', 'makeNoticeOfMotionSection');       
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeCommentsMarkup', 'makeSpeechBlockSection');
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeNoticeMarkup', 'makeNoticeOfMotionSection');               
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeSpeechMarkup', 'makeSpeechBlockSection');  
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeCommentsMarkup', 'makeNoticeOfMotionSection');             
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeCommentsMarkup', 'makeQuestionBlockSection');              
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeCommentsMarkup', 'makePaperSection');      
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeCommentsMarkup', 'makePrayerSection');     
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeSpeechBlockSection', 'makeQASection');     
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeSpeechBlockSection', 'makeNoticeOfMotionSection');         
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeQuestionBlockSection', 'makeQASection');   
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeSpeechBlockSection', 'makeQuestionBlockSection');          
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeQATitleMarkup', 'makeQASection');          
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeQuestionTitleMarkup', 'makeQuestionBlockSection');         
INSERT INTO PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION) VALUES('debaterecord', 'makeQuestionTextMarkup', 'makeQuestionBlockSection');          
CREATE PRIMARY KEY ON PUBLIC.ACTION_PARENT(DOC_TYPE, ACTION_NAME, PARENT_ACTION);             
CREATE CACHED TABLE PUBLIC.DOCUMENT_SECTION_TYPES(
    DOC_TYPE VARCHAR(100) NOT NULL,
    SECTION_TYPE_NAME VARCHAR(50) NOT NULL
);          
-- 8 = SELECT COUNT(*) FROM PUBLIC.DOCUMENT_SECTION_TYPES;    
INSERT INTO PUBLIC.DOCUMENT_SECTION_TYPES(DOC_TYPE, SECTION_TYPE_NAME) VALUES('debaterecord', 'MastHead');    
INSERT INTO PUBLIC.DOCUMENT_SECTION_TYPES(DOC_TYPE, SECTION_TYPE_NAME) VALUES('debaterecord', 'NoticeOfMotion');              
INSERT INTO PUBLIC.DOCUMENT_SECTION_TYPES(DOC_TYPE, SECTION_TYPE_NAME) VALUES('debaterecord', 'NoticeOfMotionDetails');       
INSERT INTO PUBLIC.DOCUMENT_SECTION_TYPES(DOC_TYPE, SECTION_TYPE_NAME) VALUES('debaterecord', 'MetadataContainer');           
INSERT INTO PUBLIC.DOCUMENT_SECTION_TYPES(DOC_TYPE, SECTION_TYPE_NAME) VALUES('debaterecord', 'QAContainer'); 
INSERT INTO PUBLIC.DOCUMENT_SECTION_TYPES(DOC_TYPE, SECTION_TYPE_NAME) VALUES('debaterecord', 'Question');    
INSERT INTO PUBLIC.DOCUMENT_SECTION_TYPES(DOC_TYPE, SECTION_TYPE_NAME) VALUES('debaterecord', 'QuestionContainer');           
INSERT INTO PUBLIC.DOCUMENT_SECTION_TYPES(DOC_TYPE, SECTION_TYPE_NAME) VALUES('debaterecord', 'Speech');      
CREATE PRIMARY KEY ON PUBLIC.DOCUMENT_SECTION_TYPES(DOC_TYPE, SECTION_TYPE_NAME);             
CREATE CACHED TABLE PUBLIC.DOCUMENT_TYPES(
    DOC_TYPE VARCHAR(100) NOT NULL,
    DESCRIPTION VARCHAR(100)
);
-- 5 = SELECT COUNT(*) FROM PUBLIC.DOCUMENT_TYPES;            
INSERT INTO PUBLIC.DOCUMENT_TYPES(DOC_TYPE, DESCRIPTION) VALUES('debaterecord', 'Debate Record');             
INSERT INTO PUBLIC.DOCUMENT_TYPES(DOC_TYPE, DESCRIPTION) VALUES('bill', 'Bill');              
INSERT INTO PUBLIC.DOCUMENT_TYPES(DOC_TYPE, DESCRIPTION) VALUES('document', 'Document');      
INSERT INTO PUBLIC.DOCUMENT_TYPES(DOC_TYPE, DESCRIPTION) VALUES('report', 'Report');          
INSERT INTO PUBLIC.DOCUMENT_TYPES(DOC_TYPE, DESCRIPTION) VALUES('act', 'Act');
CREATE PRIMARY KEY ON PUBLIC.DOCUMENT_TYPES(DOC_TYPE);        
CREATE CACHED TABLE PUBLIC.GENERAL_EDITOR_PROPERTIES(
    PROPERTY_NAME CHAR(50) NOT NULL,
    PROPERTY_VALUE CHAR(50),
    PROPERTY_DESCRIPTION VARCHAR(100)
);              
-- 12 = SELECT COUNT(*) FROM PUBLIC.GENERAL_EDITOR_PROPERTIES;
INSERT INTO PUBLIC.GENERAL_EDITOR_PROPERTIES(PROPERTY_NAME, PROPERTY_VALUE, PROPERTY_DESCRIPTION) VALUES('registryJDBCdriver', 'org.h2.Driver', 'jdbc driver to use for registry');           
INSERT INTO PUBLIC.GENERAL_EDITOR_PROPERTIES(PROPERTY_NAME, PROPERTY_VALUE, PROPERTY_DESCRIPTION) VALUES('registryDB', 'registry.db', 'registry db name');    
INSERT INTO PUBLIC.GENERAL_EDITOR_PROPERTIES(PROPERTY_NAME, PROPERTY_VALUE, PROPERTY_DESCRIPTION) VALUES('registryJDBCdriverPrefix', 'jdbc:h2:', 'prefix for registry jdbc connection string');               
INSERT INTO PUBLIC.GENERAL_EDITOR_PROPERTIES(PROPERTY_NAME, PROPERTY_VALUE, PROPERTY_DESCRIPTION) VALUES('logoPath', 'settings\logos', 'path to logo');       
INSERT INTO PUBLIC.GENERAL_EDITOR_PROPERTIES(PROPERTY_NAME, PROPERTY_VALUE, PROPERTY_DESCRIPTION) VALUES('activeDocumentMode', 'debaterecord', 'editor client is set to edit a document of this type');       
INSERT INTO PUBLIC.GENERAL_EDITOR_PROPERTIES(PROPERTY_NAME, PROPERTY_VALUE, PROPERTY_DESCRIPTION) VALUES('root:debaterecord', 'root', 'name of root sectionfor debaterecord');
INSERT INTO PUBLIC.GENERAL_EDITOR_PROPERTIES(PROPERTY_NAME, PROPERTY_VALUE, PROPERTY_DESCRIPTION) VALUES('localRegistry', 'yes', 'registry is a local database ');            
INSERT INTO PUBLIC.GENERAL_EDITOR_PROPERTIES(PROPERTY_NAME, PROPERTY_VALUE, PROPERTY_DESCRIPTION) VALUES('registryUser', 'sa', 'user name to connect to registry db');        
INSERT INTO PUBLIC.GENERAL_EDITOR_PROPERTIES(PROPERTY_NAME, PROPERTY_VALUE, PROPERTY_DESCRIPTION) VALUES('registryPassword', '', 'password to connect to registry db');       
INSERT INTO PUBLIC.GENERAL_EDITOR_PROPERTIES(PROPERTY_NAME, PROPERTY_VALUE, PROPERTY_DESCRIPTION) VALUES('localRegistryFolder', 'registry', 'path to local registry (sub folder under main installation)');   
INSERT INTO PUBLIC.GENERAL_EDITOR_PROPERTIES(PROPERTY_NAME, PROPERTY_VALUE, PROPERTY_DESCRIPTION) VALUES('textMetadataPropertyBeginMarker', '{{', 'used to demarcate beginning of inline metadata');          
INSERT INTO PUBLIC.GENERAL_EDITOR_PROPERTIES(PROPERTY_NAME, PROPERTY_VALUE, PROPERTY_DESCRIPTION) VALUES('textMetadataPropertyEndMarker', '}}', 'used to demarcate ending of inline metadata ');              
CREATE PRIMARY KEY ON PUBLIC.GENERAL_EDITOR_PROPERTIES(PROPERTY_NAME);        
CREATE CACHED TABLE PUBLIC.DOCUMENT_METADATA(
    DOC_TYPE VARCHAR(100) NOT NULL,
    METADATA_NAME CHAR(50) NOT NULL,
    METADATA_DATATYPE CHAR(50) NOT NULL,
    METADATA_NAMESPACE CHAR(50),
    METADATA_TYPE CHAR(30),
    DISPLAY_ORDER INT,
    VISIBLE INT,
    DISPLAY_NAME CHAR(100)
);            
-- 5 = SELECT COUNT(*) FROM PUBLIC.DOCUMENT_METADATA;         
INSERT INTO PUBLIC.DOCUMENT_METADATA(DOC_TYPE, METADATA_NAME, METADATA_DATATYPE, METADATA_NAMESPACE, METADATA_TYPE, DISPLAY_ORDER, VISIBLE, DISPLAY_NAME) VALUES('debaterecord', 'doctype', 'string', 'bungeni', 'document', 1, 1, 'Document Type');          
INSERT INTO PUBLIC.DOCUMENT_METADATA(DOC_TYPE, METADATA_NAME, METADATA_DATATYPE, METADATA_NAMESPACE, METADATA_TYPE, DISPLAY_ORDER, VISIBLE, DISPLAY_NAME) VALUES('debaterecord', 'docmodifiedon', 'datetime', 'bungeni', 'document', 3, 1, 'Modified On');    
INSERT INTO PUBLIC.DOCUMENT_METADATA(DOC_TYPE, METADATA_NAME, METADATA_DATATYPE, METADATA_NAMESPACE, METADATA_TYPE, DISPLAY_ORDER, VISIBLE, DISPLAY_NAME) VALUES('debaterecord', 'docauthor', 'string', 'bungeni', 'document', 5, 1, 'Author');               
INSERT INTO PUBLIC.DOCUMENT_METADATA(DOC_TYPE, METADATA_NAME, METADATA_DATATYPE, METADATA_NAMESPACE, METADATA_TYPE, DISPLAY_ORDER, VISIBLE, DISPLAY_NAME) VALUES('debaterecord', 'parliamentid', 'string', 'bungeni', 'document', 4, 0, 'Parliament ID');     
INSERT INTO PUBLIC.DOCUMENT_METADATA(DOC_TYPE, METADATA_NAME, METADATA_DATATYPE, METADATA_NAMESPACE, METADATA_TYPE, DISPLAY_ORDER, VISIBLE, DISPLAY_NAME) VALUES('debaterecord', 'doccreatedon', 'datetime', 'bungeni', 'document', 2, 1, 'Created On');      
CREATE PRIMARY KEY ON PUBLIC.DOCUMENT_METADATA(DOC_TYPE, METADATA_NAME);      
CREATE CACHED TABLE PUBLIC.TOOLBAR_ACTION_SETTINGS(
    DOC_TYPE VARCHAR(100) NOT NULL,
    ACTION_NAME VARCHAR(100) NOT NULL,
    ACTION_ORDER INT NOT NULL,
    ACTION_STATE INT NOT NULL,
    ACTION_CLASS VARCHAR(200),
    ACTION_TYPE VARCHAR(50),
    ACTION_NAMING_CONVENTION VARCHAR(100),
    ACTION_NUMBERING_CONVENTION VARCHAR(50),
    ACTION_PARENT VARCHAR(50),
    ACTION_ICON VARCHAR(50),
    ACTION_DISPLAY_TEXT VARCHAR(100),
    ACTION_DIMENSION VARCHAR(50),
    ACTION_SECTION_TYPE CHAR(50),
    ACTION_EDIT_DLG_ALLOWED INT DEFAULT 0
);           
-- 16 = SELECT COUNT(*) FROM PUBLIC.TOOLBAR_ACTION_SETTINGS;  
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makeNoticeOfMotionSection', 3, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'section', 'notice-of-motion', 'single', 'parent', ' ', 'Create a Notice of Motion Section', ' ', ' NoticeOfMotion', 0);         
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makePrayerMarkup', 1, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'markup', 'prayer', 'none', 'makePrayerSection', ' ', 'Markup as Prayer', ' ', ' MastHead', 0);           
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makePaperMarkup', 1, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'markup', 'papers', 'none', 'makePaperSection', ' ', 'Markup as Paper', ' ', '', 0);       
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makePaperDetailsMarkup', 2, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'markup', 'paper-details', 'none', 'makePaperSection', ' ', 'Markup as Paper Details', ' ', '', 0); 
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makeQASection', 4, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'section', 'qa', 'serial', 'parent', ' ', 'Create a Question-Answer section', ' ', 'QAContainer', 0);        
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makeNoticeOfMotionMarkup', 1, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'markup', 'notice-of-motion', 'none', 'makeNoticeOfMotionSection', '', 'Markup as Notice-of-Motion', '', '', 0);  
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makeNoticeDetailsMarkup', 3, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'markup', 'notice-details', 'none', 'makeNoticeDetailsMarkup', '', 'Markup as Notice Details', '', '', 0);         
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makeNoticeMarkup', 2, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'markup', 'notice', 'none', 'makeNoticeOfMotionSection', ' ', 'Markup as Notice', ' ', '', 0);            
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makeQATitleMarkup', 1, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'markup', 'qa-title', 'none', 'makeQASection', '', 'Markup as QA Title', '', '', 0);     
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makeSpeechMarkup', 2, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'markup', 'speech-text', 'none', 'makeQuestionBlockSection', ' ', 'Markup as Speech', ' ', '', 0);        
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makeQuestionTitleMarkup', 1, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'markup', 'question-title', 'none', 'makeQuestionBlockSection', ' ', 'Markup as Question Title', ' ', '', 0);      
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makeQuestionTextMarkup', 2, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'markup', 'question-text', 'none', 'makeQuestionBlockSection', '', 'Markup as Question Text', '', '', 0);           
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makeQuestionBlockSection', 1, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'section', 'question', 'serial', 'makeQASection', 'makeQASection', 'Create a numbered Question Section', ' ', ' QuestionContainer', 1);           
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makePrayerSection', 1, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'section', 'prayers', 'single', 'parent', ' ', 'Create a Prayer Section', ' ', ' MastHead', 1);          
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makePaperSection', 2, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'section', 'papers', 'single', 'parent', ' ', 'Create a Paper Section', ' ', ' Paper', 0);
INSERT INTO PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME, ACTION_ORDER, ACTION_STATE, ACTION_CLASS, ACTION_TYPE, ACTION_NAMING_CONVENTION, ACTION_NUMBERING_CONVENTION, ACTION_PARENT, ACTION_ICON, ACTION_DISPLAY_TEXT, ACTION_DIMENSION, ACTION_SECTION_TYPE, ACTION_EDIT_DLG_ALLOWED) VALUES('debaterecord', 'makeSpeechBlockSection', 1, 1, 'org.bungeni.editor.actions.EditorActionHandler', 'section', 'speech', 'serial', 'makeQASection', ' ', 'Speech Section', ' ', ' Speech', 1);          
CREATE PRIMARY KEY ON PUBLIC.TOOLBAR_ACTION_SETTINGS(DOC_TYPE, ACTION_NAME);  
CREATE INDEX PUBLIC.TAS_ACTIONPARENT_IDX ON PUBLIC.TOOLBAR_ACTION_SETTINGS(ACTION_PARENT);    
CREATE CACHED TABLE PUBLIC.TOOLBAR_SUB_ACTION_SETTINGS(
    DOC_TYPE VARCHAR(100) NOT NULL,
    PARENT_ACTION_NAME VARCHAR(100) NOT NULL,
    SUB_ACTION_NAME VARCHAR(100) NOT NULL,
    SUB_ACTION_ORDER INT NOT NULL,
    SUB_ACTION_STATE INT NOT NULL,
    ACTION_TYPE VARCHAR(50),
    ACTION_DISPLAY_TEXT VARCHAR(100),
    ACTION_FIELDS VARCHAR(100)
);               
-- 4 = SELECT COUNT(*) FROM PUBLIC.TOOLBAR_SUB_ACTION_SETTINGS;               
INSERT INTO PUBLIC.TOOLBAR_SUB_ACTION_SETTINGS(DOC_TYPE, PARENT_ACTION_NAME, SUB_ACTION_NAME, SUB_ACTION_ORDER, SUB_ACTION_STATE, ACTION_TYPE, ACTION_DISPLAY_TEXT, ACTION_FIELDS) VALUES('debaterecord', 'makePrayerSection', 'section_creation', 0, 1, 'section_create', 'Create emtpy masthead', '');      
INSERT INTO PUBLIC.TOOLBAR_SUB_ACTION_SETTINGS(DOC_TYPE, PARENT_ACTION_NAME, SUB_ACTION_NAME, SUB_ACTION_ORDER, SUB_ACTION_STATE, ACTION_TYPE, ACTION_DISPLAY_TEXT, ACTION_FIELDS) VALUES('debaterecord', 'makePrayerSection', 'selectlogo', 3, 1, 'image', 'Apply logo', 'btn:initdebate_selectlogo');       
INSERT INTO PUBLIC.TOOLBAR_SUB_ACTION_SETTINGS(DOC_TYPE, PARENT_ACTION_NAME, SUB_ACTION_NAME, SUB_ACTION_ORDER, SUB_ACTION_STATE, ACTION_TYPE, ACTION_DISPLAY_TEXT, ACTION_FIELDS) VALUES('debaterecord', 'makePrayerSection', 'debatedate_entry', 1, 1, 'date', 'Markup debate date', 'dt:initdebate_hansarddate');          
INSERT INTO PUBLIC.TOOLBAR_SUB_ACTION_SETTINGS(DOC_TYPE, PARENT_ACTION_NAME, SUB_ACTION_NAME, SUB_ACTION_ORDER, SUB_ACTION_STATE, ACTION_TYPE, ACTION_DISPLAY_TEXT, ACTION_FIELDS) VALUES('debaterecord', 'makePrayerSection', 'debatetime_entry', 2, 1, 'time', 'Markup debate time', 'dt:initdebate_timeofhansard');        
CREATE PRIMARY KEY ON PUBLIC.TOOLBAR_SUB_ACTION_SETTINGS(DOC_TYPE, PARENT_ACTION_NAME, SUB_ACTION_NAME);      
CREATE INDEX PUBLIC.SUBACTIONORDER_IDX ON PUBLIC.TOOLBAR_SUB_ACTION_SETTINGS(SUB_ACTION_ORDER);               
