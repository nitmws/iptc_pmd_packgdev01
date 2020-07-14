"""
    This module provides the most generic IPTC photo metadata classe
"""
from dataclasses import dataclass
from typing import List, Optional, Type
from .common import IptcPhotometadata, CreatorExt, ArtworkOrObject, CvTerm, EmbdEncRightsExpr, \
    Entity, ImageRegion, LinkedEncRightsExpr, Licensor, Location, \
    PersonWDetails, ProductWGtin, RegistryEntry


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
    def copyrightNotice(self) -> str:
        return self._copyrightNotice

    @copyrightNotice.setter
    def copyrightNotice(self, value: Optional[str]):
        self._copyrightNotice = value

    @property
    def creatorsExt(self) -> List[CreatorExt]:
        return self._creatorsExt

    @creatorsExt.setter
    def creatorsExt(self, value: Optional[List[CreatorExt]]):
        self._creatorsExt = value

    @property
    def jobtitle(self) -> str:
        return self._jobtitle

    @jobtitle.setter
    def jobtitle(self, value: Optional[str]):
        self._jobtitle = value

    @property
    def creditLine(self) -> str:
        return self._creditLine

    @creditLine.setter
    def creditLine(self, value: Optional[str]):
        self._creditLine = value

    @property
    def dateCreated(self) -> str:
        return self._dateCreated

    @dateCreated.setter
    def dateCreated(self, value: Optional[str]):
        self._dateCreated = value

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: Optional[str]):
        self._description = value

    @property
    def captionWriter(self) -> str:
        return self._captionWriter

    @captionWriter.setter
    def captionWriter(self, value: Optional[str]):
        self._captionWriter = value

    @property
    def headline(self) -> str:
        return self._headline

    @headline.setter
    def headline(self, value: Optional[str]):
        self._headline = value

    @property
    def instructions(self) -> str:
        return self._instructions

    @instructions.setter
    def instructions(self, value: Optional[str]):
        self._instructions = value

    @property
    def intellectualGenre(self) -> str:
        return self._intellectualGenre

    @intellectualGenre.setter
    def intellectualGenre(self, value: Optional[str]):
        self._intellectualGenre = value

    @property
    def jobid(self) -> str:
        return self._jobid

    @jobid.setter
    def jobid(self, value: Optional[str]):
        self._jobid = value

    @property
    def keywords(self) -> List[str]:
        return self._keywords

    @keywords.setter
    def keywords(self, value: Optional[List[str]]):
        self._keywords = value

    @property
    def provinceState(self) -> str:
        return self._provinceState

    @provinceState.setter
    def provinceState(self, value: Optional[str]):
        self._provinceState = value

    @property
    def usageTerms(self) -> str:
        return self._usageTerms

    @usageTerms.setter
    def usageTerms(self, value: Optional[str]):
        self._usageTerms = value

    @property
    def sceneCodes(self) -> List[str]:
        return self._sceneCodes

    @sceneCodes.setter
    def sceneCodes(self, value: Optional[List[str]]):
        self._sceneCodes = value

    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, value: Optional[str]):
        self._source = value

    @property
    def subjectCodes(self) -> List[str]:
        return self._subjectCodes

    @subjectCodes.setter
    def subjectCodes(self, value: Optional[List[str]]):
        self._subjectCodes = value

    @property
    def sublocationName(self) -> str:
        return self._sublocationName

    @sublocationName.setter
    def sublocationName(self, value: Optional[str]):
        self._sublocationName = value

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: Optional[str]):
        self._title = value

    @property
    def additionalModelInfo(self) -> str:
        return self._additionalModelInfo

    @additionalModelInfo.setter
    def additionalModelInfo(self, value: Optional[str]):
        self._additionalModelInfo = value

    @property
    def artworkOrObjects(self) -> List[Type[ArtworkOrObject]]:
        return self._artworkOrObjects

    @artworkOrObjects.setter
    def artworkOrObjects(self, value: Optional[List[Type[ArtworkOrObject]]]):
        self._artworkOrObjects = value

    @property
    def organisationInImageCodes(self) -> List[str]:
        return self._organisationInImageCodes

    @organisationInImageCodes.setter
    def organisationInImageCodes(self, value: Optional[List[str]]):
        self._organisationInImageCodes = value

    @property
    def copyrightOwners(self) -> List[Type[Entity]]:
        return self._copyrightOwners

    @copyrightOwners.setter
    def copyrightOwners(self, value: Optional[List[Type[Entity]]]):
        self._copyrightOwners = value

    @property
    def aboutCvTerms(self) -> List[Type[CvTerm]]:
        return self._aboutCvTerms

    @aboutCvTerms.setter
    def aboutCvTerms(self, value: Optional[List[Type[CvTerm]]]):
        self._aboutCvTerms = value

    @property
    def digitalImageGuid(self) -> str:
        return self._digitalImageGuid

    @digitalImageGuid.setter
    def digitalImageGuid(self, value: Optional[str]):
        self._digitalImageGuid = value

    @property
    def digitalSourceType(self) -> str:
        return self._digitalSourceType

    @digitalSourceType.setter
    def digitalSourceType(self, value: Optional[str]):
        self._digitalSourceType = value

    @property
    def embdEncRightsExprs(self) -> List[Type[EmbdEncRightsExpr]]:
        return self._embdEncRightsExprs

    @embdEncRightsExprs.setter
    def embdEncRightsExprs(self, value: Optional[List[Type[EmbdEncRightsExpr]]]):
        self._embdEncRightsExprs = value

    @property
    def eventName(self) -> str:
        return self._eventName

    @eventName.setter
    def eventName(self, value: Optional[str]):
        self._eventName = value

    @property
    def genres(self) -> List[Type[CvTerm]]:
        return self._genres

    @genres.setter
    def genres(self, value: Optional[List[Type[CvTerm]]]):
        self._genres = value

    @property
    def imageRating(self) -> int:
        return self._imageRating

    @imageRating.setter
    def imageRating(self, value: Optional[int]):
        self._imageRating = value

    @property
    def imageRegion(self) -> List[Type[ImageRegion]]:
        return self._imageRegion

    @imageRegion.setter
    def imageRegion(self, value: Optional[List[Type[ImageRegion]]]):
        self._imageRegion = value

    @property
    def registryEntries(self) -> List[Type[RegistryEntry]]:
        return self._registryEntries

    @registryEntries.setter
    def registryEntries(self, value: Optional[List[Type[RegistryEntry]]]):
        self._registryEntries = value

    @property
    def suppliers(self) -> List[Type[Entity]]:
        return self._suppliers

    @suppliers.setter
    def suppliers(self, value: Optional[List[Type[Entity]]]):
        self._suppliers = value

    @property
    def imageSupplierImageId(self) -> str:
        return self._imageSupplierImageId

    @imageSupplierImageId.setter
    def imageSupplierImageId(self, value: Optional[str]):
        self._imageSupplierImageId = value

    @property
    def licensors(self) -> List[Type[Licensor]]:
        return self._licensors

    @licensors.setter
    def licensors(self, value: Optional[List[Type[Licensor]]]):
        self._licensors = value

    @property
    def linkedEncRightsExprs(self) -> List[Type[LinkedEncRightsExpr]]:
        return self._linkedEncRightsExprs

    @linkedEncRightsExprs.setter
    def linkedEncRightsExprs(self, value: Optional[List[Type[LinkedEncRightsExpr]]]):
        self._linkedEncRightsExprs = value

    @property
    def locationCreated(self) -> Location:
        return self._locationCreated

    @locationCreated.setter
    def locationCreated(self, value: Optional[Location]):
        self._locationCreated = value

    @property
    def locationsShown(self) -> List[Type[Location]]:
        return self._locationsShown

    @locationsShown.setter
    def locationsShown(self, value: Optional[List[Type[Location]]]):
        self._locationsShown = value

    @property
    def minorModelAgeDisclosure(self) -> str:
        return self._minorModelAgeDisclosure

    @minorModelAgeDisclosure.setter
    def minorModelAgeDisclosure(self, value: Optional[str]):
        self._minorModelAgeDisclosure = value

    @property
    def modelAges(self) -> List[int]:
        return self._modelAges

    @modelAges.setter
    def modelAges(self, value: Optional[List[int]]):
        self._modelAges = value

    @property
    def modelReleaseDocuments(self) -> List[str]:
        return self._modelReleaseDocuments

    @modelReleaseDocuments.setter
    def modelReleaseDocuments(self, value: Optional[List[str]]):
        self._modelReleaseDocuments = value

    @property
    def modelReleaseStatus(self) -> str:
        return self._modelReleaseStatus

    @modelReleaseStatus.setter
    def modelReleaseStatus(self, value: Optional[str]):
        self._modelReleaseStatus = value

    @property
    def organisationInImageNames(self) -> List[str]:
        return self._organisationInImageNames

    @organisationInImageNames.setter
    def organisationInImageNames(self, value: Optional[List[str]]):
        self._organisationInImageNames = value

    @property
    def personInImageNames(self) -> List[str]:
        return self._personInImageNames

    @personInImageNames.setter
    def personInImageNames(self, value: Optional[List[str]]):
        self._personInImageNames = value

    @property
    def personsShown(self) -> List[Type[PersonWDetails]]:
        return self._personsShown

    @personsShown.setter
    def personsShown(self, value: Optional[List[Type[PersonWDetails]]]):
        self._personsShown = value

    @property
    def productsShown(self) -> List[Type[ProductWGtin]]:
        return self._productsShown

    @productsShown.setter
    def productsShown(self, value: Optional[List[Type[ProductWGtin]]]):
        self._productsShown = value

    @property
    def propertyReleaseDocuments(self) -> List[str]:
        return self._propertyReleaseDocuments

    @propertyReleaseDocuments.setter
    def propertyReleaseDocuments(self, value: Optional[List[str]]):
        self._propertyReleaseDocuments = value

    @property
    def propertyReleaseStatus(self) -> str:
        return self._propertyReleaseStatus

    @propertyReleaseStatus.setter
    def propertyReleaseStatus(self, value: Optional[str]):
        self._propertyReleaseStatus = value

    @property
    def webstatementRights(self) -> str:
        return self._webstatementRights

    @webstatementRights.setter
    def webstatementRights(self, value: Optional[str]):
        self._webstatementRights = value


