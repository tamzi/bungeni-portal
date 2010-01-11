/*
 * ResolveDTD.java
 *
 * Created on October 6, 2007, 12:38 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.odtransform;

import org.xml.sax.EntityResolver;
import org.xml.sax.InputSource;
import java.io.StringReader;

public class ResolveDTD implements EntityResolver {
	public InputSource resolveEntity (String publicId, String systemId)
	{
		if (systemId.endsWith(".dtd"))
		{
			StringReader stringInput =
				new StringReader(" ");
			return new InputSource(stringInput);
		}
		else
		{
			return null;	// default behavior
		}
	}
}
 
