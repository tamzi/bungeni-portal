/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.bungeni.dingsoft.aspect;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.dspace.app.xmlui.cocoon.AbstractDSpaceTransformer;
import org.dspace.app.xmlui.utils.UIException;
import org.dspace.app.xmlui.wing.WingException;
import org.dspace.app.xmlui.wing.element.Body;
import org.dspace.app.xmlui.wing.element.PageMeta;
import org.dspace.authorize.AuthorizeException;
import org.xml.sax.SAXException;
 
import java.io.IOException;
import java.io.InputStream;
import java.sql.SQLException;
import java.util.Enumeration;
import java.util.Properties;
/**
 *
 * @author undesa
 */
public class BungeniPortalLinksTransformer extends AbstractDSpaceTransformer
{
    public void addBody(Body body)throws SAXException, WingException, UIException, SQLException, IOException, AuthorizeException
    {
        body.addDivision("My Division").addPara("This is text in a new paragraph");
    }
}
