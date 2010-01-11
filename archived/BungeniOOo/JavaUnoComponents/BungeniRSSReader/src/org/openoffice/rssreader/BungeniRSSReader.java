package org.openoffice.rssreader;

import com.sun.star.uno.UnoRuntime;
import com.sun.star.uno.XComponentContext;
import com.sun.star.lib.uno.helper.Factory;
import com.sun.star.lang.XSingleComponentFactory;
import com.sun.star.registry.XRegistryKey;
import com.sun.star.lib.uno.helper.WeakBase;
import java.net.URL;
import java.net.URLConnection;
import java.util.logging.*;
import org.bungeni.rssparser.*;


public final class BungeniRSSReader extends WeakBase
   implements com.sun.star.lang.XServiceInfo,
              org.openoffice.rssreader.XBungeniRSSReader
{
    private final XComponentContext m_xContext;
    private static final String m_implementationName = BungeniRSSReader.class.getName();
    private static final String[] m_serviceNames = {
        "org.openoffice.rssreader.BungeniRSSReaderService" };
        Logger log;
       private RssParser m_rssParser;
    public BungeniRSSReader( XComponentContext context )
    {
        m_xContext = context;
    };

    public static XSingleComponentFactory __getComponentFactory( String sImplementationName ) {
        XSingleComponentFactory xFactory = null;

        if ( sImplementationName.equals( m_implementationName ) )
            xFactory = Factory.createComponentFactory(BungeniRSSReader.class, m_serviceNames);
        return xFactory;
    }

    public static boolean __writeRegistryServiceInfo( XRegistryKey xRegistryKey ) {
        return Factory.writeRegistryServiceInfo(m_implementationName,
                                                m_serviceNames,
                                                xRegistryKey);
    }

    // com.sun.star.lang.XServiceInfo:
    public String getImplementationName() {
         return m_implementationName;
    }

    public boolean supportsService( String sService ) {
        int len = m_serviceNames.length;

        for( int i=0; i < len; i++) {
            if (sService.equals(m_serviceNames[i]))
                return true;
        }
        return false;
    }

    public String[] getSupportedServiceNames() {
        return m_serviceNames;
    }

    // org.openoffice.rssreader.XBungeniRSSReader:
    public String OpenFeed(String feedURL)
    {
        // TODO !!!
        // Exchange the default return implementation.
        // NOTE: Default initialized polymorphic structs can cause problems
        // because of missing default initialization of primitive types of
        // some C++ compilers or different Any initialization in Java and C++
        // polymorphic structs.
        
        String warmedFeed="";
        try{
        java.net.URL obj = new URL(feedURL);
        m_rssParser = new RssParser (obj);
        //System.out.println("parsing feed");
        m_rssParser.parseFeed();
        //System.out.println("printing feed");
        
        }
            catch (Exception ex) {
            java.util.logging.Logger.getLogger("global").log(java.util.logging.Level.ALL,
                                                             ex.getMessage(), ex);
        }
        finally {
            return warmedFeed;
        }
      }  
    
      public org.openoffice.rssreader.BungeniRssHeader RssHeader() {
          return m_rssParser.rssHeader();
      }
      
      public org.openoffice.rssreader.BungeniRssRecord[] RssRecords(){
          return m_rssParser.rssRecords();
      }
              

      }  
