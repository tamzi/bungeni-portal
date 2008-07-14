/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.dingsoft.bungeni.search;

/**
 *
 * Class defining the constants that govern the rules on how to decode responses from 
 * the lucene search results
 * @author undesa
 * <p>Class defining the constants that govern the rules on how to decode responses from.
 * This class contains constants for distinguishing reponses e.g. Koha from Dspace and might include other
 * constants holding other relevant info depending on a certain usage context
 */
public class ResponseConstants {
    /**
     * A constant to represent a DSpace Search result
     */
    public static final int DSPACE_RESPONSE=1;
    /**
     * A constant to represent a Koha Search result
     */
    public static final int KOHARESPONSE=2;
    /**
     * A constant to represent an Unknown response. This is here for security purposes just in case
     *  something unexpected happens or the index gets corrupted
     */
    public static final int UNKNOWNRESPONSE=-1;
}
