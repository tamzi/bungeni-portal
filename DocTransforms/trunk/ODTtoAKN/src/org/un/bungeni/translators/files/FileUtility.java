package org.un.bungeni.translators.files;

import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;


/**
 * This class supplies several method useful for the management of the File documents
 *
 */
public class FileUtility 
{
	/* The instance of this FileUtility object*/
	private static FileUtility instance = null;
		

	/**
	 * Private constructor used to create the FileUtility instance
	 */
	private FileUtility()
	{
		
	}
		
	/**
	 * Get the current instance of the FileUtility class 
	 * @return the Utility instance
	*/
	public static FileUtility getInstance()
	{
		//if the instance is null create a new instance
		if (instance == null)
		{
			//create the instance
			instance = new FileUtility();
		}
		//otherwise return the instance
		return instance;
	}
	
	/**
	 * Write the File at the given path to a String
	 * @param aFilePath the path of the file to retrieve as a String
	 * @return the String representation of the file
	 * @throws IOException 
	 */
	public String FileToString(String aFilePath) throws IOException
	{
		//create a File Input Stream
	    FileInputStream file = new FileInputStream(aFilePath);
	    
	    //the byte array that will contains the byte of the file
	    byte[] b = new byte[file.available()];
	    
	    //read the bytes of the file
	    file.read(b);
	    
	    //close the file
	    file.close ();
	    
	    //return the string containing the content of the file
	    return new String(b);
	}
	
	/**
	 * Write the given content to the file at the given path
	 * @param aFilePath the path of the file to create
	 * @param aFileContent the content of the file to create
	 * @throws IOException
	 */
	public void StringToFile(String aFilePath,String aFileContent) throws IOException
	{
		//create the buffered Writer
		BufferedWriter out = new BufferedWriter(new FileWriter(aFilePath));
		
		//write the content of the File
		out.write(aFileContent);
		
		//close the file
		out.close();
	}
}
