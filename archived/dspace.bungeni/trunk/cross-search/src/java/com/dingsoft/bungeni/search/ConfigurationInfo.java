/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.dingsoft.bungeni.search;

import java.util.Properties;

/**
 *
 * Class that holds data about the current configuration of the cross search application
 * @author undesa
 */
public class ConfigurationInfo 
{
    private Properties properties;
    public static String NOT_FOUND_ERROR="NOT FOUND";
    public ConfigurationInfo()
    {
        this.properties=new Properties();
    }
    /**
     * Adds a new configuration property to this instance of the class
     * @param key The key used to identify the property
     * @param value The actual value of the property which is a String
     */
    public void addProperty(String key,String value)
    {
        properties.put(key, value);
    }
    /**
     * Retrieves a property for the key specified and returns it string representation.
     * Returns ConfigurationInfo.NOT_FOUND_ERROR if the property is misiing from the instance
     * 
     * @param key The key used to identify the property
     * @return String The actual value of the property which is a String
     */
    public String getProperty(String key)
    {
        if(properties.containsKey(key))
        {
            return properties.get(key).toString();
        }
        else
        {
            return ConfigurationInfo.NOT_FOUND_ERROR;
        }
    }
    /**
     * This method sets the properties held by the current instance of this ConfigurationInfo Object
     * @param p The new properties held by this instance of <code>ConfigurationInfo</code>
     */
    public void setProperties(Properties p)
    {
        this.properties=p;
    }
    /**
     * Returns the current <code>Properties</code> Object associated with this instance
     * @return A <code>Properties</code> Object representing the current properties held by this instance of <code>
     * ConfigurationInfo</code>
     */
    public Properties getProperties()
    {
        return this.properties;
    }
}
