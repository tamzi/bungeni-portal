/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.editor.metadata;

/**
 *
 * @author undesa
 */
   public class CountryCode {
        public String countryCode;
        public String countryName;
        
        CountryCode(){
            countryCode = countryName = "";
        }
        CountryCode(String countryC, String countryN) {
            countryCode = countryC;
            countryName = countryN;
        }
        
        @Override
        public String toString(){
            return countryName;
        }
        
    }
