/*
 * BungeniCommandsCatalogLoader.java
 *
 * Created on December 20, 2007, 1:06 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.commands.chains;

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
public class BungeniCommandsCatalogLoader {
	private static  String CONFIG_FILE = 
		"/org/bungeni/commands/chains/commandChain.xml";
	private ConfigParser parser;
	private Catalog catalog;
	
	public BungeniCommandsCatalogLoader() {
		parser = new ConfigParser();
	}

        public BungeniCommandsCatalogLoader(String catalogSource) {
                parser = new ConfigParser();
                CONFIG_FILE = catalogSource;
        }
        public Catalog getCatalog() throws Exception {
		if (catalog == null) {
                    parser.parse(this.getClass().getResource(CONFIG_FILE));		
		}
		catalog = CatalogFactoryBase.getInstance().getCatalog();
		return catalog;
	}
        
        public Catalog getCatalog(String catalogName) throws Exception {
		if (catalog == null) {
                    parser.parse(this.getClass().getResource(CONFIG_FILE));		
		}
		catalog = CatalogFactoryBase.getInstance().getCatalog(catalogName);
		return catalog;
	}
        
        
	public static void main(String[] args) throws Exception {
		BungeniCommandsCatalogLoader loader = new BungeniCommandsCatalogLoader();
		Catalog sampleCatalog = loader.getCatalog("debaterecord");
		Command command = sampleCatalog.getCommand("debateRecordInsertMasthead");
                //Context ctx = new BungeniFormContext();
		//command.execute(ctx);
	}
}