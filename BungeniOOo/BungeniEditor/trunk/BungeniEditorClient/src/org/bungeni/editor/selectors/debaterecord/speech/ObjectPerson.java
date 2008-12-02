/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.editor.selectors.debaterecord.speech;

/**
 *
 * @author undesa
 */
public class ObjectPerson {
    String personId ;
    String firstName;
    String lastName;
    String personURI;
    public ObjectPerson(String pId, String fName, String lName, String uri) {
        this.personId = pId;
        this.firstName = fName;
        this.lastName = lName;
        this.personURI = uri;
    }
    
    @Override
    public String toString(){
        return lastName + ", " + firstName;
    }
}
