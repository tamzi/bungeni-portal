package org.un.bungeni.translators.odttoakn.steps;

/**
 * This is the interface for the map step object
 * A map step object is an object used to store each element of the mapping files
 */
public interface MapStepInterface 
{
	/**
	 * This method is used to get the id attribute of a map Step
	 * @return the id attribute of a map Step
	 */
	public Integer getId();
	/**
	 * This method is used to get the type attribute of a map Step
	 * @return the type attribute of a map Step
	 */
	public String getType();
	/**
	 * This method is used to get the name attribute of a map Step
	 * @return the name attribute of a map Step
	 */
	public String getName();
	/**
	 * This method is used to get the bungeniSectionType attribute of a map Step
	 * @return the bungeniSectionType attribute of a map Step
	 */
	public String getBungeniSectionType();
	/**
	 * This method is used to get the result attribute of a map Step
	 * @return the result attribute of a map Step
	 */
	public String getResult();
	/**
	 * This method is used to get the  attribute operations  of a map Step
	 * @return the result attribute of a map Step
	 */
	public String getAttributes();
}
