ploned.ui
---------

A port of the plone 3 user interface to zope 3, in the form
of a new ui layer.

What works
----------
 - css 
 - viewlets

What doesn't work
-----------------
 - kss

Components
----------

Several zope3 components were developed to emulate the CMF Skin implementation and 
allow for parallel development of zope3 skins and plone 3 skins.

Namely SkinDirectoryResources were implemented to, allow for specification of similiarly
named resources directories in different layers, which allow for the specification of lookup. 
(aside, a nice extension/feature would be to automatically do lookup based on bases of the 
currently registered under layer.. we use an explicit specifiation instead).

Using this mechanism for example it is possible to have multiple css resource directories, 
that stack like transparency sheets as is done for cmf skins. This is similiar to the more 
formal notion of skinning and layering that was present in zope3, but depreceated (3.4) in
favor of the simplicity of the relying on the base primitives of the component architecture.

To support the css style currently used in plone3, required the addition of a DTML based
resource, and support for property files. There is no acquisition support and different
apis involved so some minor modifications are required to css files. namely

 - 


 
