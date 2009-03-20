package org.un.bungeni.translators.utility.schemavalidator;

import javax.xml.validation.TypeInfoProvider;
import javax.xml.validation.ValidatorHandler;

import org.w3c.dom.TypeInfo;
import org.w3c.dom.ls.LSResourceResolver;
import org.xml.sax.Attributes;
import org.xml.sax.ContentHandler;
import org.xml.sax.ErrorHandler;
import org.xml.sax.Locator;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;

public class LocalValidatorHandler extends DefaultHandler 
{
    int indent = 0;
    private TypeInfoProvider provider;
    public String elementName = "";
    public String elementId = "";

    public LocalValidatorHandler() 
    {
    }

    public LocalValidatorHandler(TypeInfoProvider provider) 
    {
        this.provider = provider;
    }

    /**
     * Receive notification of the start of an element.
     */
    public void startElement(String uri, String localName, String qName, Attributes attributes) throws SAXException 
    {
    	//TypeInfo etype = provider.getElementTypeInfo().;
        StringBuffer sb = new StringBuffer(100);
        
        for (int i=0; i<indent; i++) 
        {
            sb.append("  ");
        }
        sb.append("Element " + qName + " ");
        this.elementName = qName;
        
        //sb.append(" of type {" + etype.getTypeNamespace() + '}' + etype.getTypeName());
        for (int a=0; a<attributes.getLength(); a++) 
        {
        	if(attributes.getQName(a) == "id")
        	{
        		sb.append(attributes.getValue(a));
        		this.elementId = attributes.getValue(a);
        	}
             
            /*TypeInfo atype = provider.getAttributeTypeInfo(a);
            boolean spec = provider.isSpecified(a);
            sb.setLength(0);
            for (int i=0; i<indent+2; i++) 
            {
                sb.append("  ");
            }
            sb.append("Attribute " + attributes.getQName(a) + (spec ? " (specified)" : (" (defaulted)")));
            if (atype == null) 
            {
                sb.append(" of unknown type");
            } 
            else 
            {
                sb.append(" of type {" + atype.getTypeNamespace() + '}' + atype.getTypeName());
            }
            System.out.println(sb.toString()); */
        }
        System.out.println(sb.toString());
        indent++;
    }

    /**
     * Receive notification of the end of an element.
     */
    public void endElement(String uri, String localName, String qName) throws SAXException 
    {
        indent--;
    }

}
