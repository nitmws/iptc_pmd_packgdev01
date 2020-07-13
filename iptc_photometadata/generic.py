"""
    This module provides the most generic IPTC photo metadata classe
"""
from dataclasses import dataclass
from .common import IptcPhotometadata


@dataclass
class IptcPhotometadataGeneric(IptcPhotometadata):
    """IPTC Photo Metadata with all specified properties as attributes

        The class is derived from the basic Photometadata class.
    """

    supp_iptcprops = ('copyrightNotice', 'creatorsExt', 'creditLine', 'dateCreated',
                      'description', 'captionWriter', 'headline', 'instructions',
                      'intellectualGenre', 'jobid', 'keywords', 'usageTerms', 'sceneCodes', 'source',
                      'subjectCodes', 'title',
                      'additionalModelInfo', 'artworkOrObjects', 'organisationInImageCodes', 'copyrightOwners',
                      'aboutCvTerms', 'digitalImageGuid', 'digitalSourceType', 'embdEncRightsExprs',
                      'eventName', 'genres', 'imageRating', 'imageRegion', 'registryEntries',
                      'suppliers', 'imageSupplierImageId', 'licensors', 'linkedEncRightsExprs',
                      'locationCreated', 'locationsShown',
                      'minorModelAgeDisclosure', 'modelAges', 'modelReleaseDocuments', 'modelReleaseStatus',
                      'organisationInImageNames', 'personInImageNames', 'personsShown', 'productsShown',
                      'propertyReleaseDocuments', 'propertyReleaseStatus', 'webstatementRights')

    def __init__(self):
        super().__init__()
        self._supported_iptcpmd_tlprops = self.supp_iptcprops

    @property
    def copyrightNotice(self):
        return self._copyrightNotice

    @copyrightNotice.setter
    def copyrightNotice(self, value):
        self._copyrightNotice = value

    @property
    def creatorsExt(self):
        return self._creatorsExt

    @creatorsExt.setter
    def creatorsExt(self, value):
        self._creatorsExt = value

    @property
    def creditLine(self):
        return self._creditLine

    @creditLine.setter
    def creditLine(self, value):
        self._creditLine = value

    @property
    def dateCreated(self):
        return self._dateCreated

    @dateCreated.setter
    def dateCreated(self, value):
        self._dateCreated = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def captionWriter(self):
        return self._captionWriter

    @captionWriter.setter
    def captionWriter(self, value):
        self._captionWriter = value

    @property
    def headline(self):
        return self._headline

    @headline.setter
    def headline(self, value):
        self._headline = value

    @property
    def instructions(self):
        return self._instructions

    @instructions.setter
    def instructions(self, value):
        self._instructions = value

    @property
    def intellectualGenre(self):
        return self._intellectualGenre

    @intellectualGenre.setter
    def intellectualGenre(self, value):
        self._intellectualGenre = value

    @property
    def jobid(self):
        return self._jobid

    @jobid.setter
    def jobid(self, value):
        self._jobid = value

    @property
    def keywords(self):
        return self._keywords

    @keywords.setter
    def keywords(self, value):
        self._keywords = value

    @property
    def usageTerms(self):
        return self._usageTerms

    @usageTerms.setter
    def usageTerms(self, value):
        self._usageTerms = value

    @property
    def sceneCodes(self):
        return self._sceneCodes

    @sceneCodes.setter
    def sceneCodes(self, value):
        self._sceneCodes = value

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value

    @property
    def subjectCodes(self):
        return self._subjectCodes

    @subjectCodes.setter
    def subjectCodes(self, value):
        self._subjectCodes = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def additionalModelInfo(self):
        return self._additionalModelInfo

    @additionalModelInfo.setter
    def additionalModelInfo(self, value):
        self._additionalModelInfo = value

    @property
    def artworkOrObjects(self):
        return self._artworkOrObjects

    @artworkOrObjects.setter
    def artworkOrObjects(self, value):
        self._artworkOrObjects = value

    @property
    def organisationInImageCodes(self):
        return self._organisationInImageCodes

    @organisationInImageCodes.setter
    def organisationInImageCodes(self, value):
        self._organisationInImageCodes = value

    @property
    def copyrightOwners(self):
        return self._copyrightOwners

    @copyrightOwners.setter
    def copyrightOwners(self, value):
        self._copyrightOwners = value

    @property
    def aboutCvTerms(self):
        return self._aboutCvTerms

    @aboutCvTerms.setter
    def aboutCvTerms(self, value):
        self._aboutCvTerms = value

    @property
    def digitalImageGuid(self):
        return self._digitalImageGuid

    @digitalImageGuid.setter
    def digitalImageGuid(self, value):
        self._digitalImageGuid = value

    @property
    def digitalSourceType(self):
        return self._digitalSourceType

    @digitalSourceType.setter
    def digitalSourceType(self, value):
        self._digitalSourceType = value

    @property
    def embdEncRightsExprs(self):
        return self._embdEncRightsExprs

    @embdEncRightsExprs.setter
    def embdEncRightsExprs(self, value):
        self._embdEncRightsExprs = value

    @property
    def eventName(self):
        return self._eventName

    @eventName.setter
    def eventName(self, value):
        self._eventName = value

    @property
    def genres(self):
        return self._genres

    @genres.setter
    def genres(self, value):
        self._genres = value

    @property
    def imageRating(self):
        return self._imageRating

    @imageRating.setter
    def imageRating(self, value):
        self._imageRating = value

    @property
    def imageRegion(self):
        return self._imageRegion

    @imageRegion.setter
    def imageRegion(self, value):
        self._imageRegion = value

    @property
    def registryEntries(self):
        return self._registryEntries

    @registryEntries.setter
    def registryEntries(self, value):
        self._registryEntries = value

    @property
    def suppliers(self):
        return self._suppliers

    @suppliers.setter
    def suppliers(self, value):
        self._suppliers = value

    @property
    def imageSupplierImageId(self):
        return self._imageSupplierImageId

    @imageSupplierImageId.setter
    def imageSupplierImageId(self, value):
        self._imageSupplierImageId = value

    @property
    def licensors(self):
        return self._licensors

    @licensors.setter
    def licensors(self, value):
        self._licensors = value

    @property
    def linkedEncRightsExprs(self):
        return self._linkedEncRightsExprs

    @linkedEncRightsExprs.setter
    def linkedEncRightsExprs(self, value):
        self._linkedEncRightsExprs = value

    @property
    def locationCreated(self):
        return self._locationCreated

    @locationCreated.setter
    def locationCreated(self, value):
        self._locationCreated = value

    @property
    def locationsShown(self):
        return self._locationsShown

    @locationsShown.setter
    def locationsShown(self, value):
        self._locationsShown = value

    @property
    def minorModelAgeDisclosure(self):
        return self._minorModelAgeDisclosure

    @minorModelAgeDisclosure.setter
    def minorModelAgeDisclosure(self, value):
        self._minorModelAgeDisclosure = value

    @property
    def modelAges(self):
        return self._modelAges

    @modelAges.setter
    def modelAges(self, value):
        self._modelAges = value

    @property
    def modelReleaseDocuments(self):
        return self._modelReleaseDocuments

    @modelReleaseDocuments.setter
    def modelReleaseDocuments(self, value):
        self._modelReleaseDocuments = value

    @property
    def modelReleaseStatus(self):
        return self._modelReleaseStatus

    @modelReleaseStatus.setter
    def modelReleaseStatus(self, value):
        self._modelReleaseStatus = value

    @property
    def organisationInImageNames(self):
        return self._organisationInImageNames

    @organisationInImageNames.setter
    def organisationInImageNames(self, value):
        self._organisationInImageNames = value

    @property
    def personInImageNames(self):
        return self._personInImageNames

    @personInImageNames.setter
    def personInImageNames(self, value):
        self._personInImageNames = value

    @property
    def personsShown(self):
        return self._personsShown

    @personsShown.setter
    def personsShown(self, value):
        self._personsShown = value

    @property
    def productsShown(self):
        return self._productsShown

    @productsShown.setter
    def productsShown(self, value):
        self._productsShown = value

    @property
    def propertyReleaseDocuments(self):
        return self._propertyReleaseDocuments

    @propertyReleaseDocuments.setter
    def propertyReleaseDocuments(self, value):
        self._propertyReleaseDocuments = value

    @property
    def propertyReleaseStatus(self):
        return self._propertyReleaseStatus

    @propertyReleaseStatus.setter
    def propertyReleaseStatus(self, value):
        self._propertyReleaseStatus = value

    @property
    def webstatementRights(self):
        return self._webstatementRights

    @webstatementRights.setter
    def webstatementRights(self, value):
        self._webstatementRights = value
        

