import unittest

from marginalia.document import SimpleDocument, SimpleDocumentAnnotationAdaptor
from marginalia.interfaces import ISimpleDocument, IMarginaliaAnnotatable
from marginalia.interfaces import IMarginaliaAnnotatableAdaptor
from zope.interface import alsoProvides
from zope.app.testing.functional import FunctionalTestCase
from zope.interface.verify import verifyObject

from zope.publisher.browser import TestRequest
from zope.component import getMultiAdapter, provideAdapter

class SimpleDocumentTestCase(FunctionalTestCase):
    """Functional test cases for SimpleDocument."""

    def setUp(self):
        """Prepares for a functional test case."""
        super(SimpleDocumentTestCase, self).setUp()
        self.document = SimpleDocument()
        self.document.description = u"body text"
        self.document.title = u"document title"
        
    def tearDown(self):
        """Cleans up after a functional test case."""
        super(SimpleDocumentTestCase, self).tearDown()
        del self.document

    def test_fields(self):
        """Testing document fields."""
        self.assertEquals(self.document.description, u"body text",
                          "Document description not stored")
        self.assertEquals(self.document.title, u"document title",
                          "Document title not stored")
    
    def test_implements(self):
        """Checks the Interfaces that Simple Document implements."""
        self.assertEquals(ISimpleDocument.implementedBy(SimpleDocument), True,
                          "ISimpleDocument Interface implementation error")

        self.assertEquals(ISimpleDocument.providedBy(self.document), True,
                          "ISimpleDocument Interface implementation error")        

        self.assertEquals(IMarginaliaAnnotatable.implementedBy(SimpleDocument), True,
                          "IMarginaliaAnnotatable Interface implementation error")

        self.assertEquals(IMarginaliaAnnotatable.providedBy(self.document), True,
                          "IMarginaliaAnnotatable Interface implementation error")        


    def test_verifyimplementations(self):
        """Verifies the implementations."""
        self.assertEquals(verifyObject(ISimpleDocument, self.document), True,
                          "ISimpleDocument not properly implemented")
        self.assertEquals(verifyObject(IMarginaliaAnnotatable, self.document), True,
                          "ISimpleDocument not properly implemented")

    def test_annotationadaptor(self):
        """Testing the the annotation adaptor."""
        annotation_adaptor = IMarginaliaAnnotatableAdaptor(self.document)

        self.assertEquals(isinstance(annotation_adaptor,
                                     SimpleDocumentAnnotationAdaptor), True,
                          "Unable to find the Annotation Adaptor Implementation.")
        self.assertEquals(annotation_adaptor.isAnnotatable(), True,
                          "This should return True like a marker interface.")
        self.assertEquals(annotation_adaptor.getBodyText(), u"body text",
                          "This should return True like a marker interface.")
        #getAnnotatedUrl might be removed from IMarginaliaAnnotatableAdaptor
        
class SimpleDocumentAnnotationTestCase(FunctionalTestCase):
    """Integration test cases for SimpleDocument."""

    def setUp(self):
        """Prepares for a functional test case."""
        super(SimpleDocumentAnnotationTestCase, self).setUp()
        self.document = SimpleDocument()
        self.document.description = u"body text"
        self.document.title = u"document title"
        
    def tearDown(self):
        """Cleans up after a functional test case."""
        super(SimpleDocumentAnnotationTestCase, self).tearDown()
        del self.document

    def test_adaptor(self):
        """Testing the annotation adaptor."""
        request = TestRequest()
        view = getMultiAdapter((self.document, request), name=u'annotate.html')
        self.assertEquals(view.getBodyText(), u"body text",
                          "IAnnotatable views unable to access the description attribute.")

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SimpleDocumentTestCase))
    suite.addTest(unittest.makeSuite(SimpleDocumentAnnotationTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
                  
