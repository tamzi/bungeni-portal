package org.bungeni.restlet.server;

import java.io.File;

import org.bungeni.restlet.TransformerRestletDefaultConfiguration;
import org.bungeni.restlet.resources.OdtResource;
import org.bungeni.restlet.restlets.TransformParamsRestlet;
import org.restlet.Application;
import org.restlet.Component;
import org.restlet.Restlet;
import org.restlet.Router;
import org.restlet.data.Protocol;


public class TransformerServer extends Application {
   private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(TransformerServer.class.getName());
   private static Component serverComponent = null;
   private static int SERVER_PORT = 8182;
   private static String SERVER_TMP_FOLDER = "/home/undesa/tmp";
   public static final String SERVER_CONFIG_FILE = "transformer.ini";
   private static Restlet setParamsRestlet  = null;


   public static void setServerPort(int nPort) {
       SERVER_PORT = nPort;
   }

   public static void setServerTempFolder(String sFolder) {
       SERVER_TMP_FOLDER = sFolder;
   }

@SuppressWarnings("finally")
private static boolean configServer(String workingDir) {
	   boolean bState = false;
	   try {
		   String iniFile = workingDir + File.separator + SERVER_CONFIG_FILE;
		   File fIni = new File(iniFile);
		   if (fIni.exists()) {
			   TransformerRestletDefaultConfiguration config = TransformerRestletDefaultConfiguration.getInstance(fIni);
			   SERVER_PORT = config.getServerPort();
			   SERVER_TMP_FOLDER = config.getServerTmpFolder();
			   bState = true;
		   } 
	   } catch (Exception ex) {
		   log.error("configServer :", ex);
		   ex.printStackTrace(System.out);
	   } finally {
		   return bState;
	   }
	  
   }
   
   
   @SuppressWarnings("finally")
public static TransformerServer startServer(String workingDir) {
            TransformerServer ts = null;
            try {
                if (serverComponent == null) {
                	if (configServer(workingDir)) {
                		serverComponent = new Component();
                		serverComponent.getServers().add(Protocol.HTTP, SERVER_PORT);
                		ts = new TransformerServer();
                		serverComponent.getDefaultHost().attach("", ts);
                		//create the restlet instance here, before calling start
                		setParamsRestlet = new TransformParamsRestlet(workingDir);
                		serverComponent.start();
                	} else {
                		System.out.println("Failed while configuring TransformServer");
                	}
                } else {
                    if (serverComponent.isStopped()) {
                        serverComponent.start();
                    } else {
                        System.out.println("TransformServer is already running on port " + SERVER_PORT);
                        log.info("TransformServer is already running on port " + SERVER_PORT);
                    }
                }

            } catch (Exception ex) {
                log.error("startServer : " , ex);
            } finally {
                return ts;
            }
     }

    public static String getTempFileFolder() {
        return SERVER_TMP_FOLDER;
    }

     @Override
      public Restlet createRoot() {
        Router router = new Router(getContext());
        router.attach("/convert_to_anxml", OdtResource.class);
        router.attach("/set_convert_params",setParamsRestlet);
        return router;
      }

     public static void main(String[] args) {
    	 TransformerServer.startServer(System.getProperty("user.dir"));
     }
}
