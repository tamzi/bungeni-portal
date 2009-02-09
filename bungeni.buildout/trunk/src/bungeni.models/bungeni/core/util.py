
import config

from sqlalchemy import create_engine
from zope.configuration import xmlconfig 

zcml_slug = """\
<configure xmlns="http://namespaces.zope.org/zope"
           xmlns:db="http://namespaces.objectrealms.net/rdb">

  <include package="ore.alchemist" file="meta.zcml"/>
  <include package="alchemist.catalyst" file="meta.zcml"/>

  <!-- Setup Database Connection -->
  <db:engine
     name="bungeni-db"
     url="%s"
     />
     
  <db:bind
     engine="bungeni-db"
     metadata="bungeni.core.metadata" />

  <db:bind
     engine="bungeni-db"
     metadata="alchemist.security.metadata" />     

  <!-- Setup Core Model --> 
  <include package="bungeni.core" file="catalyst.zcml"/>
 
</configure>
"""%( config.DATABASE_URL )

     
def cli_setup( **kw ):
    """ commonly used by cli scripts for bootstrapping the database
    environment """
    db = create_engine( config.DATABASE_URL, **kw )
    mdset = []
    
    from bungeni.core.schema import metadata
    metadata.bind = db
    mdset.append( metadata )
    
    from alchemist.security.schema import metadata
    metadata.bind = db
    mdset.append( metadata )    

    from marginalia.schema import metadata
    metadata.bind = db
    mdset.append( metadata )    

    return mdset

def zcml_setup( **kw ):
    """ alot of our models dependencies depend on catalyzing models,
    this function ensures this for cli scripts"""

    xmlconfig.string( zcml_slug )
    

    
