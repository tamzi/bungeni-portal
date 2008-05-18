/*
 * OOoNumberingHelper.java
 *
 * Created on May 18, 2008, 8:52 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.numbering.ooo;

import java.util.HashMap;
import org.bungeni.ooo.OOComponentHelper;

/**
 *
 * @author Administrator
 */
public class OOoNumberingHelper {
       
    public static HashMap<String, String> numberingMetadata =
            new HashMap<String,String>()  {
                {
                    put("APPLIED_NUMBER", "BungeniAppliedNumber" );
                    put("NUMBERING_SCHEME", "BungeniNumberingScheme" );
                    put("PARENT_PREFIX_NUMBER", "BungeniParentPrefix");
                }
    };
    
    public static String NUMBERING_SEPARATOR_DEFAULT=".";

    /** Creates a new instance of OOoNumberingHelper */
    public OOoNumberingHelper() {
    }
    
    public static String getSectionAppliedNumber(OOComponentHelper ooDoc, String sectionName) {
        String appliedNumber = "";
        HashMap<String,String> sectionMeta = ooDoc.getSectionMetadataAttributes(sectionName);
        if (sectionMeta.containsKey(numberingMetadata.get("APPLIED_NUMBER"))) {
            appliedNumber = sectionMeta.get(numberingMetadata.get("APPLIED_NUMBER"));
        }
        return appliedNumber ;
    }
    
    
}
