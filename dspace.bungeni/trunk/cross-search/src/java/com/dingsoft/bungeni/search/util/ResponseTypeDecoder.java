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
 *
 * @author undesa
 */
public class ResponseTypeDecoder {
    
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
