/*
 * DocumentMetadata.java
 *
 * Created on October 26, 2007, 1:35 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.editor.metadata;

/**
 *
 * @author Administrator
 */
public class DocumentMetadata {

    private String Name;
    private String Type;
    private String DisplayName;
    private String DataType;
    private String Value;

    /** Creates a new instance of DocumentMetadata */
    public DocumentMetadata(String name, String type, String datatype) {
        Name = name;
        Type = type;
        DataType = datatype;
    }
    
    public void setName(String name ) {
        Name = name;
    } 
    
    public void setType(String type ) {
        Type = type;
    }
    
    public void setDisplayName(String dname) {
        this.DisplayName = dname;
    }
    
    public void setDataType (String datatype ) {
        DataType = datatype;
    }
    
    public String getName( ) {
         return Name;
    } 
    
    public String getType ( ) {
         return Type;
    }
    
    public String getDataType ( ) {
         return DataType;
    }
    
    public String toString(){
        return this.DisplayName;
    }
}
