/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.editor.metadata;

/**
 *
 * @author undesa
 */
 public class LanguageCode {
        String languageCode;
        String languageName;
        
        LanguageCode(String langC, String langN) {
            languageCode = langC;
            languageName = langN;
        }
        
        @Override
        public String toString(){
            return languageName;
        }
    }