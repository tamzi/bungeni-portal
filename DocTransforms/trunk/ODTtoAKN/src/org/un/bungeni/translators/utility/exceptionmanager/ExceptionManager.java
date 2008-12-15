package org.un.bungeni.translators.utility.exceptionmanager;

/**
 * This object parse a SAXEception understand what type of exception is and throws an 
 * user readable error
 */
public class ExceptionManager 
{
	/* The instance of this FileUtility object*/
	private static ExceptionManager instance = null;
		

	/**
	 * Private constructor used to create the ExceptionManager instance
	 */
	private ExceptionManager()
	{
		
	}
		
	/**
	 * Get the current instance of the ExceptionManager class 
	 * @return the ExceptionManager instance
	*/
	public static ExceptionManager getInstance()
	{
		//if the instance is null create a new instance
		if (instance == null)
		{
			//create the instance
			instance = new ExceptionManager();
		}
		//otherwise return the instance
		return instance;
	}
	
	/**
	 * This method parse a SAXEception understand what type of exception is and throws a 
	 * user readable error
	 * @param e
	 */
	public void parseException(Exception e) 
	{
		System.out.println(e.getMessage());
		//the message of the exception
		String exceptionMessage = e.getMessage();
		
		//check what type of text the exception launch
		if(exceptionMessage.matches("(.*)Attribute '(.*)' must appear on element '(.*)'.")) 
			return;//throw new Exception("return");
	}
}
