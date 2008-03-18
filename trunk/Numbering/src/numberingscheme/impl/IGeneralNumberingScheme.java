/*
 * IGeneralNumberingScheme.java
 *
 * Created on March 18, 2008, 2:44 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package numberingscheme.impl;

import java.util.ArrayList;

/**
 * General numbering scheme interface, all numbering scheme classes need to implement this interface (apart form extending BaseNumberingScheme)
 * @author Ashok
 */
public interface IGeneralNumberingScheme {
    public void setRange(NumberRange range);
    public void generateSequence();
    public ArrayList<String> getGeneratedSequence();
}
