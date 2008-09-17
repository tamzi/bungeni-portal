package org.un.bungeni.translators.odttoakn.steps;

/**
 * This is the interface for the step objects of the ODTtoAKN translator. 
 * A step contains all the informations related to a particular step of the translation.
 */
public interface StepInterface 
{
	/**
	 * Set the name of a Step 
	 * @param aName the name that you want to assign to a Step
	 */
	public void setName(String aName);
	/**
	 * Set the URI of a step. 
	 * @param aURI the path of the XSLT regarding the step to perform
	 */
	public void setHref(String aURI);
	/**
	 * An integer containing the position of the step. 
	 * @param aPosition the integer of the position of the step. The step of the configurations 
	 * 		            are resolved performing all the Steps of the configurations. The step 
	 * 					with the lowest position number is performed firstly.   
	 */
	public void setPosition(Integer aPosition);
	
	/**
	 * Used to get the name of the Step 
	 * @return the name of the Step
	 */
	public String getName();

	/**
	 * Used to get the href of the Step 
	 * @return the href of the Step
	 */
	public String getHref();
	
	/**
	 * Used to get the position of the Step. The step of the configurations 
	 * are resolved performing all the Steps of the configurations. The step 
	 * with the lowest position number is performed firstly. 
	 * @return the position of the Step
	 */
	public Integer getPosition();
}
