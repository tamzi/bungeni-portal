/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.dingsoft.bungeni.search.util;

import com.dingsoft.bungeni.search.*;
import java.util.ArrayList;
import java.util.Iterator;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
/**
 *A utility class to aid in the determination of the type of response dspace or koha
 *  and to define some reference constants for the various types of responses
 * @author undesa
 */
public class ResponseTypeDecoder {
    
    /**
     * Utility method that returns an integer indicating the response type of a response
     * .The return value is one of the constants for response types defined in the <code>ResponseConstants</code>
     * class
     * @param document The Document object representing the search result
     * @return int A value representing the type of response.
     * <p>Utility method that returns an integer indicating the response type of a response
     * .The return value is one of the constants for response types defined in the <code>ResponseConstants</code>
     */
    public static int getResponseTypeForDocument(Document document)
    {
        ArrayList fields=new ArrayList(document.getFields());
        Iterator itor=fields.iterator();
        while(itor.hasNext())
        {
            Field tempField=(Field)itor.next();
            if(tempField.name().equalsIgnoreCase("DSIndexer.lastIndexed"))
            {
                return ResponseConstants.DSPACE_RESPONSE;
            }
            else if(tempField.name().equalsIgnoreCase("record"))
            {
                return ResponseConstants.KOHARESPONSE;
            }
            else
            {
                return ResponseConstants.UNKNOWNRESPONSE;
            }
        }
        return ResponseConstants.UNKNOWNRESPONSE;
    }
}
