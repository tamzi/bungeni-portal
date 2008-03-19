/*
 * NumberRange.java
 *
 * Created on March 18, 2008, 12:46 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package numberingscheme.impl;

/**
 * NumberRange class, stores range information, starting ,ending.
 * @author Ashok
 */
public class NumberRange {
    public long start;
    public long end;
    /** Creates a new instance of NumberRange */
    public NumberRange() {
        start= (long) 1;
        end = (long) 10;
    }
    public NumberRange(long s, long e) {
       setRange(s, e);
    }
    public void setRange (long s, long e) {
        start = s;
        end = e;
    }
}
