Description

    DotNetTheme is an example for DIYPloneStyle.

Installation

    Place DotNetTheme in the Products directory of your Zope instance
    and restart the server.

    In the ZMI, go to 'portal_setup' and, (1) select the 'Properties' tab and
    choose 'DotNetTheme' in the popup list before clicking 'Update'.
    Then (2) go to the 'Import' tab and click 'Import all steps'.

    While adding a Plone Site to Zope (from the ZMI), you can select
    DotNetTheme in the proposed Extension Profiles to have it installed
    automatically during the creation of the portal.

    You may have to empty your browser cache to see the effects of the
    product installation.

    Uninstall -- This must be done manually from the ZMI, as GenericSetup does
    not yet have a complete API for removing/uninstalling stuff.

Selecting a skin

    Depending on the values given in the skins tool profile (see
    profiles/default/skins.xml), the skin will be selected (or not) as default
    one while installing the product. If you need to switch from a default
    skin to another, go to the 'Site Setup' page, and choose 'Skins' (as
    portal manager). You can also decide from that page if members can choose
    their preferred skin and, in that case, if the skin cookie should be
    persistent.

    Note -- Don't forget to perform a full refresh of the page or reload all
    images (not from browser cache) after selecting a skin. In Firefox, you
    can do so by pressing the 'shift' key while reloading the page. In IE, use
    the key combination <Ctrl-F5>.

Written by

    David Convent <davconvent _'at'_ gmail.com>
