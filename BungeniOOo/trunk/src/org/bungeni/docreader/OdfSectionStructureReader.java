/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.bungeni.docreader;

import org.openoffice.odf.doc.OdfDocument;
import org.openoffice.odf.doc.element.office.OdfAutomaticStyles;
import org.openoffice.odf.doc.element.style.OdfStyle;
import org.openoffice.odf.doc.element.text.OdfSection;
import org.openoffice.odf.dom.style.OdfStyleFamily;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

/**
 *
 * @author undesa
 */
public class OdfSectionStructureReader {
        private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(OdfSectionStructureReader.class.getName());
 
        
    private OdfStyle getSectionStyle (OdfSection oSection) {
           OdfAutomaticStyles osb = oSection.getAutomaticStyles();
           OdfStyle secStyle = osb.getStyle(oSection.getStyleName(), OdfStyleFamily.Section);
           return secStyle;
    }
    
    private NamedNodeMap getSectionStyleProperties(OdfStyle sectStyle) {
        NamedNodeMap nmap = null;
        NodeList nsectList = sectStyle.getChildNodes();
        for (int i=0; i < nsectList.getLength(); i++) {
            Node nmatch = nsectList.item(i);
            if (nmatch.getNodeName().equals("style:section-properties")) {
                if (nmatch.hasAttributes()) {
                    NamedNodeMap nattrMap = nmatch.getAttributes();
                    return nattrMap;    
                }
            }
        }
        return nmap;
}
    
            
    private Node getBodyNode(NodeList nlist) {
        for (int i=0; i < nlist.getLength(); i++) {
            Node nnode = nlist.item(i);
            if (nnode instanceof OdfSection) {
                OdfSection nsection = (OdfSection) nnode;
                //get section style name
                String sectionStyleName = nsection.getStyleName();
                if (sectionStyleName != null) {
                    if (sectionStyleName.length() > 0 ) {
                        //
                        OdfStyle sectStyle = getSectionStyle(nsection);
                        NamedNodeMap sectionProps = getSectionStyleProperties (sectStyle);
                        Node nfoundNode = sectionProps.getNamedItem("BungeniSectionType");
                        if (nfoundNode != null ) {
                            if (nfoundNode.getNodeValue().equals("body")) {
                                return nnode;
                            }
                        }
                    }
                }
            }
        }
        return null;
    }
    
    private NamedNodeMap getSectionMetadataAttributes(OdfSection nSection) {
             OdfStyle sectStyle = getSectionStyle(nSection);
             if (sectStyle != null) {
                NamedNodeMap sectionProps = getSectionStyleProperties (sectStyle);
                return sectionProps;
             } else
                 return null;
    }
    
    private String getSectionType(OdfSection nsection, NamedNodeMap nattr) {
        Node nitem = nattr.getNamedItem("BungeniSectionType");
        if (nitem != null) {
            return nitem.getNodeValue();
        } else 
            return nsection.getName();
    }
    
    private void getChildSections(Node nNode, int nDepth) {
        ++nDepth;
        NodeList nChildren = nNode.getChildNodes();
        for (int i=0; i < nChildren.getLength() ; i++ ) {
            Node nnChild = nChildren.item(i);
            if (nnChild instanceof OdfSection) {
                OdfSection childSection = (OdfSection) nnChild;
                NamedNodeMap nattribs = getSectionMetadataAttributes(childSection);
                if (nattribs != null) {
                    //if section has metadata
                    for (int d=0 ; d < nDepth ; d++) System.out.print(" ");
                    System.out.println(" - section type = " + getSectionType(childSection, nattribs));
                }
                getChildSections(nnChild, nDepth);
            }
        }
    }
    
    public void generateSectionHierarchy(String pathTofile){
        try {
            OdfDocument odf = OdfDocument.loadDocument(pathTofile);
            //OdfStyles odfStyles = odf.ge();
            //OdfFileDom fdom = odf.getStylesDom();
            //   fdom.getE
            NodeList lst = odf.getContentDom().getElementsByTagName("text:section");
            //get the first node with the body property
            Node nBodyNode = getBodyNode (lst);
            System.out.println(" body node = " + nBodyNode.getNodeName());
            //get child sections
            getChildSections(nBodyNode, 0);
           
        } catch (Exception ex) {
            log.error("getSectionHierarchy : " + ex.getMessage());
        }
        
    }
}
