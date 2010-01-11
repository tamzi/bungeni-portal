/*
 * Shut up
 */

package com.dingsoft.bungeni.search.util;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Date;

/**
 *
 * This is a generic class that logs all the Messages Errors and and Exceptions that occur in the cause of program usage
 * @author Solomon Kariri
 */
public class LoggingFactory {
    private LoggingFactory()
    {
        
    }
    private static PrintWriter out=null;
    private static String homeDir=null;
    static 
    {
        try
        {
            homeDir=".."+File.separator;
            homeDir+=File.separator+"repositorylogs";
            new File(homeDir).mkdirs();
            FileWriter writ=new FileWriter(homeDir+File.separator+"digitalrepository.log",true);
            out=new PrintWriter(writ);
        }
        catch(IOException ioe)
        {
            ioe.printStackTrace();
        }
    }
    /**
     * The method logs a full stack trace of the error and also indicates precisely the tme when the error was reported or logged.
     * @param error an <code>Object</code> of type <code>Error</code> that represents the error that has occured
     * The method logs a full stack trace of the error and also indicates precisely the tme when the error was reported or logged.
     * The method adds a signature at the top of the log message to indicate clearly that the log is an error through the use of the
     * line Error <i>error type and name</i>
     */
    public synchronized static void logError(Error error)
    {
        StackTraceElement[]elements=error.getStackTrace();
        out.println("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++");
        out.println("Error "+error+" Logged on "+new Date().toString());
        out.flush();
        for(int i=0;i<elements.length;i++)
        {
            out.println(elements[i].toString());
            out.flush();
        }
    }
    /**
     * The method logs a full stack trace of the exception and also indicates precisely the time when the exception was reported or logged.
     * @param e The exception that is to be logged
     * The method logs a full stack trace of the exception and also indicates precisely the time when the exception was reported or logged.
     * The method adds a signature at the top of the log message to indicate clearly that the log is an exception through the use of the
     * line Exception <i>exception type and name</i>
     */
    public synchronized static void logException(Exception e)
    {
        StackTraceElement[]elements=e.getStackTrace();
        out.println();
        out.println("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++");
        out.println("Exception "+e+" Logged on "+new Date().toString());
        out.flush();
        for(int i=0;i<elements.length;i++)
        {
            out.println(elements[i].toString());
            out.flush();
        }
    }
    
    /**
     * This method just echos what has been passed to it as the message to the log file.
     * @param message The message that is to be logged
     * This method just echos what has been passed to it as the message to the log file.
     * <p>The method aso adds a signature showing clearly that what has been logged is a normal message
     * and also indicates precisely the time when the message was reported or logged
     */
    public synchronized static void logCommon(String message)
    {
        out.println();
        out.println("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++");
        out.println("Normal log Message Logged on "+new Date().toString());
        out.println(message);
        out.flush();
    }
    /**
     * This method adds the toString() return value of the parameter object to the log file.
     * @param obj The object that is to be logged
     * <p>The method simply echoes the toString() return value of type String to the log file.
     * It also adds a signature to the log message indicating that it is an Object that was logged
     * and also indicates precisely the time that the Object was logged
     */
    public synchronized static void logObject(Object obj)
    {
        out.println();
        out.println("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++");
        out.println("Object "+obj.getClass().getName()+" Logged on"+new Date().toString());
        out.println(obj.toString());
        out.flush();
    }
}