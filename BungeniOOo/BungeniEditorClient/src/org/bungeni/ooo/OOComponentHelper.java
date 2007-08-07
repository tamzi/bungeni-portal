/*
 * OOComponentHelper.java
 *
 * Created on July 23, 2007, 6:57 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.ooo;

import com.sun.star.beans.IllegalTypeException;
import com.sun.star.beans.PropertyExistException;
import com.sun.star.beans.PropertyValue;
import com.sun.star.beans.PropertyVetoException;
import com.sun.star.beans.UnknownPropertyException;
import com.sun.star.beans.XPropertyContainer;
import com.sun.star.beans.XPropertySet;
import com.sun.star.comp.helper.Bootstrap;
import com.sun.star.comp.helper.BootstrapException;
import com.sun.star.container.XNameAccess;
import com.sun.star.container.XNamed;
import com.sun.star.document.XDocumentInfo;
import com.sun.star.document.XDocumentInfoSupplier;
import com.sun.star.frame.XController;
import com.sun.star.frame.XDispatchHelper;
import com.sun.star.frame.XDispatchProvider;
import com.sun.star.frame.XFrame;
import com.sun.star.frame.XModel;
import com.sun.star.lang.WrappedTargetException;
import com.sun.star.lang.XComponent;
import com.sun.star.lang.XMultiComponentFactory;
import com.sun.star.lang.XMultiServiceFactory;
import com.sun.star.lang.XServiceInfo;
import com.sun.star.lang.XServiceInfo;
import com.sun.star.lang.XServiceInfo;
import com.sun.star.lang.XServiceInfo;
import com.sun.star.style.XStyleFamiliesSupplier;
import com.sun.star.text.XText;
import com.sun.star.text.XTextColumns;
import com.sun.star.text.XTextContent;
import com.sun.star.text.XTextDocument;
import com.sun.star.text.XTextSectionsSupplier;
import com.sun.star.text.XTextViewCursor;
import com.sun.star.text.XTextViewCursorSupplier;
import com.sun.star.uno.Any;
import com.sun.star.uno.AnyConverter;
import com.sun.star.uno.UnoRuntime;
import com.sun.star.uno.XComponentContext;
import org.bungeni.editor.dialogs.editorTabbedPanel;

/**
 * 
 * OpenOffice component helper class.
 * This class takes an XComponent object as input, and provides various document level helper functions.
 * @author Administrator
 */
public class OOComponentHelper {
    private XComponent m_xComponent;
    private XComponentContext m_xComponentContext;
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(OOComponentHelper.class.getName());
      
    /** Creates a new instance of OOComponentHelper */
    public OOComponentHelper(XComponent xComponent, XComponentContext xComponentContext) {
          try {
            m_xComponent = xComponent;
            m_xComponentContext = xComponentContext;
        } catch (Exception ex) {
            log.debug(ex.getLocalizedMessage(), ex);
        }
    }
    
    /**
     * Queries an input Object for an XServiceInfo interface, if found, returns the interface.
     */
     public XServiceInfo getServiceInfo(Object obj){
             XServiceInfo xInfo = ooQueryInterface.XServiceInfo(obj); // UnoRuntime.queryInterface(XServiceInfo.class, obj);
             return xInfo;
   }
    
    /**
     * Gets the XTextContent from the input Object. Input object is queried for XTextContent.
     */
    public XTextContent getTextContent(Object element){
        XTextContent xContent = ooQueryInterface.XTextContent(element);//(XTextContent) UnoRuntime.queryInterface(XTextContent.class, element);
        return xContent;
    }
    /**
     * Returns the XTextDocument of the current openoffice document.
     */
  public XTextDocument getTextDocument(){
      log.debug("in getTextDocument()");
        XTextDocument xTextDoc = (XTextDocument) UnoRuntime.queryInterface(XTextDocument.class, this.m_xComponent);
       if (xTextDoc == null ) log.debug("getTextDocument() returned null");
        return xTextDoc;
    }
    
    /**
     * Gets the XModel interface of the current document controller.
     */
    public XModel getDocumentModel(){
        return (XModel)UnoRuntime.queryInterface(XModel.class, this.m_xComponent);
    }
    
    
    public XMultiServiceFactory getDocumentFactory(){
        XMultiServiceFactory xFactory = (XMultiServiceFactory) UnoRuntime.queryInterface(XMultiServiceFactory.class, this.m_xComponent);
        return xFactory;
    }
    
    public Object createInstance(String instanceName){
        Object newInstance = null;
        try {
            newInstance = getDocumentFactory().createInstance(instanceName);
        } catch (com.sun.star.uno.Exception ex) {
            log.debug("createInstance(instanceName="+instanceName+"); error message follows :"+ ex.getLocalizedMessage(), ex);
        } finally {
            return newInstance;
        }
    }
    
    public Object createInstanceWithContext(String instanceName){
       Object newInstance = null;
        try {
            newInstance = this.m_xComponentContext.getServiceManager().createInstanceWithContext("com.sun.star.frame.DispatchHelper", this.m_xComponentContext);
        } 
        catch (com.sun.star.uno.Exception ex) {
            log.debug(ex.getLocalizedMessage(), ex);
        }
        finally {
            return newInstance;
        }
   }
    
    
    public XTextContent createTextSection(String sectionName, short numberOfColumns){
       XNamed xNamedSection = null;
       XTextContent xSectionContent = null;
       try {
           //create a new section instance
           Object newSection = createInstance("com.sun.star.text.TextSection");
           //set the name
           xNamedSection = (XNamed)UnoRuntime.queryInterface(XNamed.class, newSection);
           xNamedSection.setName(sectionName);
           //XTextContent xSectionContent = (XTextContent)UnoRuntime.queryInterface(XTextContent.class, newSection);
           //create column instance, and set column count
           XTextColumns xColumns = (XTextColumns) UnoRuntime.queryInterface( XTextColumns.class, createInstance("com.sun.star.text.TextColumns")); 
           xColumns.setColumnCount(numberOfColumns);
           //set the column count to the section
           getObjectPropertySet(xNamedSection).setPropertyValue("TextColumns", xColumns);
           xSectionContent = (XTextContent) UnoRuntime.queryInterface(XTextContent.class, xNamedSection);
        } catch (PropertyVetoException ex) {
            ex.printStackTrace();
        } catch (WrappedTargetException ex) {
            ex.printStackTrace();
        } catch (com.sun.star.lang.IllegalArgumentException ex) {
            ex.printStackTrace();
        } catch (UnknownPropertyException ex) {
            ex.printStackTrace();
        } finally {
            return xSectionContent;
        }
        
    }
    
    public XPropertySet getObjectPropertySet(Object obj){
        XPropertySet xObjProps = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class, obj); 
        return xObjProps;
    }
    
    
    /**
     * Gets the current view cursor.
     */
    public XTextViewCursor getViewCursor(){
     XTextViewCursorSupplier xViewCursorSupplier = (XTextViewCursorSupplier)UnoRuntime.queryInterface(XTextViewCursorSupplier.class, getDocumentModel().getCurrentController());
     XTextViewCursor xViewCursor = xViewCursorSupplier.getViewCursor();
     return xViewCursor;
    }
    
    public XNameAccess getStyleFamilies(){
        XStyleFamiliesSupplier xStyleFamiliesSupplier = ooQueryInterface.XStyleFamiliesSupplier(getTextDocument());
        return xStyleFamiliesSupplier.getStyleFamilies();
    }
    public XDocumentInfo getDocumentInfo(){
      XDocumentInfoSupplier xdisInfoProvider =  (XDocumentInfoSupplier) UnoRuntime.queryInterface(XDocumentInfoSupplier.class, getTextDocument() );
      return  xdisInfoProvider.getDocumentInfo();
    }
    
    
    /**
     * Adds a new property to the document
     * @param propertyName Property Name to Add
     * @param value Value of property to be added
     */
    public void addProperty (String propertyName, String value){
        
         XPropertyContainer xDocPropertiesContainer = (XPropertyContainer) UnoRuntime.queryInterface(XPropertyContainer.class, getDocumentInfo());
        try {
       
            xDocPropertiesContainer.addProperty(propertyName, (short)0, new Any(com.sun.star.uno.Type.STRING, value));
        } catch (PropertyExistException ex) {
            log.debug("Property " + propertyName + " already Exists");
        } catch (com.sun.star.lang.IllegalArgumentException ex) {
            log.debug(ex.getLocalizedMessage(), ex);
        } catch (IllegalTypeException ex) {
            log.debug(ex.getLocalizedMessage(), ex);
        }
    }
    
    /**
     * Sets an existing property value to the input value.
     * @param propertyName Property name to to which value is to be set.
     * @param propertyValue Property value that is to be set.
     */
    public void setPropertyValue(String propertyName, String propertyValue) {
            XDocumentInfo xdi = getDocumentInfo();
            XPropertySet xDocProperties = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class, xdi);
            try{
               
                xDocProperties.setPropertyValue(propertyName, propertyValue);
            } catch (UnknownPropertyException ex) {
                ex.printStackTrace();
            } catch (WrappedTargetException ex) {
                ex.printStackTrace();
            } catch (com.sun.star.lang.IllegalArgumentException ex) {
                ex.printStackTrace();
            } catch (PropertyVetoException ex) {
                ex.printStackTrace();
            }
    }
    
    public String getPropertyValue(String propertyName ) throws UnknownPropertyException{
            XDocumentInfo xdi = getDocumentInfo();
            String value="";
        XPropertySet xDocProperties = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class, xdi);
        try {
             value = (String) xDocProperties.getPropertyValue(propertyName);
           /// value = anyUnoValue.toString();
        } catch (UnknownPropertyException ex) {
            log.debug("Property "+ propertyName+ " does not exit");
        } catch (WrappedTargetException ex) {
            log.debug(ex.getLocalizedMessage(), ex);
        } finally {
            return value;
        }
            
    }
    
    public XNameAccess getTextSections(){
        log.debug("in getTextSections()");
        //get the text document, XText object
        //query interface for the textsections supplier
         XTextSectionsSupplier oTSSupp = (XTextSectionsSupplier)UnoRuntime.queryInterface( XTextSectionsSupplier.class, getTextDocument() );
         XNameAccess xNamedSections = oTSSupp.getTextSections();
        if (xNamedSections == null ) 
            log.debug("getTextSections() returned null");
        else
            log.debug("getTextSections retrned : "+ (xNamedSections.hasElements()==true?"true":"false") );
        return xNamedSections;
    }
    
    public XComponent getComponent(){
        return this.m_xComponent;
    }
    public XMultiComponentFactory getRemoteServiceManager() {
        return this.m_xComponentContext.getServiceManager();
    }
    public void executeDispatch(String cmd, PropertyValue[] oProperties){
        try {

        log.debug("executeDispatch : "+ cmd);
        log.debug("executeDispatch: oProperties0 : "+ oProperties[0].Name+" , "+ oProperties[0].Value);
        log.debug("executeDispatch: oProperties1 : "+ oProperties[1].Name+" , "+ oProperties[1].Value);
        
        final XModel docModel = this.getDocumentModel();
        log.debug("executeDispath: modelURL "+ docModel.getURL() );
        log.debug("executeDispatch : getting controller");
        XController docController = docModel.getCurrentController();
        final XFrame docFrame = docController.getFrame();
        log.debug("executeDispatch : getting dispatch provider");
        XDispatchProvider docDispatchProvider = ooQueryInterface.XDispatchProvider(docFrame);
        log.debug("executeDispatch : getting dispatchhelper");
        final Object oDispatchHelper = this.getRemoteServiceManager().createInstanceWithContext("com.sun.star.frame.DispatchHelper", this.m_xComponentContext);
        if (oDispatchHelper == null ) { log.debug("executeDispatch oDispatchHelper is null!!"); }
        XDispatchHelper xdispatchHelper = ooQueryInterface.XDispatchHelper(oDispatchHelper);
        
        xdispatchHelper.executeDispatch(docDispatchProvider, cmd, "", 0, oProperties); 

        } catch (com.sun.star.uno.Exception ex){
            log.debug("error in exeucteDispatch " +ex.getLocalizedMessage(), ex);
        }
        
    }
    
    
    public void createInstance(){
       
    }
    
    
    
    public boolean propertyExists(String propertyName){
        XDocumentInfo xdi = getDocumentInfo();
        boolean bExists = false;
        XPropertySet xDocProperties = (XPropertySet) UnoRuntime.queryInterface(XPropertySet.class, xdi);
        try {
     
                Object objValue =  xDocProperties.getPropertyValue(propertyName);
                bExists = true;
                log.debug("property Exists - value : "+ AnyConverter.toString(objValue) );
            } 
        catch (com.sun.star.lang.IllegalArgumentException ex) {
                        bExists = false;
                         log.debug("propertyExists - unknown property exception");
            }
         catch (UnknownPropertyException ex) {
                 log.debug("propertyExists - unknown property exception");
                //property does not exist
                    bExists = false;
        }
        catch (WrappedTargetException ex) {
                      bExists = false;
            }
        finally {
            return bExists;
        }
     }
    
 
}
