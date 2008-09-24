package org.un.bungeni.translators.odttoakn.map;

import java.util.HashMap;

import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpressionException;
import org.un.bungeni.translators.odttoakn.steps.MapStep;
import org.un.bungeni.translators.xpathresolver.XPathResolver;
import org.w3c.dom.Document;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

/**
 *  This is the map reader Object, 
 *  A map reader object is used to read a map xml and retrieve all te Map Steps of the map
 */
public class MapReader implements MapReaderInterface
{
	//the XML that contains the map
	private Document mapXML; 
	
	/**
	 * Create a new Map reader object builded on the given Map XML file 
	 * @param aMapXML the XML file that contains the map 
	 */
	public MapReader(Document aMapXML)
	{
		//save the map XML
		this.mapXML = aMapXML;
	}
	
	/**
	 * Return the step having the given id
	 * @param anId the id of the step that you want to retrieve 
	 * @return the Step haing the given id
	 * @throws XPathExpressionException 
	 */
	public MapStep getMapStepById(Integer anId) throws XPathExpressionException
	{
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the Map step with the given id in this Map XML
		Node stepNode = (Node)xresolver.evaluate(this.mapXML, "//element[@id='" + anId.toString() + "]", XPathConstants.NODE);
				
		//get the MapSteps with the given type in this configuration
		NodeList attributeNodes = (NodeList)xresolver.evaluate(this.mapXML, "//element[@id='" + stepNode.getAttributes().getNamedItem("id").getNodeValue() + "']//attribute" , XPathConstants.NODESET);
		
		//the string that will contain all the attributes mapping
		String attributesList = ""; 
		
		//process all attributes and add them to the string
		for (int k = 0; k < attributeNodes.getLength(); k++)
		{
			//the current node
			Node currentNode = attributeNodes.item(k);
			
			//add all the information of the attribute node to the string
			attributesList = attributesList + currentNode.getAttributes().getNamedItem("attname").getNodeValue() + "=";
			attributesList = attributesList + currentNode.getAttributes().getNamedItem("attresult").getNodeValue() + ";";
			attributesList = attributesList + currentNode.getAttributes().getNamedItem("attvalue").getNodeValue();
			
			//if is not the last child add a comma
			if (k != attributeNodes.getLength() -1)
			{
				attributesList = attributesList + ",";
			}
			
		}
		
		//create the Map Step 
		MapStep resultMapStep = new MapStep( Integer.parseInt(stepNode.getAttributes().getNamedItem("id").getNodeValue()),
						  					 stepNode.getAttributes().getNamedItem("type").getNodeValue(),
						  					 stepNode.getAttributes().getNamedItem("name").getNodeValue(),
						  					 stepNode.getAttributes().getNamedItem("bungeniSectionType").getNodeValue(),
						  					 stepNode.getAttributes().getNamedItem("result").getNodeValue(),
						  					 attributesList);

		//return the created Step
		return resultMapStep;
	}
	/**
	 * Return the HashMp containing all the step of the the map having the given type
	 * @param aType the type of the steps that you want to retrieve 
	 * @return the HashMap containing all the step of the map having the given type indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, MapStep> getMapStepsByType(String aType) throws XPathExpressionException
	{
		//the HashMap to return 
		HashMap<Integer,MapStep> resultMap = new HashMap<Integer,MapStep>();
		
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the MapSteps with the given type in this configuration
		NodeList stepNodes = (NodeList)xresolver.evaluate(this.mapXML, "//element[@type='" + aType + "]", XPathConstants.NODESET);
		
		//get all the Map steps and creates a  Map Step object for each one of them
		for (int i = 0; i < stepNodes.getLength(); i++) 
		{
			//get the step node
			Node stepNode = stepNodes.item(i);
						
			//get the MapSteps with the given type in this configuration
			NodeList attributeNodes = (NodeList)xresolver.evaluate(this.mapXML, "//element[@id='" + stepNode.getAttributes().getNamedItem("id").getNodeValue() + "']//attribute" , XPathConstants.NODESET);
			
			//the string that will contain all the attributes mapping
			String attributesList = ""; 
			
			//process all attributes and add them to the string
			for (int k = 0; k < attributeNodes.getLength(); k++)
			{
				//the current node
				Node currentNode = attributeNodes.item(k);
				
				//add all the information of the attribute node to the string
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attname").getNodeValue() + "=";
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attresult").getNodeValue() + ";";
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attvalue").getNodeValue();
				
				//if is not the last child add a comma
				if (k != attributeNodes.getLength() -1)
				{
					attributesList = attributesList + ",";
				}
				
			}
			
			//create the Map Step 
			MapStep resultStep = new MapStep( Integer.parseInt(stepNode.getAttributes().getNamedItem("id").getNodeValue()),
 					 								 stepNode.getAttributes().getNamedItem("type").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("name").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("bungeniSectionType").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("result").getNodeValue(),
 					 								 attributesList);

			//add the node to the hash map set its key as its position (step attribute)
			resultMap.put(Integer.parseInt(stepNode.getAttributes().getNamedItem("id").getNodeValue()),resultStep);		
		}
		
		//return the hash map containing all the Steps
		return resultMap;	
	}
	/**
	 * Returns all the steps having the given name
	 * @param aName the name of the steps that you want to retrieve  
	 * @return the HashMap containing all the Steps of the map having the given name indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, MapStep> getMapStepsByName(String aName) throws XPathExpressionException
	{
		//the HashMap to return 
		HashMap<Integer,MapStep> resultMap = new HashMap<Integer,MapStep>();
		
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the MapSteps with the given type in this configuration
		NodeList stepNodes = (NodeList)xresolver.evaluate(this.mapXML, "//element[@name='" + aName + "]", XPathConstants.NODESET);
		
		//get all the Map steps and creates a  Map Step object for each one of them
		for (int i = 0; i < stepNodes.getLength(); i++) 
		{
			//get the step node
			Node stepNode = stepNodes.item(i);
						
			//get the MapSteps with the given type in this configuration
			NodeList attributeNodes = (NodeList)xresolver.evaluate(this.mapXML, "//element[@id='" + stepNode.getAttributes().getNamedItem("id").getNodeValue() + "']//attribute" , XPathConstants.NODESET);
			
			//the string that will contain all the attributes mapping
			String attributesList = ""; 
			
			//process all attributes and add them to the string
			for (int k = 0; k < attributeNodes.getLength(); k++)
			{
				//the current node
				Node currentNode = attributeNodes.item(k);
				
				//add all the information of the attribute node to the string
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attname").getNodeValue() + "=";
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attresult").getNodeValue() + ";";
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attvalue").getNodeValue();
				
				//if is not the last child add a comma
				if (k != attributeNodes.getLength() -1)
				{
					attributesList = attributesList + ",";
				}
				
			}
			
			//create the Map Step 
			MapStep resultStep = new MapStep( Integer.parseInt(stepNode.getAttributes().getNamedItem("id").getNodeValue()),
 					 								 stepNode.getAttributes().getNamedItem("type").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("name").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("bungeniSectionType").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("result").getNodeValue(),
 					 								 attributesList);

			//add the node to the hash map set its key as its position (step attribute)
			resultMap.put(Integer.parseInt(stepNode.getAttributes().getNamedItem("id").getNodeValue()),resultStep);		
		}
		
		//return the hash map containing all the Steps
		return resultMap;	
	}

	/**
	 * Returns all the steps having the given bungeniSectionType
	 * @param aBungeniSectionType the bungeniSectionType of the Steps of the Map that you want to retrieve
	 * @return the HashMap containing all the steps of the map having the given bungeniSectionType indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, MapStep> getMapStepsByBungeniSectionType(String aBungeniSectionType) throws XPathExpressionException
	{
		//the HashMap to return 
		HashMap<Integer,MapStep> resultMap = new HashMap<Integer,MapStep>();
		
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the MapSteps with the given type in this configuration
		NodeList stepNodes = (NodeList)xresolver.evaluate(this.mapXML, "//element[@bungeniSectionType='" + aBungeniSectionType + "]", XPathConstants.NODESET);
		
		//get all the Map steps and creates a  Map Step object for each one of them
		for (int i = 0; i < stepNodes.getLength(); i++) 
		{
			//get the step node
			Node stepNode = stepNodes.item(i);
						
			//get the MapSteps with the given type in this configuration
			NodeList attributeNodes = (NodeList)xresolver.evaluate(this.mapXML, "//element[@id='" + stepNode.getAttributes().getNamedItem("id").getNodeValue() + "']//attribute" , XPathConstants.NODESET);
			
			//the string that will contain all the attributes mapping
			String attributesList = ""; 
			
			//process all attributes and add them to the string
			for (int k = 0; k < attributeNodes.getLength(); k++)
			{
				//the current node
				Node currentNode = attributeNodes.item(k);
				
				//add all the information of the attribute node to the string
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attname").getNodeValue() + "=";
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attresult").getNodeValue() + ";";
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attvalue").getNodeValue();
				
				//if is not the last child add a comma
				if (k != attributeNodes.getLength() -1)
				{
					attributesList = attributesList + ",";
				}
				
			}
			
			//create the Map Step 
			MapStep resultStep = new MapStep( Integer.parseInt(stepNode.getAttributes().getNamedItem("id").getNodeValue()),
 					 								 stepNode.getAttributes().getNamedItem("type").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("name").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("bungeniSectionType").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("result").getNodeValue(),
 					 								 attributesList);

			//add the node to the hash map set its key as its position (step attribute)
			resultMap.put(Integer.parseInt(stepNode.getAttributes().getNamedItem("id").getNodeValue()),resultStep);		
		}
		
		//return the hash map containing all the Steps
		return resultMap;	
	}

	/**
	 * Returns all the steps having the given result
	 * @param aResult the result of the Steps of the map that you want to retrieve 
	 * @return an HashMap containing all the steps of the map having the given result indexed by their id 
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, MapStep> getMapStepsByResult(String aResult) throws XPathExpressionException
	{
		//the HashMap to return 
		HashMap<Integer,MapStep> resultMap = new HashMap<Integer,MapStep>();
		
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the MapSteps with the given type in this configuration
		NodeList stepNodes = (NodeList)xresolver.evaluate(this.mapXML, "//element[@result='" + aResult + "]", XPathConstants.NODESET);
		
		//get all the Map steps and creates a  Map Step object for each one of them
		for (int i = 0; i < stepNodes.getLength(); i++) 
		{
			//get the step node
			Node stepNode = stepNodes.item(i);
						
			//get the MapSteps with the given type in this configuration
			NodeList attributeNodes = (NodeList)xresolver.evaluate(this.mapXML, "//element[@id='" + stepNode.getAttributes().getNamedItem("id").getNodeValue() + "']//attribute" , XPathConstants.NODESET);
			
			//the string that will contain all the attributes mapping
			String attributesList = ""; 
			
			//process all attributes and add them to the string
			for (int k = 0; k < attributeNodes.getLength(); k++)
			{
				//the current node
				Node currentNode = attributeNodes.item(k);
				
				//add all the information of the attribute node to the string
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attname").getNodeValue() + "=";
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attresult").getNodeValue() + ";";
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attvalue").getNodeValue();
				
				//if is not the last child add a comma
				if (k != attributeNodes.getLength() -1)
				{
					attributesList = attributesList + ",";
				}
				
			}
			
			//create the Map Step 
			MapStep resultStep = new MapStep( Integer.parseInt(stepNode.getAttributes().getNamedItem("id").getNodeValue()),
 					 								 stepNode.getAttributes().getNamedItem("type").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("name").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("bungeniSectionType").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("result").getNodeValue(),
 					 								 attributesList);

			//add the node to the hash map set its key as its position (step attribute)
			resultMap.put(Integer.parseInt(stepNode.getAttributes().getNamedItem("id").getNodeValue()),resultStep);		
		}
		
		//return the hash map containing all the Steps
		return resultMap;	
	}

	
	/**
	 * Return an HashMap containing all the step of the map indexed by their id 
	 * @return the HashMap containing all the step of the map indexed by their id
	 * @throws XPathExpressionException 
	 */
	public HashMap<Integer, MapStep> getMapSteps() throws XPathExpressionException
	{
		//the HashMap to return 
		HashMap<Integer,MapStep> resultMap = new HashMap<Integer,MapStep>();
		
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the MapSteps with the given type in this configuration
		NodeList stepNodes = (NodeList)xresolver.evaluate(this.mapXML, "//element", XPathConstants.NODESET);
		
		//get all the Map steps and creates a  Map Step object for each one of them
		for (int i = 0; i < stepNodes.getLength(); i++) 
		{
			//get the step node
			Node stepNode = stepNodes.item(i);
						
			//get the MapSteps with the given type in this configuration
			NodeList attributeNodes = (NodeList)xresolver.evaluate(this.mapXML, "//element[@id='" + stepNode.getAttributes().getNamedItem("id").getNodeValue() + "']//attribute" , XPathConstants.NODESET);
			
			//the string that will contain all the attributes mapping
			String attributesList = ""; 
			
			//process all attributes and add them to the string
			for (int k = 0; k < attributeNodes.getLength(); k++)
			{
				//the current node
				Node currentNode = attributeNodes.item(k);
				
				//add all the information of the attribute node to the string
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attname").getNodeValue() + "=";
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attresult").getNodeValue() + ";";
				attributesList = attributesList + currentNode.getAttributes().getNamedItem("attvalue").getNodeValue();
				
				//if is not the last child add a comma
				if (k != attributeNodes.getLength() -1)
				{
					attributesList = attributesList + ",";
				}
				
			}
			
			//create the Map Step 
			MapStep resultStep = new MapStep( Integer.parseInt(stepNode.getAttributes().getNamedItem("id").getNodeValue()),
 					 								 stepNode.getAttributes().getNamedItem("type").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("name").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("bungeniSectionType").getNodeValue(),
 					 								 stepNode.getAttributes().getNamedItem("result").getNodeValue(),
 					 								 attributesList);

			//add the node to the hash map set its key as its position (step attribute)
			resultMap.put(Integer.parseInt(stepNode.getAttributes().getNamedItem("id").getNodeValue()),resultStep);		
		}
		
		//return the hash map containing all the Steps
		return resultMap;	
	}
	
	/**
	 * Returns a String containing the path of the map resolver 
	 * @return a String containing the path of the map resolver 
	 * @throws XPathExpressionException
	 */
	public String getMapResolver() throws XPathExpressionException
	{
		//retreive the XPath resolver instance 
		XPathResolver xresolver = XPathResolver.getInstance();
		
		//get the MapSteps with the given type in this configuration
		String resolverLocation = (String)xresolver.evaluate(this.mapXML, "//mapresolver/@href", XPathConstants.STRING);
		
		//return the resolver location
		return resolverLocation;
	}
}
