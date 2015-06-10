



---

## Overview ##

### The customization folder ###

Bungeni packages the customization aspects of the system in a specific folder.

Rather than start with no customization configurations, to make things easier, Bungeni comes packaged with a default customization folder which can be used as a basis for creating your own customizations.

The system comes packaged with a default customization setup in the `src/bungeni_custom` folder (let's refer to this as `{BUNGENI_CUSTOM}` from here on) within your main Bungeni installation folder i.e. somewhere like `/my/installation/path/bungeni_apps/bungeni` (and let's refer to this one simply as `{BUNGENI}` from here on).

The customization folder structure looks like this :
```
bungeni_custom/
├── __init__.py
├── types.xml
├── forms/
├── notifications/
├── registry/
├── reporting/
├── sys/
├── translations/
├── vocabularies/
├── workflows/
└── workspace/
```

This structure provides points of access to different aspects of customization discussed in this document. The content of the folders is described below.

| **file / folder name** | **purpose** |
|:-----------------------|:------------|
| `__init__.py`          | Special file that defines this folder as a _python package_; sets some general variables |
| `types.xml`            | Declares all custom types |
| `forms`                | Contains the configuration files for UI form descriptors |
| `notifications`        | contains the notification configuration files used for workflow notifications |
| `registry`             | Contains the format for numbering content|
| `reporting`            | Contains the reporting templates in XHTML format |
| `sys`                  | Contains configuration files related to database connections, openoffice access and default roles in the system |
| `translations`         | Contains the localized message strings in [PO format](http://www.gnu.org/savannah-checkouts/gnu/gettext/manual/html_node/PO-Files.html) |
| `vocabularies`         | Contains the different vocabularies used in the system in VDEX format |
| `workflows`            | Contains the Workflow customization files. There is one file per document type |
| `workspace`            | Contains the Workspace customization files. There is one file per document type |


By default when you install the system - a private customization folder is created within `bungeni_apps/customizations` called by the same name `bungeni_custom`.

**We don't recommend making customizations in the default customization folder, instead use the private customization folder in `bungeni_apps/customizations` to make your custom modifications. This kind of setup will allow you to test your customization against the reference customization implementation provided out of the box in Bungeni**.

### How Bungeni determines the active customization folder ###

Bungeni determines the customization folder by means of a `{BUNGENI}/bungeni_custom.pth` _python package path_ customization file that simply contains a path to where the system should look for a `bungeni_custom` _python package_. The default one contains:

```
    /home/undesa/bungeni_apps/bungeni/src
```

Changing the path here will tell Bungeni to look for the customization folder, i.e. the `bungeni_custom` python package, in a different location.

### Using the private customization folder ###

You can start customizing workflows, vocabularies, workspaces, et cetera, for your Bungeni in _your_ `bungeni_custom` folder at `/my/installation/path/bungeni_apps/customizations/bungeni_custom`.

Let's refer to _your_ private customization folder simply as `{MY_CUSTOM}` from now on.

### Testing customizations ###

While customizing, it may sometimes be useful to switch between customizations (e.g. the one you are working on and the default one that bungeni installs with); you may switch anytime by simply re-editing the `{BUNGENI}/bungeni_custom.pth` file (and restarting Bungeni).

### Best practices ###

  * You should version control (or at the very least backup) your customization folder since it isn't part of shipped bungeni source code. Which means if your server crashes for whatever reason and you have to reinstall and re-setup Bungeni, you will be able to restore the system and the default customisation since they are version controlled - but you won't be able to restore your own customizations unless you have your own backup.

  * Do **not** make your customizations in the default `bungeni_custom` customization folder. This is intended only as a test customization setup and is version controlled and will receive updates. Always use a private customization folder as specified above.





---

## How to configure languages ##
### Purpose ###
Here you can set the default launguage used in the Bungeni user interface as well as enable alternative languages.
If you have enabled more than one language, the default language (see below) will be used in the Bungeni user interface i.e. if the browser language is not one of the alternative languages.

### How to enable and set the default language ###

Bungeni language configuration is managed in this file:
```
    {MY_CUSTOM}/__init__.py
```
The location of this file may be different if you have a custom configuration location. (See [Using the customization folder](HowTo_CustomizeParliamentaryInformationManagement#Using_the_customization_folder.md))

The parameters in the table below will be found in this file and determine how languages are handled in Bungeni.

| **Parameter (Sample)** | **Notes** |
|:-----------------------|:----------|
| zope\_i18n\_allowed\_languages = "ar en es es-do fr it nl pt ru sw tk" | A space separated string of language ids of available languages.<br /> To enable or disable language, add or remove its id from this list |
| _default\_language = "en"_ | This is the default language used in the system. It should be one of those in `zope_i18n_allowed_languages`. |
| _right\_to\_left\_languages = "ar"_ | This is a space separated list of language ids for which the user interface should be displayed right-to-left. <br /> These language ids must be a subset of `zope_i18n_allowed_languages` |
| _zope\_i18n\_compile\_mo\_files = True_ | Set this to True/False to turn on/off compiling of message catalogs into a binary format (faster). |


Only enabled languages will show up in Bungeni's language menu. With the `zope_i18n_allowed_languages` setting above, this would be the resulting language menu.

![http://bungeni-portal.googlecode.com/svn/wiki/images/languages-menu.png](http://bungeni-portal.googlecode.com/svn/wiki/images/languages-menu.png)



---

## Vocabularies ##

A vocabulary is a _value list_ where each value needs to be remembered (e.g. stored in a database) in a standard way, but represented in a variety of ways, and possibly in different languages. Such value lists may also be nested i.e. a _value tree_.

Vocabularies may be static, so are a priori known and thus pre-defined, or dynamic, so a priori unknown as may depend on current data or context.

### Vocabulary names ###

Both static and dynamic vocabularies have a unique **name**, needed for when configuring _field descriptors_ in [UI Forms](#Forms.md). By convention, the name of a static vocabulary is the name of the file (without the extension) that defines it. Dynamic vocabularies are pre-defined, and named, by the Bungeni application.


### Static vocabularies ###

Bungeni uses the [Vocabulary Definition Exchange](http://www.imsglobal.org/vdex/) (VDEX) standard to manage customizable static vocabularies, each with a dedicated XML file, are to be found at:

```
    {MY_CUSTOM}/vocabularies/
        attachment_type.vdex
        attendance_type.vdex
        bill_type.vdex
        change_procedure.vdex
        committee_continuity.vdex
        committee_type.vdex
        event_type.vdex
        gender.vdex
        logical_address_type.vdex
        marital_status.vdex
        member_election_type.vdex
        party.vdex
        postal_address_type.vdex
        question_type.vdex
        representation.vdex
        response_type.vdex
        sitting-activity-types.vdex  # name: sitting_activity_types
        sitting-convocation-types.vdex  # name: sitting_convocation_types
        sitting-meeting-types.vdex  # name: sitting_meeting_types
        subject_terms.vdex
        yes_no.vdex
```

#### Managing static vocabularies ####

To manage a vocabulary we simply modify the corresponding XML file that defines it (in [VDEX format](http://www.imsglobal.org/vdex/)).

A vdex file defines a vocabulary _completely_. For example, we can add all individual terms that we need (the `<term>`), the _token_ value (the `<termIdentifier>`) for each term, the _display label_ (the `<caption>`) for each term, and in as many languages as we desire (a `<langstring>` per language per term).

Here, as an example, is a relatively simple vocabulary defining the types of Bills we choose to support in our parliament:
```
<vdex xmlns="http://www.imsglobal.org/xsd/imsvdex_v1p0" 
    orderSignificant="true" profileType="flatTokenTerms">
    <vocabName>
        <langstring language="en">bill_type</langstring>
    </vocabName>
    <vocabIdentifier>org.bungeni.metadata.vocabularies.bill_type</vocabIdentifier>
    <term>
        <termIdentifier>government</termIdentifier>
        <caption>
            <langstring language="en">Government Initiative</langstring>
            <langstring language="pt">Governo</langstring>
        </caption>
    </term>
    <term>
        <termIdentifier>member</termIdentifier>
        <caption>
            <langstring language="en">Member Initiative</langstring>
            <langstring language="pt">Membro</langstring>
        </caption>
    </term>
</vdex>
```


### Dynamic vocabularies ###

Bungeni pre-defines the following data or context dependent vocabularies, each being intended for a very specific purpose and context.

| **name** | **description** |
|:---------|:----------------|
| `language` | The list of available languages |
| `country` | The list of all countries |
| `workflow_states` | The list of states in this workflow |
| `workflowed_type` | The list of workflowed types |
| `group`  | The list of all active groups |
| `committee` | The list of all committees |
| `parliament` | The list of all parliaments |
| `ministry` | The list of all ministyries in current parliament |
| `group_sub_role` | The sub-roles of the role assigned to this group |
| `group_title_types` | The title types associated with this group |
| `office_role` | The sub-list of roles that may be assigned to an office |
| `member` | The members of this group |
| `parliament_member` | The list of all Members of Parliament |
| `parliament_member_delegation` | The list of MPs Delegating to this user (if any) or of all MPs |
| `user`   | The list of all active users |
| `user_not_mp` | The list of user who are not MPs |
| `owner_or_login` | The context owner OR the current logged in user (a list of 1 item) |
| `substitution` | Active user of the same group |
| `signatory` | The list of MP Signatories for this document |
| `sitting` | The list of all sittings |
| `sitting_attendance` | All members of this group who do not have an attendance record yet |
| `report` | The list of all reports |
| `venue`  | The list of all venues |



---

## Roles ##

Roles in Bungeni are used to specify who has permission to perform different tasks. Roles can be seen as a collection of permissions while permissions are like keys to doors that open to a particular functionality. For example, there may be a permission to view a document and another to edit the document. These permissions may then be granted to or denied from certain roles.

All the members of a group get the role associated with that group. For example, if a parliament has a "Clerk's Office" with a role "bungeni.Clerk" associated with it then all the members of that office are assigned that role. In addition the administrator may assign a sub-role to a specific member of a group. For example, in the Clerk's Office there may be one person who deals specifically with questions. He may be granted the sub-role bungeni.Question.Clerk and specific permissions may then be granted to this role.



### System roles - what they mean and default usage ###

System roles are the roles already defined in the system that are being used in a certain way and are not part of configuration. These are

| **Role ID** | **Use** | **Notes** |
|:------------|:--------|:----------|
| bungeni.Owner | The owner of a document, ie. the person who creates/moves a document |           |
| bungeni.Signatory | Signatory of a document |           |
| bungeni.Admin | The bungeni administrator |           |
| bungeni.Authenticated | All authenticated users |           |
| bungeni.Anonymous | Bungeni Visitor |           |
| bungeni.MP  | Member of parliament | To be deprecated |
| bungeni.Minister | Minister | To be deprecated |
| bungeni.PoliticalGroupMember | Political Group Member | To be deprecated |
| bungeni.Government | Member of Government | To be deprecated |
| bungeni.CommitteeMember | Committee Member | To be deprecated |

### Admin defined roles ###

A Bungeni administrator may define additional parliament specific roles in bungeni\_custom/sys/acl/roles.zcml. A role added here may then be associated with an office while adding an office.

| **attribute** | **example** | **note** |
|:--------------|:------------|:---------|
| title         | Clerk's Office | The title "Clerk's Office" is what appears in the user interface |
| id            | bungeni.Clerk | This is the ID that will be used anywhere else in the system where a role may be specified e.g. the workspace configuration or the workflow configuration. |

Example

```
<role title="Clerk's Office" id="bungeni.Clerk" />
```

To associate the role above with an office, in “administration” go to “offices” and add an office, then set the "role id" field to this role.

### Sub Roles ###

If you need to have finer grained roles you may use sub-roles e.g. If you want all staff in the Clerk Office to see all parliamentary documents, but only the “Question Office” staff to actually edit questions and move them in the workflow.

Please note that with sub-roles one cannot deny permissions that have been granted to the parent role.

| **attribute** | **example** | **note** |
|:--------------|:------------|:---------|
| title         | Question Clerk | The title "Question Clerk" is what appears in the UI |
| id            | bungeni.QuestionClerk |This is the ID that will be used anywhere else in the system where a role may be specified e.g. the workspace configuration or the workflow configuration. |
| role          | bungeni.Clerk | This is the ID parent role |


Example

```
<bungeni:subrole id="bungeni.QuestionClerk" title="Question Clerk" role="bungeni.Clerk"/>
```

The above example creates a new sub-role of the "bungeni.Clerk" role. A Bungeni administrator may then grant this sub-role to a member of the "Clerk's Office" by going to the admin tab -> offices -> Clerk's office -> Office Members, selecting the member they would like to grant the sub-role to from the list then selecting "add sub-role" from the menu.

There is an option to either grant the sub-role to the user globally or not. A global sub-role means that that user is granted that role on the group like the main group role. A non-global sub-role means that the user only gets that sub-role on documents that have been assigned to him.

#### Assignment feature ####

Bungeni supports assigns members of staff to work on different different documents. For example, if a Clerk’s office has 10 Question Clerks and 100 incoming questions, the Clerk can allocate specific questions to the different clerks.

Note: Read more information about document features below.

The assignment feature is enabled per document type in the document's workflow. The assignment feature has two parameters "assigning\_roles" and "assign\_to\_roles". Persons with a role listed in "assign\_roles" have the ability to assign the document type to users with an "assign\_to" role.

The administrator also needs to specify in which states of the document that the assignments can be viewed or edited by granting the view/edit permissions on that state.

```
    <facet name="internal">
        ...
        <allow permission="user_assignment.View" roles="Clerk.HeadClerk" />
        <allow permission="user_assignment.Edit" roles="Clerk.HeadClerk" />
    </facet>
    
    ...
    
    <state id="received" title="Received by clerk" tags="actionclerk">
        <facet ref=".internal" />
        ...
    </state>
```

When a document is in a state in which assignments may be viewed/edited, a user with a role that may view/edit documents gets a menu items on the document to view/edit assignments

<a href='Hidden comment: 
----
== Parliamentary Metadata ==
=== Adding a parliament ===
=== Adding Parliamentary entities ===
=== Committees ===
=== Groups ===
=== Government ===
=== Users ===
=== Offices ===
'></a>




---

## Document, Group and other Types ##

Bungeni provides rich support for a variety of **parliamentary document types** e.g. _Agenda Item_, _Bill_, _Motion_, _Question_, _Tabled Document_, as well as a variety of **group and membership types** that are typical of many parliament-like institutions e.g. _Ministry_, _Committee_, _Office_.

### Archetypes, custom types ###

All these above-mentioned types are not only entirely customizable in Bungeni, but may also be extended to instruct the system to handle other _document_ or _group_ or _membership_ types. And, for each of these categories of custom types, bungeni offers an _archetype_ that is to be used as the base _template_ for any additional types we wish to extend the system with. Each archetype provides the necessary "behaviour" for the given category of type (bundled as _features_) that we can enable and disable as we need per type we define. Custom types are entirely customizable (including possibility of disabling them altogether).

### System support types ###

Bungeni also provides a variety of other _support_ types, such as _Sitting_, _User_, _Signatory_, _Event_, _Attachment_, _Audit_ etc, needed to support the functionality of the various archetype-based types we define. Support types may be customized to quite some degree (but may not be disabled).

Note that, if an aspect of a Bungeni object type (be it parliamentary documents, groups, memberships, or any support type) is customizable, then it is customizable in a consistent way i.e. if a type is _workflowed_ then the workflow is always controlled in the same way. if a type has a Form UI Views, then those views are always controlled in the same way (via a UI Descriptor), and so on.


### Parliamentary Documents ###

All **parliamentary document types** are based on the _Doc_ archetype. The document types _Agenda Item_, _Bill_, _Motion_, _Question_, _Tabled Document_, are included in Bungeni out of the box, and as mentioned others types may be added to the system easily.

All parliamentary document types are **workflowed**--with the workflow definition for any type being entirely customizable. Most other aspects of a document type definition are also customizable e.g. the various **user interface views** (via UI _descriptors_) for the type, or which **features** are enabled by the type.

#### Document _features_ ####

A document type may enable or disable a variety of **features**. When enabled for the document type, the feature is available for _each_ document of that type.

In each case, when a feature is enabled for a type, the system will also provide the necessary User Interface views for the feature e.g. if _audit_ is enabled for a type, then the UI will provide various ways to view the audit log of the document.

Here's a summary of supported features for parliamentary documents:

  * **audit**: all changes on a document are _audited_.
  * **version**: a document may be _versioned_.
  * **attachment**: _attachments_ may be added to the document.
  * **event**: _events_ (a special kind of support document) may be added to the document.
  * **signatory**: the document life-cycle, defined by its workflow, requires that other members of parliament _sign_ the document.
  * **schedule**: the document may be included in _sitting agenda_.
  * **workspace**: the document is to be included in the private user's _workspace_.
  * **notification**: user may subscribe and receive a variety of _notifications_ as the document changes.
  * **download**: the document may be available for _download_ e.g. in PDF.
  * **assignment**: the document may be assigned to specific users

Enabling, disabling and possibly parametrizing a feature for a type is part of the workflow definition for type--that must itself have been _enabled_.

#### Enabling and disabling custom document types ####

The entry point to type customization is the file:
```
    {MY_CUSTOM}/types.xml
```

A document type is enabled simply by including a `<doc>` element with the type name, and setting the attribute `@enabled="true"`. To disable, set the attribute `@enabled="false"` (or just remove the `<doc>` element):

```
<types>
    <doc name="agenda_item" enabled="true" />
    <doc name="bill" enabled="true" />
    <doc name="motion" enabled="true" />
    <doc name="question" enabled="true" />
    <doc name="tabled_document" enabled="true" />
    ...
</types>
```

All custom document types must specify a name, that will be the _key_ used throughout the system to identify this type.

As previously mentioned, all types are _workflowed_ and by default the name for the `{WORKFLOW_NAME}` is the same as the `{TYPE_NAME}` for the type--but this may be set to anything else via a '@workflow' attribute on the `<doc>` element. Whatever the `{WORKFLOW_NAME}` is specified to be, a correspodning _workflow definition file_ for it is expoected to be found at:
```
    {MY_CUSTOM}/workflows/{WORKFLOW_NAME}.xml
```

Disabling a type means the type will **not** be registered (so will be _unknown_ to Bungeni), and all associated configuration e.g. workflow, descriptor, workspace, etc, will also not be loaded.


### Groups ###

Group types included by default are _Parliament_, _Government_, _Committee_, _Ministry_, _Political Group_, _Office_. Group types and their memberships types are also enabled or disabled in a similar way as document types:
```
<types>
    ...
    <group name="parliament" enabled="true">
        <member name="member_of_parliament" workflow="group_membership" enabled="true" />
    </group>
    <group name="ministry" workflow="group" enabled="true">
        <member name="minister" workflow="group_membership" enabled="true" />
    </group>
    <group name="committee" enabled="true">
        <member name="committee_member" workflow="group_membership" enabled="true" />
        <member name="committee_staff" workflow="group_membership" enabled="true" />
    </group>
    ...
</types>
```
Notice that _Ministry_ group type is re-using the base _group_ workflow and all the various membership types are using the base _group\_membership_workflow._

Again, see the `{MY_CUSTOM}/types.xml` itself for further explanations and sample settings of these.

#### Group _features_ ####

  * **address**: the group supports having addresses

Note: other "behaviorial aspects" of groups, such as capacity to have members or capacity to hold sittings, are currently considered _intrinsic_ group features, and so possibility to enable or disable these is not offered (however, this is under consideration and may change).



---

## Forms ##

The Bungeni User Interface allows a number of interactions or manipulations for instances of any given type. These include creating, viewing, modifying an instance or even listing multiple instances. The various UI views required for these interactions are all highly customizable, both in terms of appearance as well as in terms of who can do what on an instance of the type. We use:

  * the term **forms** as a more general term for the UI views for a type;
  * the term **modes** to distinguish between the various interactions i.e. the above mentioned interactions correspond to the modes **add**, **view**, **edit** and **listing**.
  * **roles** to manage who may access specific fields in the different modes.

We use a _descriptor_ to describe all the above for each type in Bungeni.

**All types** in Bungeni are UI-customizable, some to a larger degree than others--custom types are of course completely customizable (so, as an example, we may even disable them completely) while other system-required _support_ types are quite extensively customizable (but not completely, for example we may _not_ disable them).


### Form field _descriptors_ ###

We customize the form views per type in Bungeni by means of a _descriptor_ per type, contained in either of the files:
```
    {MY_CUSTOM}/forms/ui.xml
    {MY_CUSTOM}/forms/custom.xml
```
The `ui.xml` file contains a UI _descriptor_ for each system support type (and a _default_ of this file may be automatically-regenerated, to reflect default settings in Bungeni for these system types).

The `custom.xml` files contains (the _master_ definition of) a UI _descriptor_ for each custom type we have added to the system.

A UI _descriptor_ for a type something like this:
```
<ui roles="bungeni.Clerk bungeni.Speaker bungeni.Owner bungeni.Signatory ... bungeni.Anonymous">
    ...
    <descriptor name="question" archetype="doc" order="13">
        ...
        <field name="title" label="Title" required="true" 
                value_type="text" render_type="text_box">
            <show modes="add" />
            <show modes="view edit listing" />
        </field>
        <field name="type_number" label="Number" required="false" 
                value_type="number" render_type="number">
            <show modes="view listing" />
        </field>
        <field name="acronym" label="Acronym" required="false" 
                value_type="text" render_type="text_line">
            <show modes="view edit add" />
            <hide modes="listing" />
        </field>
        <field name="description" label="Description" required="false" 
                value_type="text" render_type="text_box">
            <show modes="view edit add" />
            <hide modes="listing" />
        </field>
        <field name="response_type" label="Response Type" required="false"
                description="Choose the type of response expected for this question"
                value_type="vocabulary" render_type="single_select" vocabulary="response_type"
                extended="text">
            <show modes="view edit add listing" />
        </field>
        ...
    </descriptor>
    ...
</ui>
```

Each type _descriptor_ here controls the following aspects of the UI for the type:
  * the list of named UI fields for the type
  * the appearance _order_ of the UI fields for the type
  * various UI handling and rendering aspects for each field:
    * the field label and/or description
    * is it a required field or not?
    * what type should the value be considered as?
    * what class of UI widget should be used?
    * the controlled vocabulary to use, if any
  * the _modes_ in which the system may show/hide the field--this is the `@displayable` attribute (a convenience, provided for _information only_, may not modify)
  * the _modes_ that each field **is** customized in--the sum value of the `@modes` attribute of all the `<show>` and `<hide>` elements on the field;
  * for each _mode_, the _roles_ for whom the field is shown or not--the value of the _optional_ `@roles` attribute of all the `<show>` and `<hide>` elements on the field

The `descriptor/@order` attribute provides a hint to how references to descriptors themselves may be ordered e.g. for when generating navigation menus for browsing content such as the tree menu under the `admin` section.

The above extract describes some fields for a _question_. Here, as an example, is what the UI view might look like when we are logged in as the _Clerk_ and in **add** mode:

![http://bungeni-portal.googlecode.com/svn/wiki/images/add-question.png](http://bungeni-portal.googlecode.com/svn/wiki/images/add-question.png)

Note that the `type_number` field (that is the number of the question, updated at a later stage in the question's life-cycle) does not appear in **add** mode as per the field descriptor.

#### Extended properties ####

A descriptor may _extend_ the base descriptor it is based on with additional fields. This is done by simply adding an `extended` attribute to the `<field>` with the value being a supported extended property type that currently are:
  * `text`: the value is a piece of text e.g. the Question `response_type` field.
  * `translated_text`: the value is a piece of i18n text (can be translated to different languages) e.g. the Bill `short_title` field.

You may **not** declare a property in the base descriptor as extended.


### Changing display order of fields ###

The is simply a matter of re-ordering the `<field>` elements. So, for example if we would like to make `description` field appear after `response_type`, we simply move the field descriptor down i.e.
```
        ...
        <field name="response_type" label="Response Type" required="false"
                description="Choose the type of response expected for this question"
                value_type="vocabulary" render_type="single_select" vocabulary="response_type">
            <show modes="view edit add listing" />
        </field>
        <field name="description" label="Description" required="false" 
                value_type="text" render_type="text_box">
            <show modes="view edit add" />
            <hide modes="listing" />
        </field>
        ...
```
Then, whenever both fields are shown, the `description` field will appear above the `response_type` field. But note that this will have no visible affect in `listing` mode as `description` is not set to be displayed there (for all _roles_).

### Show/Hide fields on a Form per mode ###

Fields are customized using any number of `<show>` and `<hide>` elements, within the `<field>` element. Both the `<show>` and `<hide>` elements have the following attributes that allow customization of the field behavior:

  * _@modes_ - lists the modes that are to be shown or hidden.
  * _@roles_ - lists the roles for which the modes are to be shown or hidden. The only roles allowed here are the ones listed in the `ui/@roles` attribute. This is optional, and when not set all the roles listed in `ui/@roles` are implied.

`<show>` and `<hide>` do exactly what they are named as, `<show>` shows the field for the listed modes and roles, and `<hide>` hides the field for the listed modes and roles. A field may specify as many `<show>` and/or `<hide>` directives as it needs.
The action of the `show` or `hide` directive is applied to the list of roles specified in _@roles_--meaning also that the _opposite_ action is applied to the _complement_ of the set of roles specified in _@roles_ i.e. to all other roles in `ui/@roles`. Thus, `show` and `hide` are really complementary ways to state the same thing, but at times it may be more convenient to use than the other.

One thing to remember when using `<show>` and `<hide>` is that we may have as many `<show>` or `<hide>` elements as we need, but any given _mode_ may appear **only once**.

#### Show/Hide example ####

Above, the question _acronym_ field is shown to all in _view edit add_ modes, and hidden from all in _listing_ mode. Let's say we would like to adjust the _acronym_ field such that:
  1. only the _Clerk_ and the _Owner_ may _set or change_ it;
  1. we would like that in `listing` mode _all logged in users_ can see it;
  1. but for _view_ mode we keep it as it is i.e. it is shown to all.
To achieve this, we could modify the field descriptor as follows:
```
        <field name="acronym" label="Acronym" required="false" 
                value_type="text" render_type="text_line">
            <show modes="view" />
            <show modes="edit add" roles="Clerk Owner" />
            <hide modes="listing" roles="Anonymous" />
        </field>
```



---

## Workflow ##

<a href='Hidden comment: 
=== How to map documents/groups/membership workflow ===
=== How to configure documents/groups/membership workflow ===
'></a>

Every document type in Bungeni is _workflowed_, as mentioned above in the [Parliamentary Documents](#Parliamentary_Documents.md) section that also indicates how to **relate** a _workflow definition_ to a _type_.

A definition of a workflow in Bungeni is an XML file that defines the following behavioral aspects of the type it "workflows":
  * The dedicated _permission actions_ for the type.
  * _All_ the _global permissions_, dedicated to the type, that are to be granted to the various _roles_ you have defined in your parliament.
  * The _features_ enabled by the type, see [Document features](#Document_features.md) section for the list of available features on parliamentary document types in Bungeni.
  * The various _facets_--or _behaviourial faces_--that we would like to have the workflow may assume. A workflow facet allows a set of permissions, that may then be used by any state to allow the same set of permissions. Note that to configure permissions relating to a _feature_, a state uses a facet defined by the workflow of the sub-item.
  * _All_ the possible _states_ the type may be in, thoughout its life-cycle.
  * _All_ the _local permissions_, that are to be granted or denied _on the document instance_, to the various _roles_ we have defined in our parliament. Local permissions are defined by referring a single facet from same workflow, plus up to a facet per supported feature. Facets for disabled features are ignored.
  * _All_ the "paths" or _transitions_ we wish to allow from any state to another, along with other related information such as which _roles_ may execute the _transition_ or under what _condition_ should the transition be "made possible".

Here, just as indication of the various functions of a workflow XML definition, is a skeletal extract of a workflow definition for a _Motion_ document type:

```
<workflow title="Motion Workflow" 
    description="A Motion"
    tags="draft private public approved ... terminal"
    permission_actions=".View .Edit .Add .Delete"
    >
    
    <!-- global grants -->
    <allow permission=".Add" roles="Clerk MP" />
    
    <!-- features -->
    <feature name="audit" enabled="true" />
    <feature name="version" enabled="true" />
    <!-- NOTE on Feature Facet Permissions: Sub-item permissions (apart from the
    Add permission, that is by defn unbound to an *existing* item) that are 
    allowed within a *feature facet* apply only for when the (workflowed, always)
    sub-item itself is in a permissions_from_parent="true" state. -->
    <feature name="attachment" enabled="true" />
    <feature name="event" enabled="true" />
    <feature name="signatory" enabled="true">
        <parameter name="min_signatories" value="1" />
        <parameter name="open_states" value="admissible" />
    </feature>
    <feature name="schedule" enabled="true" />
    <feature name="workspace" enabled="true" />
    <feature name="notification" enabled="true" />
    <feature name="email" enabled="true" />
    <feature name="download" enabled="true" />
    <feature name="group_assignment" enabled="true" />
    
    <!-- workflow facets -->
    <facet name="draft_Clerk">
        <allow permission=".View" roles="Clerk" />
        <allow permission=".Edit" roles="Clerk" />
        <allow permission=".Delete" roles="Clerk" />
    </facet>
    ...
    
    
    <!-- states -->
    <state id="working_draft" title="Working Draft" tags="draft private">
        <facet ref=".draft_Clerk" />
        <facet ref="attachment.draft_Clerk" />
        <facet ref="event.draft_Clerk" />
        <facet ref="signatory.draft_Clerk" />
    </state>
    <state id="draft" title="Draft" tags="draft private">
        <facet ref=".draft_Owner" />
        <facet ref="attachment.draft_Owner" />
        <facet ref="event.draft_Owner" />
        <facet ref="signatory.draft_Owner" />
    </state>
    <state id="submitted_signatories" title="Submitted to Signatories" version="true" tags="actionmp">
        <facet ref=".internal_Signatory" />
        <facet ref="attachment.internal" />
        <facet ref="event.internal" />
        <facet ref="signatory.internal" />
    </state>
    <state id="redraft" title="Redraft" version="true" 
            note="document under review before resubmission">
        <facet ref=".redraft_Owner" />
        <facet ref="attachment.internal_Owner" />
        <facet ref="event.internal" />
        <facet ref="signatory.internal_Owner" />
    </state>
    ...
    
    
    <!-- transitions -->
    ...
    <transition title="Submit to Signatories"
        source="draft redraft"
        destination="submitted_signatories"
        condition="pi_has_signatories"
        roles="Owner"
    />
    <transition title="Redraft"
        source="submitted_signatories"
        destination="redraft"
        condition="user_is_context_owner"
        roles="Owner"
    />
    ...
```

Note that managing permissions for a type is the biggest and trickiest chore in managing a workflow. To help manage this arduous task, some tools and conventions are available:

  * The reponsibility of managing feature-related permissions is with the features themselves. Each feature defines as many _facets_ as needed i.e. for as many _behaviourial faces_ the feature takes on within the workflow.
    * Each state then may specify up to a single facet per feature, thus deciding how that feature should behave for when the document is in the state.
    * A facet may be set as the _default_, by setting `@default="true"`--in which case all states will automatically use this facet unless they explicitly specify another one.
    * Disabling a feature in a workflow will also _disable_ all the permsissions assocaited with any of its facets.

  * We only allow permissions (never _deny_); each state must explictly state what is allowed.

  * We may allow a permission to a Role either _globally_ (unlimited, not bound to any instance) or _locally_ (only for this _instance_ within a given _state_) but **not both**.

  * It is possibile to _bind_ the permissions of a state to that of another (for states with identical permissions), by using the `state/@permissions_from_state` attribute (to reference another state in the same workflow). However, when a state is bound to another in this way, no permission changes may be added i.e. it is all or nothing.

  * Similarly to previous, for sub-items such as _attachments_, _events_, _addresses_, we may delegate the permissions of a given state to the parent (head) document that _owns_ the sub-item, by setting the `state/@permissions_from_parent="true"` boolean attribute. Again, this is all or nothing, so if set no other permissions may be specified.



---

## Workspaces ##

Every user who logs in to Bungeni has a workspace, where they may view, add and edit documents. In order to provide the user with a familiar environment, the workspace in Bungeni has been modeled to the interface provided by very much used email applications (e.g Gmail or Yahoo mail).

The workspace has 3 main sections:
  1. my documents - Here a user finds all the documents that he has created, edited or signed in the lifetime of the current parliament;
  1. documents under consideration - This section contains all the parliamentary documents currently been worked on by parliament, and viewable by other users .e. they are in states tagged "public" in the workflow configuration and not tagged as being in terminal state, that would mean that they have ended their parliamentary life;
  1. scheduling – Here is were you may schedule sittings of the plenary and committees. See section on scheduling for more info.


### my documents section ###

The "my documents" section contains only those documents that the user has the permissions to add, view or edit e.g. in the case of the MP,  only the ones they have authored or signed, in the case of staff, only the documents that have been submitted to that department

The “my documents” section is structured in four tabs:

  * draft - This tab contains all the documents that the user is currently working on that have not been submitted to anyone else
  * inbox - This tab contains all the documents that require attention from the user, eg. a question that requires clarification from an MP, etc.
  * sent - This tab contains documents that the user has worked on and are now in some non terminal stage of their work-flow
  * archive - Here you find all the parliamentary documents that have reached their terminal state in the current parliament.

### How to configure workspaces ###

Every document type has a workspace configuration file in the workspace folder of the bungeni\_custom folder.

The administrator needs to specify which workspace tabs a document in a certain state will appear in for the different users.

To customise a workspace you need to set:

| attribute | example | note |
|:----------|:--------|:-----|
| state     | clarification\_required | The state of the document |
| tabs      | inbox   | The tabs the document should appear in |
| roles     | bungeni.MP | The roles for which this config applies |

Example

```
<state id="clarification_required">
  <tab id="inbox" roles="bungeni.Owner"/>
  <tab id="sent" roles="bungeni.Clerk"/>
</state>
```

The example above specifies that a document in the state "clarification\_required" will appear in the inbox of the person who introduced it (bungeni.Owner) and in the sent folder of the clerk (bungeni.clerk).



---

## Notification ##

Bungeni has a notifications system that can be configured to send out notifications to users on document workflow transitions. It is flexible, allowing for different methods to be used to send out notifications for example email or SMS.

The notifications system uses a message queue system called RabbitMQ to route and queue messages. When an event occurs in Bungeni that requires that someone be notified, a message is sent to the queue. Services such as email or SMS can then retrieve the message from the queue and send it to the intended recipient. Parliaments can build other applications that make use of the messages from the message queue such as Instant Messaging notifications e.g. Jabber, Social Media sites such as Facebook and Twitter and so on.

Enabling notifications is one step, one also has to configure the delivery method of the notification. Bungeni ships with an "email" feature, you may build other delivery methods that consume messages from the queue.

### How to set up notifications ###

Every document type has a notifications configuration file in the notifications folder

```
    {MY_CUSTOM}/notifications/{TYPE_NAME}.xml
```

| attribute | example | note |
|:----------|:--------|:-----|
| roles     | bungeni.Clerk | All users with this role on the object will be notified |
| onstate   | submitted | When the document reaches the states defined here, the users with the roles specified above will be notified |

For example

```
    <notify roles="bungeni.Clerk " onstate="submitted"/>
    <notify roles="bungeni.Owner" onstate="received"/>
```

In the above example, members of the clerks office will be notified when the document is submitted and the person who owns the document will be notified once it is received by the Clerk's office.

## Email ##

The email feature in Bungeni uses the notifications system described above. To enable email notifications for a workflowed type eg. a document or sitting, enable the feature "email" in the workflow for that type and add an email template in the email/templates folder in bungeni\_custom.

### Configuring the SMTP server ###

The first step of configuring the email notifications feature in Bungeni is to enter the details of the SMTP server. Login to bungeni and browse to "email settings" under the "administration" tab and enter the details of the SMTP server.

### Email Templates ###

The templates used for each document type are found in

```
    {MY_CUSTOM}/email/templates/{TYPE_NAME}.xml
```

The email subject and body templates are defined using ZPT, the template system used in Bungeni.


---

## Publications (agenda, agenda, minutes, reports) ##

### Purpose ###
Bungeni provides a facility to generate reports e.g. agenda, minutes, document reports e.t.c.
This section will explain how you may customise the templates used to generate reports.

### Scheduling (Calendar) Reports ###
Within scheduling, the reporting infrastructure provides a facility to produce documents out of the sittings within a certain period. Some typical use-cases include:
  * agenda and minutes of a specific sitting
  * a report of bills/questions e.t.c to be discussed in the coming month or other time-frame

Below is a screenshot of a report generation session.
The templates detailed below will appear as options on the report generation screen.
Adding or deleting templates (discussed below) will determine the options provided to generate reports within this context.

![http://bungeni-portal.googlecode.com/svn/wiki/images/reporting-scheduling-generation-session.png](http://bungeni-portal.googlecode.com/svn/wiki/images/reporting-scheduling-generation-session.png)

### Document Reports ###
The different documents in Bungeni e.g. bill, questions, e.t.c can also be download as PDF/ODT.
Document templates for the particular **document type** will determine the formattting og the PDF/ODT output.
Below is a sample of a document download session for a question:

![http://bungeni-portal.googlecode.com/svn/wiki/images/reporting-documents-download.png](http://bungeni-portal.googlecode.com/svn/wiki/images/reporting-documents-download.png)

### How to customise templates ###
The templates are based on XHTML with an additional set of tags to support inclusion of bungeni content into the final document.
Templates are stored in **bungeni\_custom** under: **/reporting/templates**

Those used in scheduling go into the **scheduling** directory whereas those used for document reports will be in **documents**.
Once templates are added within these directories they become available as options when generating reports.

### Structure of Templates ###
Each template is structurally composedof a configuration, head and body sections.

Here is a simple sample of a structure for a template:

```
<html xml:lang="en" xmlns:br="http://bungeni.org/reports">
  <br:config>
    <title>One week of questions Questions</title>
    <length>1w</length>
    <language>en</language>
  </br:config>
  <head>
    <title>Weekly Questions</title>
  </head>
  <body>
    <p>A blank report</p>
   </body>
</html>
```

#### Configuration section ####
The configuration section sets metadata associated with the current report type:
```
  <br:config>
    <title>Questions of the Week</title>
    <length>1w</length>
    <language>en</language>
  </br:config>
```
##### Configuration Options #####
| **Option** | **Sample** | **Description** |
|:-----------|:-----------|:----------------|
| title      | `<title>Questions of the week</title>` | This is the report title. It can be referenced within the body. It is also displayed in menus within Bungeni |
| length     | `<length>1w/length>` | Period covered by the report starting from a selected date. In this case - One(1) week. **More on this below**. |
| language   | `<language>fr</language>` | The language of the content in generated report |
| doctypes   | `<doctypes>question</doctypes>` | A space separated list of document types for which this template may generate reports. <sup>a</sup> |

<sup>a</sup> `Please note that the doctypes configuration parameter has meaning only in the context of document templates.`

###### Configuring Report Length ######
This is the notation used to specify the period covered by a report (_**n**_ is a positive integer greater than _1_)
  1. _n_**h** evaluates to n hours such that `1h` evaluates to one (1) hour
  1. _n_**d** evaluates to n days such that `5d` evaluates to five (2) days
  1. _n_**w** evaluates to n weeks such that `4w` evaluates to four (4) weeks
  1. We can also use combinations of _w_, _d_, _h_ depending on requirements

Below are sample timespans that can be used to specify the period covered by a report.
| **Length** | **Evaluates to** | **Equivalent hours notation** |
|:-----------|:-----------------|:------------------------------|
| 1h         | 1 hour           | _N/A_                         |
| 3d         | 3 days           | 72h                           |
| 2d6h       | 2 days and 6 hours | 54h                           |
| 2w         | 2 weeks          | 336h                          |

#### Body Section ####
Below you can see a sample of the body section of a report and customizable attributes.

```
  <body> 
    <div id="report-content">
        <h1 class="heading" br:type="text" br:source="title"/>
        <div id="listing-body">
            <div br:type="listing" br:source="sittings">
                <h2 br:type="text" br:source="title"/>
                <h3>Questions</h3>
                <div class="questions">
                    <ul br:type="listing" br:source="questions">
                        <li br:type="text" br:source="title"/>
                    </ul>
                </div>
            </div>
        </div>
    </div>
   </body>
```

##### Configuration options #####

| **Tag** | **Value** | **Description** | **Example** |
|:--------|:----------|:----------------|:------------|
| br:type | text      | Includes the specified context variable as text | Display the title of a document as plain text: <br /> `<div br:type="text" br:source="title"/>` |
|         | html      | Includes the specified context variable as HTML | Display the body of a document as html: <br /> `<div br:type="html" br:source="body_text"/>` |
|         | link      | Renders a link to with the link as the named **br:url** parameter | Display a link to a document uri with the dublin core title as link text: <br /> `<a br:type="link" br:url="uri" br:source="dc:title/>"` |
|         | listing   | Generates a list of items | Display the list of titles of questions included in the template: <br /> `<ul br:type="listing" br:source="questions">`<br />`    <li br:type="text" br:source="dc:title"/>` <br /> `</ul>` |
|         | block     | Uses specified br:source as context | Display document owner details for a question: <br /> `<table br:type="block" br:source="owner">` <br />    `<tr>`<br />        `<td>Title</td>`        <br />        `<td br:type="text" br:source="dc:title_member"/>`<br />    `</tr>` <br />`</table>` |
| br:source | A named context variable | names of available context variables are determined from the object available to the current template tag | See [HowTo\_CustomizeParliamentaryInformationManagement#Available\_context\_names](HowTo_CustomizeParliamentaryInformationManagement#Available_context_names.md) |
| br:condition | A named context variable | This attribute determines if the current tag should be rendered.<br /> Checks existense of a value for the named context variable. | This tag will only be rendered if there is a title <br /> `<span br:source="title" br:condition="title"/>` |

##### Available context names #####
The documentation for the names available for use in reports can generated from within Bungeni's home folder.
Simply run this script:
```
    ./bin/reporting-documentation
```
This will generate a tree in HTML of these names indiside the `docs/reporting/` folder within Bungeni's home folder.
You can open this file in any browser to see the tree of available names that can be incorporated in a report template.

If you are running Bungeni in debug mode, the reporting documentation can also be accessed from this address in a default installation.

```
    http://localhost:8081/docs/reporting/
```

Below is an image showing the generated tree of names:

![http://bungeni-portal.googlecode.com/svn/wiki/images/reporting-sample-doctree.png](http://bungeni-portal.googlecode.com/svn/wiki/images/reporting-sample-doctree.png)

`Note that in the case of document templates the names available are limited to the particular document section.`
`For instance in the case of a bill only the names under `bills` in the above figure would be available to the report template.`



---

## Layout, theme and formats ##
The layout, look and feel of the portal is controlled by a theme template in conjunction with a set of css styles and rule files. A default theme is enabled for each Bungeni installation.

### How to create a theme ###

Bungeni comes with a default theme and layout. You can create your own themes inside the custom folder. (see [customization folder](#The_customization_folder.md))

The theme folder should have the structure:

```
name_of_theme/
├── css/
├── images/
└── layout.html
```

Copy _`css`_ and _`images`_ folders together with _`layout.html`_ file from the default Bungeni theme into your theme folder. The Bungeni theme is located at:

```
{BUNGENI_INSTALL_PATH}/portal/src/portal.theme/portal/theme/static/
```

  * see [How to change page layout](HowTo_CustomizeParliamentaryInformationManagement#Changing_page_layout.md)
  * see [How to style with CSS](HowTo_CustomizeParliamentaryInformationManagement#Styling_with_CSS.md)

### Demo themes ###

Demo themes can be found at this location: http://bungeni-portal.googlecode.com/svn/portal.country_themes/trunk
To enable a demo theme, edit the demo\_theme parameter in the Fabric 'setup.ini' file. The default setting is as follows:

```
[custom]
...
demo_theme = default
```

Set this parameter to the appropriate value (_You must use the name of the theme as it is in the portal.country\_themes package_) e.g. for the demo theme with the name 'ke' the setting would be as follows:

```
[custom]
...
demo_theme = ke
```

then run the following command in fabric


```
fab -H localhost enable_demo_theme config_ini:portal 
```



### Changing page layout ###

The `layout.html` is an HTML file which defines the arrangement of HTML elements on both Portal and Workspace. It contains place-holder elements where to insert content from various Bungeni components.

The image below shows screenshots of both portal and workspace areas on Bungeni.

![http://bungeni-portal.googlecode.com/files/portal-and-workspace.png](http://bungeni-portal.googlecode.com/files/portal-and-workspace.png)

Think of `layout.html` as a template document that defines where to insert content, say the search-form or main-navigation bar. The HTML attributes _`id`_ and _`class`_ are used to identify the elements where you will insert content. In the snippet below, the `portal-search` _id_ denotes the container element where the search-form will be inserted.

```
<html>
  <head></head>
  <body>
   ...
   <!-- search -->
   <div id="portal-search"></div>
   ...
  </body>
</html>
```

### Getting layout content ###

There are rules that match content elements with the corresponding layout's elements. The rule to insert content into the above element looks like this:

```
   <!-- search -->
   <append content="children:#portal-search" theme="children:#portal-search" />
```

This will insert all elements **from** _`content`_ **into** _`theme`_ without copying the `#portal-search` element itself.
The rules are defined in `rules.xml` file found in:

```
{BUNGENI_INSTALL_PATH}/portal/src/portal.theme/portal/theme/static/themes/
```

To apply CSS styling, see **Styling with CSS** section below.

### Changing the Menu Order and Structure ###

### Styling with CSS ###

The CSS files for styling Bungeni are broken down into two files:

  * reset.css - Has styling properties that affect width, height and alignment of Bungeni.

  * skin.css - Cosmetic changes such as text-color, background-color, border, typography are done here.

styling in both CSS files is split into four major sections:

  * GENERAL - Applies site-wide
  * TEMPLATE-PORTAL - Anonymous user-space or public view
  * TEMPLATE-WORKSPACE - Logged in area
  * TEMPLATE-PORTAL-EXIST - Public view from an XML repository

Denoted at the start by a comment banner. e.g. for TEMPLATE-PORTAL

```
...

/* =============================================================================
   TEMPLATE PORTAL - Styling applied on portal
   ========================================================================== */

.template-portal {
    background: #eeeeee !important;
}

.template-portal #header-wrapper {
    background: #434343;
    border-bottom: 10px solid #c1c1c0;
}

...
```

These are top-level class selector's found on the HTML `body` tag e.g. `<body class="template-portal">`

To increase width of the portal from the default `960px`.

_reset.css_ -> find `template-portal` top-level section and look under width sub-section

Similar process for change background-color albeit under the _skin.css_ file

### Theming Bungeni using Skins ###

Bungeni skins are located under the custom folder:

```
{BUNGENI_INSTALL_PATH}/src/bungeni_custom/ 
```



---

## How to setup a parliament ##

Once you have defined your documents/their workflows and related roles and permissions, you have added their vocabularies, etc. you are ready to set up your own parliament.

To have Bungeni up and running, like any other system there is need a minimum set of data in order to be fully functional. You need to basically add:
  * **authenticated users** that may have specific roles in the context of parliamentary workflow;
  * **groups** that in Bungeni terms could be _offices_, _committees_, _political groups_; even _parliament_ is a _group. Groups may have sub-groups, they have begin and end date, they have membership, and title specific to each group and they may also have addresses._

Basically setting up your parliament means to add the authenticated users, define the _offices_ that is the structural organization of your parliament, add a parliament, members of parliament, its committees and political groups, and also setup the Government with its Ministries and the titles used to define the memberships of the different groups.

When you login as Administrator in the _administration_ tab you will find these folders: parliaments, offices, users:
  * **parliaments** folder lists the _parliaments_, (e.g. 7th Parliament – 2009-2014). Within a parliament you will find all the documents, groups with memberships of that specific parliament;
  * **offices** folder lists the _office_ of the system. Here, depending of the actual organisation structure of your parliament you can create Departments, Services within them or Directorates and Office. Etc.
  * **users** folder list all users that are allowed an authenticated access the system e.g. Members of Parliament, Parliamentary staff, government Ministers and staff, etc.

**Step 1: _create a parliament_**
In `administration/parliaments` click _add parliament_:

![http://bungeni-portal.googlecode.com/svn/wiki/images/add-parliament.png](http://bungeni-portal.googlecode.com/svn/wiki/images/add-parliament.png)

**Step 2: _add users_**
In `administration/users` click: _add user_

All authenticated users, being Members of Parliament, Parliamentary staff, government Ministers or staff, etc. aas to first be added as Bungeni _users_. Here you may input all the biodata of the users, and if required, e.g. the the case of MPs, you may also add a biographical note. You may also add _addresses_ that the users may have, e.g. office, home, etc.

Step 3: add offices and memberships

In administration/users click _add office_

All authenticated users, being Members of Parliament, Parliamentary staff, government Ministers or staff, etc. aas to first be added as Bungeni _users_. Here you may input all the biodata of the users, and if required, e.g. the the case of MPs, you may also add a biographical note. You may also add _addresses_ that the users may have, e.g. office, home, etc.

Step 4:  add _groups_, related memberships and titles

Within parliaments the different categories of information that may be need to setup the system are listed below.

  * **parliamentary sessions** Here you add parliamentary sessions;

  * **members of parliament** MP are registered uploaded here. Before one is added the group _member of parliament_ one has to be created as _user_;

  * **political groups** Add members of _political groups_. Only MP can be added to political groups;

  * **committees** Add members of _committees_. Only MP can be added to political groups;

  * **governments** Add _government/ministries/member of ministries_;

  * **title types** Add the title use in your parliament, e.g. Speaker/President/Chief Whip etc. Please note that _titles_ in all groups may be associated to a _role_ (see section on roles).


