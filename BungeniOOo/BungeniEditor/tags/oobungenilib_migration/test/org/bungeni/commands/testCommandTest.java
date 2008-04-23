/*
 * testCommandTest.java
 * JUnit based test
 *
 * Created on December 21, 2007, 11:45 AM
 */

package org.bungeni.commands;

import junit.framework.*;
import org.apache.commons.chain.Catalog;
import org.apache.commons.chain.Command;
import org.apache.commons.chain.Context;
import org.bungeni.commands.chains.BungeniCommandsCatalogLoader;

/**
 *
 * @author Administrator
 */
public class testCommandTest extends TestCase {
    BungeniCommandsCatalogLoader loader ;
    Catalog sampleCatalog;
    
    public testCommandTest(String testName) {
        super(testName);
    }

    protected void setUp() throws Exception {
               	loader = new BungeniCommandsCatalogLoader();
                sampleCatalog = loader.getCatalog("testCatalog");
    }

    protected void tearDown() throws Exception {
    }

    /**
     * Test of execute method, of class org.bungeni.commands.testCommand.
     */
    public void testExecute() throws Exception {
        System.out.println("execute");
        
        testContext context = new testContext();

        context.getFields().add("string 1");
        context.getFields().add("string 2");
        context.getKeyValuePairs().put("key 1", "key value 1");
        testCommand instance = new testCommand();
        boolean expResult = true;
        boolean result = instance.execute(context);
        assertTrue("test succeeded", result == false);
        // TODO review the generated test code and remove the default call to fail.
      //  fail("The test case is a prototype.");
    }
    
}
