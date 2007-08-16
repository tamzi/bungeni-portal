/*
 * SettingsDbTest.java
 * JUnit based test
 *
 * Created on August 15, 2007, 6:52 PM
 */

package org.bungeni.utils;

import junit.framework.*;
import java.io.File;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.HashMap;
import java.util.Vector;

/**
 *
 * @author Administrator
 */
public class SettingsDbTest extends TestCase {
    SettingsDb db;
    
    public SettingsDbTest(String testName) {
        super(testName);
    }

    protected void setUp() throws Exception {
    
    }

    protected void tearDown() throws Exception {
    }

    public SettingsDb testConnect() {
        System.out.println("attempint to connect");
        String path = "dist\\settings\\db";
        SettingsDb.setDbPath(path);
        SettingsDb instance = new SettingsDb();
        
        return instance;
    }

    /**
     * Test of setDbPath method, of class org.bungeni.utils.SettingsDb.
     */
    public void testSetDbPath() {
        System.out.println("setDbPath");
        db = testConnect();
        // TODO review the generated test code and remove the default call to fail.
        this.assertTrue("tests failed", db.isConnected());
    }

    /**
     * Test of query method, of class org.bungeni.utils.SettingsDb.
     */
    public void testQuery() {
        System.out.println("query");
        
        String expression = "";
        db = testConnect();
        if (db.isConnected()) { 
        HashMap expResult = null;
        HashMap result = db.query("select * from toolbar_action_settings");
        System.out.println("size of query resultset = "+ result.size());
        assertTrue("tests failed", result.size() > 0);
        return;
        }
        fail("tests failed");
    }
  /**
     * Test of shutdown method, of class org.bungeni.utils.SettingsDb.
     */
    public void testShutdown() throws SQLException{
        System.out.println("shutdown");
        db = testConnect();
        if (db.isConnected()) {
        db.shutdown();
        assertTrue("tests failed", true);
        return;
        }
        fail("tests failed");
    }
 }
    
    