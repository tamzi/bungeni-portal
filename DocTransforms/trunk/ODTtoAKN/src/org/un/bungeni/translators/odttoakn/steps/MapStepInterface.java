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
	/**
	 * Set the id attribute of a step to the given type. 
	 * @return the string that contains all the operation to be done on the attributes of a particular element 
	 */
	public void setId(Integer anStepId);
	/**
	 * Set the type attribute of a step to the given type. 
	 * @param aStepType the new type of the step 
	 */
	public void setType(String aStepType);
	/**
	 * Set the name attribute of a step to the given name. 
	 * @param aStepType the new name of the step 
	 */
	public void setName(String aStepName);
	/**
	 * Set the bungeniSectionTypeAttribute of the step to the given bungeniSectionType
	 * @param aStepBungeniSectionType the new bungeniSectionType of the step 
	 */
	public void setBungeniSectionType(String aStepBungeniSectionType);
	/**
	 * Set the result of the step to the given result
	 * @param aStepResult the new result of the step 
	 */
	public void setResult(String aStepResult);
	/**
	 * Set the operation that will be done on the attributes
	 * @param aStepAttributes the string that contains all the operation to be done on the attributes of a particular element 
	 */
	public void setAttributes(String aStepAttributes);
}
