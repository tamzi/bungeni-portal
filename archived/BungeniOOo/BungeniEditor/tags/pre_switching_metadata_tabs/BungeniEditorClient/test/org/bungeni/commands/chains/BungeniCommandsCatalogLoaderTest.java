/*
 * BungeniCommandsCatalogLoaderTest.java
 * JUnit based test
 *
 * Created on December 21, 2007, 10:52 AM
 */

package org.bungeni.commands.chains;

import junit.framework.*;
import org.apache.commons.chain.Catalog;
import org.apache.commons.chain.Command;
import org.apache.commons.chain.Context;
import org.apache.commons.chain.config.ConfigParser;
import org.apache.commons.chain.impl.CatalogFactoryBase;
import org.bungeni.editor.selectors.BungeniFormContext;

/**
 *
 * @author Administrator
 */
public class BungeniCommandsCatalogLoaderTest extends TestCase {
    BungeniCommandsCatalogLoader loader ;
    Catalog sampleCatalog;
    public BungeniCommandsCatalogLoaderTest(String testName) {
        super(testName);
    }

    protected void setUp() throws Exception {
        	loader = new BungeniCommandsCatalogLoader();

    }

    protected void tearDown() throws Exception {
    }

    /**
     * Test of getCatalog method, of class org.bungeni.commands.chains.BungeniCommandsCatalogLoader.
     */
    public void testGetCatalog() throws Exception {
        System.out.println("getCatalog");
        
        
        Catalog expResult = null;
        sampleCatalog = loader.getCatalog("testCatalog");
        
        assertTrue("Test Succeeded", sampleCatalog != expResult );
  
        // TODO review the generated test code and remove the default call to fail.
       // fail("The test case is a prototype.");
    }

    
}
