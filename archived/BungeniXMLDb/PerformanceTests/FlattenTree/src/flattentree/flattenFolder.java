/*
 * Main.java
 *
 * Created on August 1, 2007, 12:51 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package flattentree;

/**
 *
 * @author ashok
 */
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.channels.FileChannel;

/**
 * Small application to take files from a directory (with sub-directories) and 
 * place them all into one directory, the files are re-named based on there
 * parent name, each parent folder name is seperated by a '.'
 * 
 * e.g. flattenFolder /home/aretter/xml /home/aretter/xml2
 * The file /home/aretter/xml/1/2/3/doc.xml would be copied
 * to /home/aretter/xml2/1.2.3.doc.xml
 * 
 * @author Adam Retter <adam.retter@googlemail.com>
 * @serial 20070612
 */

public class flattenFolder
{

	private String srcPath = null;
	private String destPath = null;
	
	public static void main(String[] args)
	{
		//check for two arguments
		if(args.length < 2)
		{
			showUseage();
			
			return;
		}
		
		new flattenFolder(args[0], args[1]);
	}
	
	private final static void showUseage()
	{
		System.out.println("\nUseage: flattenFolder <source path> <destination path>\n\n");
	}
	
	public flattenFolder(String srcPath, String destPath)
	{
		this.srcPath = srcPath;
		this.destPath = destPath;
		
		File srcFolder = new File(srcPath);
		File destFolder = new File(destPath);
		
		//create the destination if it doesnt exist
		if(!destFolder.exists())
			destFolder.mkdir();
		
		//copy the files
		recursiveCopy(srcFolder, destFolder);
	}
	
	private void recursiveCopy(File srcFolder, File destFolder)
	{
		File[] children = srcFolder.listFiles();
		
		for(int c = 0; c < children.length; c++)
		{
			if(children[c].isDirectory())
			{
				recursiveCopy(children[c], destFolder);
			}
			else if(children[c].isFile())
			{
				String destFilename	= children[c].getAbsolutePath();
                        	destFilename = destFilename.replace(srcPath + File.separatorChar, "");
				destFilename = destFilename.replace(File.separatorChar, '.');
				File destFile = new File(destFolder, destFilename);
				System.out.println("dest file = "+ destFilename);
				if(copy(children[c], destFile))
				{
					System.out.println("Copied " + children[c].getAbsolutePath() + " to " + destFile.getAbsolutePath());
				}
				else
				{
					System.err.println("FAILED to copy  " + children[c].getAbsolutePath());
				}
			}
		}
	}
	
	private boolean copy(File src, File dst)
	{
		try
		{
			if(!dst.exists())
				dst.createNewFile();
			
			// Create channel on the source
	        FileChannel srcChannel = new FileInputStream(src).getChannel();
	    
	        // Create channel on the destination
	        FileChannel dstChannel = new FileOutputStream(dst).getChannel();
	    
	        // Copy file contents from source to destination
	        dstChannel.transferFrom(srcChannel, 0, srcChannel.size());
	    
	        // Close the channels
	        srcChannel.close();
	        dstChannel.close();
		}
		catch(IOException ioe)
		{
			ioe.printStackTrace();
			System.out.println(ioe.getMessage());
			
			return false;
		}
		
		return true;
    }
}
