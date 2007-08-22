/*
 * ooDocNotes.java
 *
 * Created on August 22, 2007, 10:09 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package org.bungeni.ooo;

import com.sun.star.beans.UnknownPropertyException;
import java.io.IOException;
import java.io.StringReader;
import java.util.HashMap;
import java.util.List;
import java.util.Vector;
import org.apache.commons.lang.StringEscapeUtils;
import org.jdom.Document;
import org.jdom.Element;
import org.jdom.JDOMException;
import org.jdom.input.SAXBuilder;
import org.jdom.output.XMLOutputter;
/**
 * An openoffice document allows storage of text / string 
 * type properties, but not structured properties like XML 
 * or container properties.  A bungeniEditorNote is an xmlEncoded 
 * XML string which is stored in a property called "bungeniEditoNotes" 
 * a "bungeniEditorNotes" XML looks like this:
 * <notes>
 *    <note>
 *        <dte>
 *            ISO date
 *        </dte>
 *        <bau>
 *            author name
 *        </bau>
 *        <txt>
 *            <![[CDATA[
 *                Note text
 *            ]]>
 *        </txt>
 *    </note>
 * </notes>
 * @author Administrator
 */
public class ooDocNotes {
    OOComponentHelper ooDocument;
    String xmlStringDocument;
    org.jdom.Document xmlNotesDocument;
    private static String NOTE_PROPERTY_NAME = "bungeniEditorNotes";
    private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(ooDocNotes.class.getName());
 
    /** Creates a new instance of ooDocNotes */
    public ooDocNotes(OOComponentHelper instance) {
        log.debug("ooDocNotes : in constructor");
        ooDocument = instance;
        initNoteProperty();
    }
    
    /**
     * Returns all <note> elements
     */
    public Vector<ooDocNoteStructure> readNotes(){
        String bungeniEditorNotes = "";
        Vector<ooDocNoteStructure> ooNotes = new Vector<ooDocNoteStructure>();
        List notes=null;
           try {
        if (ooDocument.propertyExists(NOTE_PROPERTY_NAME)) {
                notes = getNotesCollection();
                for (int i=0 ; i < notes.size() ; i++) {
                    //get the note elemnt
                    Element note = (Element) notes.get(i);
                    String date = note.getChildText("dte");
                    String author = note.getChildText("bau");
                    String text = note.getChildText("txt");
                    ooDocNoteStructure noteObj = new ooDocNoteStructure (date, author, text);
                    ooNotes.addElement(noteObj);
                }
        }
        } catch (Exception ex) {
                log.debug(ex.getMessage());
        } finally {
        return ooNotes;
        }
    }
    
    private void initNoteProperty () {
        log.debug("initNoteProperty");
        if (! ooDocument.propertyExists(NOTE_PROPERTY_NAME)) {
            log.debug("adding Property: initNoteProperty");
            ooDocument.addProperty(NOTE_PROPERTY_NAME, _Note_Xml());
        }
    }
    
    private String _Note_Xml (){
        String note_Xml = "";
        note_Xml = "<notes></notes>";
        return note_Xml;
    }
    
    public void addNote (ooDocNoteStructure note) {
        try {
        Element newNote = newNote(note.getNoteText(), note.getNoteDate(), note.getNoteAuthor());
        List childNotes = getNotesCollection();
        childNotes.add(newNote);
        XMLOutputter outer = new XMLOutputter();
        String outputXML = outer.outputString(xmlNotesDocument);
        String escapedOutputXML = StringEscapeUtils.escapeXml(outputXML);
        //now set property value
        ooDocument.setPropertyValue(NOTE_PROPERTY_NAME, escapedOutputXML);
        } catch (Exception ex) {
            log.debug("addNote Exception" + ex.getMessage(), ex);
        }
    }
    
    private List getNotesCollection() {
        String bungeniEditorNotes = "";
        List notes = null;
        try {
             bungeniEditorNotes = ooDocument.getPropertyValue(NOTE_PROPERTY_NAME);
                //decode XML and parse
             bungeniEditorNotes = org.apache.commons.lang.StringEscapeUtils.unescapeXml(bungeniEditorNotes);
             xmlNotesDocument = getXMLDocument(bungeniEditorNotes);
             //getRootElement is <notes> within that are the note elements
              notes = xmlNotesDocument.getRootElement().getChildren("note"); 
         } catch (UnknownPropertyException ex) {
            log.debug(ex.getMessage(), ex);
        } finally {
            return notes;
        }
    }
    
    private org.jdom.Element newNote (String cdataText, String noteDate, String noteAuthor) {
        Element newNote = null ;
        try {
            newNote = new Element("note");
            org.jdom.Element newNoteText = new org.jdom.Element("txt");
            org.jdom.Element newNoteDate = new org.jdom.Element("dte");
            org.jdom.Element newNoteAuthor = new org.jdom.Element("aut");
            newNoteText.addContent(new org.jdom.CDATA(cdataText));
            newNoteDate.addContent(noteDate);
            newNoteAuthor.addContent(noteAuthor);

            List noteChildren = newNote.getChildren();
            noteChildren.add(newNoteAuthor);
            noteChildren.add(newNoteDate);
            noteChildren.add(newNoteText);
        } catch (Exception ex ) {
            log.debug(ex.getMessage(), ex);
        } finally {
        return newNote;
        }
    }

    private org.jdom.Document getXMLDocument(String bungeniEditorNotes) {
        org.jdom.Document xmlDocument = null;
        try {        
        SAXBuilder saxBuilder=new SAXBuilder();
        StringReader stringReader=new StringReader(bungeniEditorNotes);
        xmlDocument = saxBuilder.build(stringReader);
        } catch (IOException ex) {
            log.debug(ex.getMessage(), ex);
        } catch (JDOMException ex) {
            log.debug(ex.getMessage(), ex);
        } finally {
            return xmlDocument;
        }
         
    }
    
    
}
