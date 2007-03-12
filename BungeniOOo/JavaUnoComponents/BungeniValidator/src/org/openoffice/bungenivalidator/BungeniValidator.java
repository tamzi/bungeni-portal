package org.openoffice.bungenivalidator;

import com.sun.star.uno.UnoRuntime;
import com.sun.star.uno.XComponentContext;
import com.sun.star.lib.uno.helper.Factory;
import com.sun.star.lang.XSingleComponentFactory;
import com.sun.star.registry.XRegistryKey;
import com.sun.star.lib.uno.helper.WeakBase;
import org.bungeni.bungeniruleparser.RuleXMLElement;
import org.bungeni.bungeniruleparser.RuleXMLValidator;


/*
 * This is the public service interface class for the Java component.abstract .
 * This class acts as the proxy to the rest of the functionality packaged in this java compoennt. 
 * 
 * The main package : org.bungeni.bungeniruleparser is called from this class.
 * 
 * The bungeniruleparser class has three main classes -
 *  - RuleXMLElement - this defines the base Rule element structure in the BungeniRule.xml file
 * 
 *  - RuleXMLIterator - this is the main iterator class that operates on RuleXMLElement
 * 
 *  - RuleXMLValidator - this is the main controller class that integrates the iterator and the validator
 * 
 * 
 * 
 * 
 * 
 * 
 * 
 * 
 */

public final class BungeniValidator extends WeakBase
   implements com.sun.star.lang.XServiceInfo,
              org.openoffice.bungenivalidator.XBungeniValidator
{
    private final XComponentContext m_xContext;
    private static final String m_implementationName = BungeniValidator.class.getName();
    private static final String[] m_serviceNames = {
        "org.openoffice.bungenivalidator.BungeniValidatorService" };
    private RuleXMLValidator rxvObj; 

    public BungeniValidator( XComponentContext context )
    {
        m_xContext = context;
    };

    public static XSingleComponentFactory __getComponentFactory( String sImplementationName ) {
        XSingleComponentFactory xFactory = null;

        if ( sImplementationName.equals( m_implementationName ) )
            xFactory = Factory.createComponentFactory(BungeniValidator.class, m_serviceNames);
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

    // org.openoffice.bungenivalidator.XBungeniValidator:
    public String CheckElement(String StyleName)
    {
        // TODO !!!
        // Exchange the default return implementation.
        // NOTE: Default initialized polymorphic structs can cause problems
        // because of missing default initialization of primitive types of
        // some C++ compilers or different Any initialization in Java and C++
        // polymorphic structs.
        String strCheckElement = "";
        strCheckElement = rxvObj.checkElement(StyleName);
        
        return strCheckElement;
    }

     public String About(int StyleName)
    {
        // TODO !!!
        // Exchange the default return implementation.
        // NOTE: Default initialized polymorphic structs can cause problems
        // because of missing default initialization of primitive types of
        // some C++ compilers or different Any initialization in Java and C++
        // polymorphic structs.
        return new String("About BungeniValidator");
    }
    
     public void InitRules(String ruleFile){
         //Init rule xml validator object....
         
         rxvObj = new RuleXMLValidator(ruleFile);
         
         
     }
     
     public String[] ValidElements(){
        return rxvObj.keys();
       
     }
     
    public org.openoffice.bungenivalidator.BungeniRuleElement GetElement(String StyleName)
    {
        // TODO !!!
        // Exchange the default return implementation.
        // NOTE: Default initialized polymorphic structs can cause problems
        // because of missing default initialization of primitive types of
        // some C++ compilers or different Any initialization in Java and C++
        // polymorphic structs.
        RuleXMLElement rxe= new RuleXMLElement ();
        rxe = rxvObj.getElement(StyleName);
        if (rxe == null)
            return null;
        else
            return rxe.toBungeniRuleElement(); 
    }
     
}
