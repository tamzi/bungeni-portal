/*
 * BungeniClientDBTest.java
 *
 * Created on August 17, 2007, 1:11 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.db;

import java.util.Vector;

/**
 *
 * @author Administrator
 */
public class BungeniClientDBTest {
    
    /** Creates a new instance of BungeniClientDBTest */
    public BungeniClientDBTest() {
    }
    
    public static void main (String[] args) {
        BungeniClientDB db = new BungeniClientDB("e:\\projects\\WorkingProjects\\BungeniEditorClient\\dist\\settings\\db\\", "");
        if (db.Connect() ) {
        Vector<Vector> results = db.Query("select * from toolbar_action_settings");
        db.EndConnect();
        System.out.println("Results = "+ results.size());
        }
        
        
        
    }
}
