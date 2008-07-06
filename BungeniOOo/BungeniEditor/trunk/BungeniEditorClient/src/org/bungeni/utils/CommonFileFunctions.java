/*
 * CommonFileFunctions.java
 * 
 * Created on Jun 4, 2007, 10:01:12 AM
 * 
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.utils;


import java.io.File;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.filechooser.FileFilter;

/**
 *
 * @author Administrator
 */
public class CommonFileFunctions {
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(CommonFileFunctions.class.getName());

    public CommonFileFunctions() {
    }

 public static String getLocalDirName()
   {
      String localDirName;     

      //Use that name to get a URL to the directory we are
      java.net.URL myURL = CommonFileFunctions.class.getClass().getResource(getClassName());  //Open a URL to the our .class file     

      localDirName = myURL.getPath();  //Strip path to URL object
      localDirName = myURL.getPath().replaceAll("%20", "");  //change %20 chars to spaces     
      //Get the current execution directory
      localDirName = localDirName.substring(0,localDirName.lastIndexOf("/"));  //clean off the file
      return localDirName;
   }
 
public  static String  getClassName()
   {
       String thisClassName="";     

      //Build a string with executing class's name
      thisClassName = CommonFileFunctions.class.getName();
      thisClassName = thisClassName.substring(thisClassName.lastIndexOf(".") + 1,thisClassName.length());
      thisClassName += ".class";  

      return thisClassName;
   }

public static File getFileFromChooser(String basePath, FileFilter filter, int fileSelectionMode, JFrame pFrame) {
        File returnFile = null;
        try {
        final JFileChooser fc = new JFileChooser(basePath);
        fc.setFileFilter(filter);
        fc.setFileSelectionMode(fileSelectionMode);
        int nReturnVal = fc.showOpenDialog(pFrame);
        if (nReturnVal == JFileChooser.APPROVE_OPTION) {
                returnFile = fc.getSelectedFile();
                return returnFile; 
            } 
        } catch (Exception ex) {
            log.error("getFileFromChooser :" + ex.getMessage());
        } finally {
            return returnFile;
        }
}


}
