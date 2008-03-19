/*
 * PointNumbering.java
 *
 * Created on March 18, 2008, 1:30 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package numbering;

import java.util.ArrayList;
import java.util.ListIterator;

/**
 *
 * @author undesa
 *  class to demonstrate point numbering like 1.1 1.2
 */
public class PointNumbering {
    
    public int start;
    public int end;
    
    /** Creates a new instance of PointNumbering */
    public PointNumbering() {
    }
     public void setRange(int s, int e){
        this.start=s;
        this.end=e;
        
    }
    public int getEnd(){
        return this.end;
    }
     
    public int getStart(){
        return this.start;
    }
    
    public static void printSequence(){
        
    }
    
    public static void main(String [] args){
        PointNumbering numbererObj=new PointNumbering();
	numbererObj.setRange(1,10);
	int startRange=numbererObj.getStart();
	int endRange=numbererObj.getEnd();
	System.out.println("Start range: " + startRange + " End Range: " + endRange);
        ArrayList list=new ArrayList();
	int count=-1;
	for(int i=startRange;i<endRange;i++){
             count++;
             list.add(count,String.valueOf(i));
             for(int j=startRange;j<endRange;j++){
                 count++; // first depth
                 list.add(count,String.valueOf(i)+"."+String.valueOf(j));
                 for(int  k=startRange;k<endRange;k++){
                     count++; //second depth
                     list.add(count,String.valueOf(i)+"."+String.valueOf(j)+"."+String.valueOf(k));
                 }
             }
        }
        
        ListIterator listIterator= list.listIterator();
        while(listIterator.hasNext()){
          
            
            Object nextItem=listIterator.next();
           
         
           System.out.println(nextItem);
            
            
            
        }
    }
}
