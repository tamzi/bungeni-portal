/*
 * CommonFileFunctions.java
 * 
 * Created on Jun 4, 2007, 10:01:12 AM
 * 
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.utils;

/**
 *
 * @author Administrator
 */
public class CommonFileFunctions {

    public CommonFileFunctions() {
    }

 public  String getLocalDirName()
   {
      String localDirName;     

      //Use that name to get a URL to the directory we are
      java.net.URL myURL = this.getClass().getResource(getClassName());  //Open a URL to the our .class file     

      localDirName = myURL.getPath();  //Strip path to URL object
      localDirName = myURL.getPath().replaceAll("%20", "");  //change %20 chars to spaces     
      //Get the current execution directory
      localDirName = localDirName.substring(0,localDirName.lastIndexOf("/"));  //clean off the file
      return localDirName;
   }
 
public  String  getClassName()
   {
       String thisClassName="";     

      //Build a string with executing class's name
      thisClassName = this.getClass().getName();
      thisClassName = thisClassName.substring(thisClassName.lastIndexOf(".") + 1,thisClassName.length());
      thisClassName += ".class";  

      return thisClassName;
   }

}
