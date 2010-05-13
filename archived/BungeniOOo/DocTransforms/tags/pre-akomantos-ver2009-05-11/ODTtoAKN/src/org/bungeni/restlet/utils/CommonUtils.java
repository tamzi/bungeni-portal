package org.bungeni.restlet.utils;

import java.io.DataInputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;

public class CommonUtils {
	public static String readTextFile(File fFile) throws IOException {
		byte[] buffer = new byte[(int)fFile.length()];
		DataInputStream in = new DataInputStream(new FileInputStream(fFile));
		in.readFully(buffer);
		String s = new String(buffer);
		return s;
	}
}
