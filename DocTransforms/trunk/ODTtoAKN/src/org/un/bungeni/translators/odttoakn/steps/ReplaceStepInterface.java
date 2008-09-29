package org.un.bungeni.translators.odttoakn.steps;

/**
 * This is the interface for the ReplaceStep Object. 
 * A replace step is a simple String replacement, having a pattern to search and the replacement string.
 */
public interface ReplaceStepInterface 
{
	/**
	 * Return the replacement of this Replace Step
	 * @return a String containing the replacement of this replace object 
	 */
	public String getReplacement();
	/**
	 * Return the pattern of this Replace Step
	 * @return a String containing the pattern of this Replace Step
	 */
	public String getPattern();
	/**
	 * Set the Replacement of this Replace Step
	 * @param aReplacement the String containing the Replacement of this  ReplaceStep
	 */
	public void setReplacement(String aReplacement);
	/**
	 * Set the pattern of this Replace Step
	 * @param aPattern a String containing the pattern of this ReplaceStep 
	 */
	public void setPattern(String aPattern);
}
