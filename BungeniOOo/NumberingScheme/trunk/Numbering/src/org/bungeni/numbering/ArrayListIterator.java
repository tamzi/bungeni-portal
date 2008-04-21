/*
 * ArrayListIterator.java
 *
 * Created on March 13, 2008, 5:03 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.numbering;

import java.util.ArrayList;
import java.util.ListIterator;

/**
 *
 * @author undesa
 */
public class ArrayListIterator {
    
     public static void main(String[] args) {
    ArrayList<String> words = new ArrayList<String>();
    words.add("first");
    words.add("second");
    words.add("third");
    words.add("fourth");
 
    int loop = 0;
    for (ListIterator i = words.listIterator(); i.hasNext(); loop++) {
      System.out.println(loop + ": " + i.next()); //get next(first) item in loop and go in front of next(second) item in loop
      System.out.println(loop + ": " + i.previous()); //get previous(first) item in loop and go in front of previous(before first) item in loop
      System.out.println(loop + ": " + i.next()); //get next(first) item in loop and go in front of next(second) item in loop
    }
 
    System.out.println("=======================================");
 
    loop = 0;
    for (ListIterator i = words.listIterator(); i.hasNext(); loop++) {
      System.out.println(loop + ": " + i.next()); //get next(first) item in loop and go in front of next(second) item in loop
      System.out.println(loop + ": " + i.previous()); //get previous(first) item in loop and go in front of previous(before first) item in loop
      if (i.hasPrevious()) {
         System.out.println(loop + ": " + i.previous()); //get previous(before first) item in loop and go in front of previous(before before first) item in loop
         System.out.println(loop + ": " + i.next()); //get next(before first) item in loop and go in front of next(first) item in loop
      }
      System.out.println(loop + ": " + i.next()); //get next(first) item in loop and go in front of next(second) item in loop
    }
  }
    
}
