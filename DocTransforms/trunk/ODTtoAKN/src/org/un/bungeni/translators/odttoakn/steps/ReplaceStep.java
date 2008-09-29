package org.un.bungeni.translators.odttoakn.steps;

/**
 * This is the ReplaceStep Object. 
 * A ReplaceStep is a simple String replacement, having a pattern to search and the replacement string.
 */
public class ReplaceStep implements ReplaceStepInterface
{
	//the replacement of this ReplaceStep
	private String replacement;
	
	//the pattern of this ReplaceStep 
	private String pattern;
	
	/**
	 * Create a new ReplaceStep having the given replacement and the given pattern
	 * @param aReplacement the replacement String for the new ReplaceStep
	 * @param aPattern the pattern String for the new ReplaceStep
	 */
	public ReplaceStep(String aReplacement, String aPattern)
	{
		//set the replacement
		this.replacement = aReplacement;
		
		//set the pattern
		this.pattern = aPattern;
	}
	/**
	 * Return the replacement of this Replace Step
	 * @return a String containing the replacement of this replace object 
	 */
	public String getReplacement()
	{
		//copy the replacement
		String aReplacement = this.replacement;
		
		//return the copy of the replacement
		return aReplacement;
	}
	/**
	 * Return the pattern of this Replace Step
	 * @return a String containing the pattern of this Replace Step
	 */
	public String getPattern()
	{
		//copy the pattern
		String aPattern = this.pattern;
		
		//return the copy of the pattern 
		return aPattern;
	}
	/**
	 * Set the Replacement of this Replace Step
	 * @param aReplacement the String containing the Replacement of this  ReplaceStep
	 */
	public void setReplacement(String aReplacement)
	{
		//set the replacement value
		this.replacement = aReplacement;
	}
	/**
	 * Set the pattern of this Replace Step
	 * @param aPattern a String containing the pattern of this ReplaceStep 
	 */
	public void setPattern(String aPattern)
	{
		//set the pattern value
		this.pattern = aPattern;
	}

}
