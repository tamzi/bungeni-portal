
# Customizing the Portal Portal #

## Public Portal ##

The Public Portal of Bungeni provides a long term archive of publicly accessible Parliamentary documents.

The Public Portal is the final resting place of all Documents produced in the Bungeni system and also archives information from past parliaments.

Additionally there is a need to maintain a separation of systems and data between what is running inside Parliament and what is accessed by the general public over the internet. The public portal provides this separation by maintaining a distinct archive of published parliamentary documents and parliamentary metadata.


## Accessing the Public Portal ##

For developer and admin purposes you will need to access the institutional portal directly. By default it runs on port 8088 - to access the institutional portal interface directly use the URL :

```
http://localhost:8088/exist/apps/framework/bungeni/
```

You will see a screen like the below -

![http://bungeni-portal.googlecode.com/files/xml_ui_main.jpg](http://bungeni-portal.googlecode.com/files/xml_ui_main.jpg)


If you browse the business and members section you will see the content from the publicly accessible **business** and **members** section of Bungeni.

e.g. - the following is the business section :

![http://bungeni-portal.googlecode.com/files/xml_ui_business.jpg](http://bungeni-portal.googlecode.com/files/xml_ui_business.jpg)

The admin ui for the Bungeni reposiory portal allows customizing this user interface.


## Security Considerations ##

The customization Admin UI is accessed using a web browser. The public portal by default listens only on the localhost. It is very important for security reasons that you do not provide direct public access to the repository portal. It is good practice to provide only 'localhost' access and proxy the content. For admin purposes you may open access to a specific IP directly to the system - most firewalls support local proxying for specific IPs, so you can access a local service remotely.

## Accessing the Admin/Customization UI ##


The Admin UI is accessed over the web browser :

```
http://localhost:8088/exist/apps/framework/bungeni/admin
```

Enter the admin user name and password and you will get the preliminary screen of the Admin UI :

![http://bungeni-portal.googlecode.com/files/admin_ui_main.jpg](http://bungeni-portal.googlecode.com/files/admin_ui_main.jpg)

There are various tabs allowing you to customize different aspects of the system.


## Application Customization ##

### Customizing top level Menu and Navigation ###

Click on Navigation and a screen _Navigation Configuration UI_ like the below appears :

![http://bungeni-portal.googlecode.com/files/xml_ui_nav_ui.jpg](http://bungeni-portal.googlecode.com/files/xml_ui_nav_ui.jpg)

This screen lets you customize the navigation ; if you notice on the screenshot above there are items corresponding to the home, business and members menu items below :

![http://bungeni-portal.googlecode.com/files/xml_ui_main.jpg](http://bungeni-portal.googlecode.com/files/xml_ui_main.jpg)

To edit the `business` navigation, click on `business` in the _Navigation Configuration UI_ and click `load selected`, This will load the sub-navigation for editing :

![http://bungeni-portal.googlecode.com/files/admin_ui_edit_subnav.jpg](http://bungeni-portal.googlecode.com/files/admin_ui_edit_subnav.jpg)

You will notice here that the items available for editing : `whats on`, `committees`, `bills` etc are the same ones that appear in the `business` section of the public portal :

![http://bungeni-portal.googlecode.com/files/xml_ui_business.jpg](http://bungeni-portal.googlecode.com/files/xml_ui_business.jpg)

To change the label for an item - e.g. if you want to change the label for the committees link to offices - edit the field called `Default Name` in the `committees` subnavigation form - change it to e.g. 'offices' :

![http://bungeni-portal.googlecode.com/files/xml_ui_edit_sub_nav.jpg](http://bungeni-portal.googlecode.com/files/xml_ui_edit_sub_nav.jpg)

and then click `apply changes` at the bottom of the form to save changes to the sub-navigation.

![http://bungeni-portal.googlecode.com/files/apply_changes_sub-nav.png](http://bungeni-portal.googlecode.com/files/apply_changes_sub-nav.png)

and then finally click `save changes` on the main navigation selector.

![http://bungeni-portal.googlecode.com/files/apply_changes_main-nav.png](http://bungeni-portal.googlecode.com/files/apply_changes_main-nav.png)

Now if you browse to the public portal UI you will see the link text has changed :

![http://bungeni-portal.googlecode.com/files/offices_link_edit_name.png](http://bungeni-portal.googlecode.com/files/offices_link_edit_name.png)

Note: the `href` property maps to a url in the public portal. Creating new URLs requires developer knowledge of the public portal. The `href` property is also known as a `route` further below in `route` configuration.

### Changing Listing Behaviors ###

The listing behavior of the XML UI can be changed in the following ways globally :
  * The number of items to be shown per page in a listing
  * The number of pages to show links to for paged listings.

For example, the default behavior is to show 15 items per listing (`page limit`) and 3 linked pages on the listing page (`pagination count`) :

![http://bungeni-portal.googlecode.com/files/listing_questions.png](http://bungeni-portal.googlecode.com/files/listing_questions.png)

These properties can be set via the `Pagination Preferences` screen :

![http://bungeni-portal.googlecode.com/files/pagination_preferences.png](http://bungeni-portal.googlecode.com/files/pagination_preferences.png)

Changing the properties to as shown in the screen above the screen ; `page limit` to 3 and `pagination count` to 2 results in the listing page appearing as follows :

![http://bungeni-portal.googlecode.com/files/xml_ui_edited_pagination.png](http://bungeni-portal.googlecode.com/files/xml_ui_edited_pagination.png)

More advanced listing behavior customizations are also possible;

Listing behavior can also be changed per content type by using the `Order Configuration` screen :

![http://bungeni-portal.googlecode.com/files/order_by_config.png](http://bungeni-portal.googlecode.com/files/order_by_config.png)

This `Order Configuration` allows changing listing ordering behavior per content type.

In the example above, the `Order Configuration` is being used to edit the ordering behavior for the `Question` content type.

The `Question` content type supports 4 different kinds of ordering - these are listed as submission date(oldest and newest), status date (oldest and newest ) . Using the forms the order behavior can be changed. Listing ordering is available on all listing screens :

![http://bungeni-portal.googlecode.com/files/ordering_selection.png](http://bungeni-portal.googlecode.com/files/ordering_selection.png)

To add new methods of ordering (lets say by a different element in the XML document) requires developer knowledge, and is not accessible via configuration.

### Changing Navigation and Page Titles ###

Pages resolve to urls, and urls are internally represented in the public portal as **routes**.
Indivdual routes can be configured via `route configuration`

![http://bungeni-portal.googlecode.com/files/route_config.png](http://bungeni-portal.googlecode.com/files/route_config.png)

A route property includes the `title` this is the title of the page that the route resolves to.
A route allows specifying a navigation and sub-navigation. The navigation and sub-navigation let the indicate under what active navigation (home, business or members ) and what active sub-navigation (e.g. commitees, whats on, bills, questions ...) the specified route falls under.

![http://bungeni-portal.googlecode.com/files/route_config_edit.png](http://bungeni-portal.googlecode.com/files/route_config_edit.png)

### Customizing Search on Content Types ###

Configuring search is similar to configuring listings. In the user interface `search` option works hand in hand with the listing ordering option :

![http://bungeni-portal.googlecode.com/files/search_ui.png](http://bungeni-portal.googlecode.com/files/search_ui.png)

However unlike the ordering behavior, new `search` behavior can be added via configuration per content type.

![http://bungeni-portal.googlecode.com/files/search_ui_config.png](http://bungeni-portal.googlecode.com/files/search_ui_config.png)

In the config screen above the specific XPath for the search is configured via the `Search Path` parameter.
This however still requires an index on the specific Xpath to be create in the XML database. To see how to configure indexes in eXist [see here](http://www.exist-db.org/exist/indexing.xml#idxconf).


