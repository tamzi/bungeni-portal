# -*- coding: utf-8 -*-

from zope.interface import Interface

##code-section HEAD
##/code-section HEAD

class IDebateRecord(Interface):
    """Marker interface for .DebateRecord.DebateRecord
    """

class IDebateRecordPage(Interface):
    """Marker interface for .DebateRecordPage.DebateRecordPage
    """

class IDebateRecordFolder(Interface):
    """Marker interface for .DebateRecordFolder.DebateRecordFolder
    """

class IDebateRecordSection(Interface):
    """Marker interface for .DebateRecordSection.DebateRecordSection
    """

class ITakeTranscription(Interface):
    """Marker interface for .TakeTranscription.TakeTranscription
    """

class IMinutes(Interface):
    """Marker interface for .Minutes.Minutes
    """

class ITake(Interface):
    """Marker interface for .Take.Take
    """

class IRotaFolder(Interface):
    """Marker interface for .RotaFolder.RotaFolder
    """

class IRotaItem(Interface):
    """Marker interface for .RotaItem.RotaItem
    """

class IRotaTool(Interface):
    """Marker interface for .RotaTool.RotaTool
    """

##code-section FOOT
##/code-section FOOT