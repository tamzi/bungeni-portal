package org.bungeni.restlet.docs;

import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.net.URL;

import org.apache.log4j.Logger;
import org.bungeni.restlet.resources.OdtResource;
import org.bungeni.restlet.utils.CommonUtils;

public class Documentation {
	
	private static org.apache.log4j.Logger log =
        Logger.getLogger(Documentation.class.getName());

	
	public Documentation() {
		
	}
	
	private static File getDocumentationFile(String docPath) {
		URL url = OdtResource.class.getResource(docPath);
		File f = null;
		try {
			f = new File (url.toURI());
		} catch (URISyntaxException e1) {
			f = new File(url.getPath());
		}
		return f;
	}
	
	public static String getDocumentation(String docUrl ) {
		File fdoc = getDocumentationFile(docUrl);
		String docHtml = "";
		try {
			docHtml = CommonUtils.readTextFile(fdoc);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			log.error("getDocumentation :", e);
		}
		return docHtml;
	}
}
