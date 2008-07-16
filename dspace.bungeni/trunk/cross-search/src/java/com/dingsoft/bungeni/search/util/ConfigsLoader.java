/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.dingsoft.bungeni.search.util;

import com.dingsoft.bungeni.search.ConfigurationInfo;
import java.io.FileReader;
import java.util.Properties;


/**
 *
 * Class used for loading users configuration from the config file
 * @author undesa
 */
public class ConfigsLoader 
{
    private static ConfigurationInfo configInfo=null;
    static
    {
        try
        {
            configInfo=new ConfigurationInfo();
            Properties props=new Properties();
            props.load(new FileReader("../conf/repository.cfg"));
            configInfo.setProperties(props);
        }
        catch(Exception e)
        {
            LoggingFactory.logException(e);
        }
        catch(Error err)
        {
            LoggingFactory.logError(err);
        }
    }
    /**
     * 
     * The default constructor that loads all the configurations fromt he config file and stores them locally in a 
     * <code>ConfigurationInfo</code> object
     */
    private ConfigsLoader()
    {
    }
    /**
     * gets the current <code>ConfigurationInfo</code> abject associated with this loader
     * @return <code>Configuration Info, </code>
     */
    public static ConfigurationInfo getConfigurationInfo()
    {
        return configInfo;
    }
    /**
     * Sets the <code>Sets the configurationInfo onject associated with this instance of ConfigsLoader</code>
     * @param info A configurationInfo Object representing the new configurations
     */
    public static void setConfigurationInfo(ConfigurationInfo info)
    {
        configInfo=info;
    }
}
