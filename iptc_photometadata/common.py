import os
import json
import copy
from pathlib import Path
from dataclasses import dataclass
from typing import List, Set, Dict, Tuple, Optional, Type
from enum import Enum
import jsonpickle
from .exiftool_util import *

"""
    ===========================================================================
    Specific IPTC Photo Metadata structure classes
"""


@dataclass
class IptcStructure:
    def todict(self):
        d = {}
        for attrname in vars(self):
            attrval = getattr(self, attrname)
            if attrval is not None:
                d[attrname] = attrval
        return d

@dataclass
class CreatorContactInfo(IptcStructure):
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    emailwork: Optional[str] = None
    phonework: Optional[str] = None
    postalCode: Optional[str] = None
    region: Optional[str] = None
    weburlwork: Optional[str] = None

    def todict_et(self):
        det = {}
        if self.address is not None:
            det['CiAdrExt'] = self.address
        if self.city is not None:
            det['CiAdrCity'] = self.city
        if self.country is not None:
            det['CiAdrCtry'] = self.country
        if self.emailwork is not None:
            det['CiEmailWork'] = self.emailwork
        if self.phonework is not None:
            det['CiTelWork'] = self.phonework
        if self.postalCode is not None:
            det['CiAdrPcode'] = self.postalCode
        if self.region is not None:
            det['CiAdrRegion'] = self.region
        if self.weburlwork is not None:
            det['CiUrlWork'] = self.weburlwork
        return det

@dataclass
class ArtworkOrObject(IptcStructure):
    circaDateCreated: Optional[str] = None
    contentDescription: Optional[str] = None
    contributionDescription: Optional[str] = None
    copyrightNotice: Optional[str] = None
    creatorNames: Optional[List[str]] = None
    creatorIdentifiers: Optional[List[str]] = None
    currentCopyrightOwnerIdentifier: Optional[str] = None
    currentCopyrightOwnerName: Optional[str] = None
    currentLicensorIdentifier: Optional[str] = None
    currentLicensorName: Optional[str] = None
    dateCreated: Optional[str] = None
    physicalDescription: Optional[str] = None
    source: Optional[str] = None
    sourceInventoryNr: Optional[str] = None
    sourceInventoryUrl: Optional[str] = None
    stylePeriod: Optional[List[str]] = None
    title: Optional[str] = None

@dataclass
class CvTerm(IptcStructure):
    cvId: Optional[str] = None
    cvTermId: Optional[str] = None
    cvTermName: Optional[str] = None
    cvTermRefinedAbout: Optional[str] = None

    def todict_et(self):
        det = {}
        if self.cvId is not None:
            det['CvId'] = self.cvId
        if self.cvTermId is not None:
            det['CvTermId'] = self.cvTermId
        if self.cvTermName is not None:
            det['CvTermName'] = self.cvTermName
        if self.cvTermRefinedAbout is not None:
            det['CvTermRefinedAbout'] = self.cvTermRefinedAbout
        return det

    def loadfrom_seret(self, seretCvTerm: dict):
        _propsetcount = 0
        if 'CvId' in seretCvTerm:
            self.cvId = seretCvTerm['CvId']
            _propsetcount += 1
        if 'CvTermId' in seretCvTerm:
            self.cvTermId = seretCvTerm['CvTermId']
            _propsetcount += 1
        if 'CvTermName' in seretCvTerm:
            self.cvTermName = seretCvTerm['CvTermName']
            _propsetcount += 1
        if 'CvTermRefinedAbout' in seretCvTerm:
            self.cvTermRefinedAbout = seretCvTerm['CvTermRefinedAbout']
            _propsetcount += 1
        if _propsetcount == 0:
            self = None

@dataclass
class EmbdEncRightsExpr(IptcStructure):
    rightsExprLangId: Optional[str] = None
    rightsExprEncType: Optional[str] = None
    encRightsExpr: Optional[str] = None

    def todict_et(self):
        det = {}
        if self.rightsExprLangId is not None:
            det['RightsExprLangId'] = self.rightsExprLangId
        if self.rightsExprEncType is not None:
            det['RightsExprEncType'] = self.rightsExprEncType
        if self.encRightsExpr is not None:
            det['EncRightsExpr'] = self.encRightsExpr
        return det

    def loadfrom_seret(self, seretEncEncRightsExpr: dict):
        _propsetcount = 0
        if 'RightsExprLangId' in seretEncEncRightsExpr:
            _propsetcount += 1
            self.rightsExprLangId = seretEncEncRightsExpr['RightsExprLangId']
        if 'RightsExprEncType' in seretEncEncRightsExpr:
            _propsetcount += 1
            self.rightsExprEncType = seretEncEncRightsExpr['RightsExprEncType']
        if 'EncRightsExpr' in seretEncEncRightsExpr:
            _propsetcount += 1
            self.encRightsExpr = seretEncEncRightsExpr['EncRightsExpr']
        if _propsetcount == 0:
            self = None

@dataclass
class Entity(IptcStructure):
    identifiers: Optional[List[str]] = None
    name: Optional[str] = None

    def todict_plus_et(self, pluspropname: str) -> dict:
        det = {}
        if self.identifiers is not None:
            det[pluspropname + 'ID'] = self.identifiers
        if self.name is not None:
            det[pluspropname + 'Name'] = self.name
        return det

    def loadfrom_plus_seret(self, seretEntity: dict, pluspropname: str):
        _propsetcount = 0
        if pluspropname + 'ID' in seretEntity:
            _propsetcount += 1
            self.identifiers = [seretEntity[pluspropname + 'ID']]
        if pluspropname + 'Name' in seretEntity:
            _propsetcount += 1
            self.name = seretEntity[pluspropname + 'Name']
        if _propsetcount == 0:
            self = None

@dataclass
class RegionBoundaryPoint(IptcStructure):
    rbX: Optional[int] = None
    rbY: Optional[int] = None

@dataclass
class RegionBoundary(IptcStructure):
    rbShape: Optional[str] = None
    rbUnit: Optional[str] = None
    rbX: Optional[int] = None
    rbY: Optional[int] = None
    rbW: Optional[int] = None
    rbH: Optional[int] = None
    rbRx: Optional[int] = None
    rbVertices: Optional[List[Type[RegionBoundaryPoint]]] = None

@dataclass
class ImageRegion(IptcStructure):
    regionBoundary: Optional[Type[RegionBoundary]] = None
    rId: Optional[str] = None
    name: Optional[str] = None
    rCtype: Optional[List[Type[Entity]]] = None
    rRole: Optional[List[Type[Entity]]] = None
    any: Optional[List[dict]] = None

@dataclass
class LinkedEncRightsExpr(IptcStructure):
    rightsExprLangId: Optional[str] = None
    rightsExprEncType: Optional[str] = None
    linkedRightsExpr: Optional[str] = None

    def todict_et(self):
        det = {}
        if self.rightsExprLangId is not None:
            det['RightsExprLangId'] = self.rightsExprLangId
        if self.rightsExprEncType is not None:
            det['RightsExprEncType'] = self.rightsExprEncType
        if self.linkedRightsExpr is not None:
            det['LinkedRightsExpr'] = self.linkedRightsExpr
        return det

    def loadfrom_seret(self, seretLnkEncRightsExpr: dict):
        _propsetcount = 0
        if 'RightsExprLangId' in seretLnkEncRightsExpr:
            _propsetcount += 1
            self.rightsExprLangId = seretLnkEncRightsExpr['RightsExprLangId']
        if 'RightsExprEncType' in seretLnkEncRightsExpr:
            _propsetcount += 1
            self.rightsExprEncType = seretLnkEncRightsExpr['RightsExprEncType']
        if 'LinkedRightsExpr' in seretLnkEncRightsExpr:
            _propsetcount += 1
            self.linkedRightsExpr = seretLnkEncRightsExpr['LinkedRightsExpr']
        if _propsetcount == 0:
            self = None

@dataclass
class Licensor(IptcStructure):
    licensorID: Optional[str] = None
    licensorName: Optional[str] = None
    licensorURL: Optional[str] = None

    def todict_et(self):
        det = {}
        if self.licensorID is not None:
            det['LicensorID'] = self.licensorID
        if self.licensorName is not None:
            det['LicensorName'] = self.licensorName
        if self.licensorURL is not None:
            det['LicensorURL'] = self.licensorURL
        return det

    def loadfrom_seret(self, seretLicensor: dict):
        _propsetcount = 0
        if 'LicensorID' in seretLicensor:
            _propsetcount += 1
            self.licensorID = seretLicensor['LicensorID']
        if 'LicensorName' in seretLicensor:
            _propsetcount += 1
            self.licensorName = seretLicensor['LicensorName']
        if 'LicensorURL' in seretLicensor:
            _propsetcount += 1
            self.licensorURL = seretLicensor['LicensorURL']
        if _propsetcount == 0:
            self = None


@dataclass
class Location(IptcStructure):
    city: Optional[str] = None
    countryCode: Optional[str] = None
    countryName: Optional[str] = None
    gpsAltitude: Optional[int] = None
    gpsLatitude: Optional[int] = None
    gpsLongitude: Optional[int] = None
    identifiers: Optional[List[str]] = None
    name: Optional[str] = None
    provinceState: Optional[str] = None
    sublocation: Optional[str] = None
    worldRegion: Optional[str] = None

    def todict_et(self):
        det = {}
        if self.identifiers is not None:
            det['LocationId'] = self.identifiers
        if self.city is not None:
            det['City'] = self.city
        if self.countryCode is not None:
            det['CountryCode'] = self.countryCode
        if self.countryName is not None:
            det['CountryName'] = self.countryName
        if self.provinceState is not None:
            det['ProvinceState'] = self.provinceState
        if self.sublocation is not None:
            det['Sublocation'] = self.sublocation
        if self.worldRegion is not None:
            det['WorldRegion'] = self.worldRegion
        return det

    def loadfrom_seret(self, seretLocation: dict):
        _propsetcount = 0
        if 'LocationId' in seretLocation:
            self.identifiers = seretLocation['LocationId']
            _propsetcount += 1
        if 'City' in seretLocation:
            self.city = seretLocation['City']
            _propsetcount += 1
        if 'CountryCode' in seretLocation:
            self.countryCode = seretLocation['CountryCode']
            _propsetcount += 1
        if 'CountryName' in seretLocation:
            self.countryName = seretLocation['CountryName']
            _propsetcount += 1
        if 'ProvinceState' in seretLocation:
            self.provinceState = seretLocation['ProvinceState']
            _propsetcount += 1
        if 'Sublocation' in seretLocation:
            self.sublocation = seretLocation['Sublocation']
            _propsetcount += 1
        if 'WorldRegion' in seretLocation:
            self.worldRegion = seretLocation['WorldRegion']
            _propsetcount += 1
        if _propsetcount == 0:
            self = None


@dataclass
class PersonWDetails(IptcStructure):
    characteristics: Optional[List[Type[CvTerm]]] = None
    description: Optional[str] = None
    identifiers: Optional[List[str]] = None
    name: Optional[str] = None

    def todict(self):
        d = {}
        for attrname in vars(self):
            attrval = getattr(self, attrname)
            if attrname == 'characteristics':
                if self.characteristics is not None:
                    charlist = []
                    for characteristic in self.characteristics:
                        dchar = characteristic.todict()
                        charlist.append(dchar)
                    d[attrname] = charlist
            else:
                if attrval is not None:
                    d[attrname] = attrval
        return d

    def todict_et(self) -> dict:
        det = {}
        if self.characteristics is not None:
            detchars = []
            for characteristic in self.characteristics:
                detchar = characteristic.todict_et()
                detchars.append(detchar)
            det['PersonCharacteristic'] = detchars
        if self.description is not None:
            det['PersonDescription'] = self.description
        if self.identifiers is not None:
            det['PersonId'] = self.identifiers
        if self.name is not None:
            det['PersonName'] = self.name
        return det

@dataclass
class ProductWGtin(IptcStructure):
    description: Optional[str] = None
    gtin: Optional[str] = None
    name: Optional[str] = None

    def loadfrom_seret(self, seretProduct: dict):
        _propsetcount = 0
        if 'ProductGTIN' in seretProduct:
            _propsetcount += 1
            self.gtin = seretProduct['ProductGTIN']
        if 'ProductName' in seretProduct:
            _propsetcount += 1
            self.name = seretProduct['ProductName']
        if 'ProductDescription' in seretProduct:
            _propsetcount += 1
            self.description = seretProduct['ProductDescription']
        if _propsetcount == 0:
            self = None


@dataclass
class RegistryEntry(IptcStructure):
    assetIdentifier: Optional[str] = None
    registryIdentifier: Optional[str] = None
    role: Optional[str] = None

    def loadfrom_seret(self, seretRegistryEntry: dict):
        _propsetcount = 0
        if 'RegOrgId' in seretRegistryEntry:
            _propsetcount += 1
            self.registryIdentifier = seretRegistryEntry['RegOrgId']
        if 'RegItemId' in seretRegistryEntry:
            _propsetcount += 1
            self.assetIdentifier = seretRegistryEntry['RegItemId']
        if 'RegEntryRole' in seretRegistryEntry:
            _propsetcount += 1
            self.role = seretRegistryEntry['RegEntryRole']
        if _propsetcount == 0:
            self = None

@dataclass
class CreatorExt(IptcStructure):
    identifiers: Optional[List[str]] = None
    name: Optional[str] = None
    jobtitle: Optional[str] = None
    creatorContactInfo: Optional[Type[CreatorContactInfo]] = None

    def todict(self):
        d = {}
        for attrname in vars(self):
            attrval = getattr(self, attrname)
            if attrname == 'creatorContactInfo':
                if self.creatorContactInfo is not None:
                    d[attrname] = self.creatorContactInfo.todict()
            else:
                if attrval is not None:
                    d[attrname] = attrval
        return d


"""
    ===========================================================================
    Enumeration classes
"""


class IptcSerializationFormat(Enum):
    IPTCIIM = 1
    XMP = 2
    EXIF = 3


class IptcDeprecatedLocationRole(Enum):
    CREATED = 1
    SHOWN = 2

class PropertyOccurrence(Enum):
    NONE = 1
    ONE = 2
    MANY = 3


"""
    ===========================================================================
    The generic IptcPhotometadata class
"""

@dataclass
class IptcPhotometadata:
    """Generic IPTC photo metadata: no properties/tags are defined.

        This class is intended to be ancestor of IPTC photo metadata classes with a specific set of properties.
    """
    # Internal Note: Which properties may be supported: see Top Level Property Names in
    # https://docs.google.com/spreadsheets/d/1hfU6L1sPrueyyMCUqe4gqFjHPoLHQvFziy49DA09Cek/edit?usp=sharing
    # IPTC Core schema
    _copyrightNotice: Optional[str] = None
    _creatorsExt: Optional[List[CreatorExt]] = None
    _creditLine: Optional[str] = None
    _dateCreated: Optional[str] = None
    _description: Optional[str] = None
    _captionWriter: Optional[str] = None
    _headline: Optional[str] = None
    _instructions: Optional[str] = None
    _intellectualGenre: Optional[str] = None
    _jobid: Optional[str] = None
    _keywords: Optional[List[str]] = None
    _usageTerms: Optional[str] = None
    _sceneCodes: Optional[List[str]] = None
    _source: Optional[str] = None
    _subjectCodes: Optional[List[str]] = None
    _title: Optional[str] = None
    # IPTC Extension schema
    _additionalModelInfo: Optional[str] = None
    _artworkOrObjects: Optional[List[Type[ArtworkOrObject]]] = None
    _organisationInImageCodes: Optional[List[str]] = None
    _copyrightOwners: Optional[List[Type[Entity]]] = None
    _aboutCvTerms: Optional[List[Type[CvTerm]]] = None
    _digitalImageGuid: Optional[str] = None
    _digitalSourceType: Optional[str] = None
    _embdEncRightsExprs: Optional[List[Type[EmbdEncRightsExpr]]] = None
    _eventName: Optional[str] = None
    _genres: Optional[List[Type[CvTerm]]] = None
    _imageRating: Optional[int] = None
    _imageRegion: Optional[List[Type[ImageRegion]]] = None
    _registryEntries: Optional[List[Type[RegistryEntry]]] = None
    _suppliers: Optional[List[Type[Entity]]] = None
    _imageSupplierImageId: Optional[str] = None
    _licensors: Optional[List[Type[Licensor]]] = None
    _linkedEncRightsExprs: Optional[List[Type[LinkedEncRightsExpr]]] = None
    _locationCreated: Optional[Type[Location]] = None
    _locationsShown: Optional[List[Type[Location]]] = None
    _minorModelAgeDisclosure: Optional[str] = None
    _modelAges: Optional[List[int]] = None
    _modelReleaseDocuments: Optional[List[str]] = None
    _modelReleaseStatus: Optional[str] = None
    _organisationInImageNames: Optional[List[str]] = None
    _personInImageNames: Optional[List[str]] = None
    _personsShown: Optional[List[Type[PersonWDetails]]] = None
    _productsShown: Optional[List[Type[ProductWGtin]]] = None
    _propertyReleaseDocuments: Optional[List[str]] = None
    _propertyReleaseStatus: Optional[str] = None
    _webstatementRights: Optional[str] = None

    semiptc_propnames = ('_copyrightNotice', '_creatorsExt', '_creditLine', '_dateCreated',
                         '_description', '_captionWriter', '_headline', '_instructions',
                         '_intellectualGenre', '_jobid', '_keywords', '_usageTerms', '_sceneCodes', '_source',
                         '_subjectCodes', '_title',
                         '_additionalModelInfo', '_artworkOrObjects', '_organisationInImageCodes', '_copyrightOwners',
                         '_aboutCvTerms', '_digitalImageGuid', '_digitalSourceType', '_embdEncRightsExprs',
                         '_eventName', '_genres', '_imageRating', '_imageRegion', '_registryEntries',
                         '_suppliers', '_imageSupplierImageId', '_licensors', '_linkedEncRightsExprs',
                         '_locationCreated', '_locationsShown',
                         '_minorModelAgeDisclosure', '_modelAges', '_modelReleaseDocuments', '_modelReleaseStatus',
                         '_organisationInImageNames', '_personInImageNames', '_personsShown', '_productsShown',
                         '_propertyReleaseDocuments', '_propertyReleaseStatus', '_webstatementRights')

    def __init__(self):
        self._currentdir: str = ''
        self._supported_iptcpmd_tlprops = ()  # Tuple of semantic IPTC metadata property names supported by a (sub)class
        # Role of the deprecated IPTC location properties: they represent Location CREATED or Location SHOWN
        self._deprlocationrole: IptcDeprecatedLocationRole = IptcDeprecatedLocationRole.SHOWN
        # Reading seret metadata: should the parsing follow the IPTC Photo Metadata Standard strictly: True or False
        self._ipmd_parse_strict = True
        # dict holding the semantic IPTC Photo Metadata properties
        self._semiptc_metadata = {}
        # dict holding the serialization in IPTC IIM, XMP and Exif of the semantic IPTC metadata, using ExifTool naming
        self._seret_metadata = {}
        # the two dicts below: key = IPTC property name, value = transformation method
        self._semiptc2seret_registry = {}
        self._seret2semiptc_registry = {}
        # iterate across names bound to this class and register the methods for transforming metadata with typical names
        _dirnames = dir(self)
        for _dirname in _dirnames:
            if _dirname.startswith('semiptc2seret'):
                _propname = _dirname[14:]
                self._semiptc2seret_registry[_propname] = getattr(self, _dirname)
            if _dirname.startswith('seret2semiptc'):
                _propname = _dirname[14:]
                self._seret2semiptc_registry[_propname] = getattr(self, _dirname)

    """
        **********************************************************
        Region of getters and setters of attributes of this class
    """

    @property
    def seret_metadata(self):
        """Gets dictionary of serialized IPTC Photo Metadata, using ExifTool naming"""
        return self._seret_metadata

    @seret_metadata.setter
    def seret_metadata(self, seret_metadata):
        """Sets dictionary of serialized IPTC Photo Metadata, using ExifTool naming"""
        self._seret_metadata = seret_metadata

    @property
    def currentdir(self):
        """Gets the current directory of the application using this classe"""
        return self._currentdir

    @currentdir.setter
    def currentdir(self, thecurrentdir):
        """Sets the current directory of the application using this classe"""
        if os.path.isdir(thecurrentdir):
            self._currentdir = thecurrentdir

    @property
    def deprlocationrole(self) -> IptcDeprecatedLocationRole:
        return self._deprlocationrole

    @deprlocationrole.setter
    def deprlocationrole(self, role: IptcDeprecatedLocationRole):
        self._deprlocationrole = role

    @property
    def ipmd_parse_strict(self) -> bool:
        return self._ipmd_parse_strict

    @ipmd_parse_strict.setter
    def ipmd_parse_strict(self, bestrict: bool):
        self._ipmd_parse_strict = bestrict

    """
        *******************************************************************
        Exporting and importing metadata to JSON files
    """

    def export_semiptc_as_jsonfile(self, json_fp):
        """Exports the semantic IPTC Photo Metadata of this class to a JSON file"""
        self._generate_semiptc_metadata()
        filename = Path(json_fp)
        filename = filename.with_suffix('.json')
        with filename.open(mode='w') as _f:
            _f.write(json.dumps(self._semiptc_metadata, indent=2,
                                ensure_ascii=False, sort_keys=True))

    def export_self_as_jsonfile(self, json_fp):
        """Exports the current instance this class to a JSON file"""
        selfstr = jsonpickle.encode(self, indent=2)
        filename = Path(json_fp)
        filename = filename.with_suffix('.json')
        with filename.open(mode='w') as _f:
            _f.write(selfstr)


    def import_semiptc_from_jsonfile(self, json_fp):
        """Imports the semantic IPTC Photo Metadata of this class from a JSON file"""
        if json_fp:
            if os.path.isfile(json_fp):
                with open(json_fp, "r") as pmdfile:
                    self._semiptc_metadata = json.load(pmdfile)

    def export_seret_as_jsonfile(self, json_fp):
        """Exports the serialized IPTC metadata using ExifTool naming of this class to a JSON file"""
        filename = Path(json_fp)
        filename = filename.with_suffix('.json')
        with filename.open(mode='w') as _f:
            _f.write(json.dumps(self._seret_metadata, indent=2,
                                ensure_ascii=False, sort_keys=True))

    def import_seret_from_jsonfile(self, json_fp):
        """Imports the serialized IPTC metadata using ExifTool naming  of this class from a JSON file"""
        if json_fp:
            if os.path.isfile(json_fp):
                with open(json_fp, "r") as pmdfile:
                    etjson = json.load(pmdfile)
                    if isinstance(etjson, list):
                        self._seret_metadata = etjson[0]
                    else:
                        self._seret_metadata = etjson

    """
        ****************************************************************************************************
        Region of methods for transforming semantic IPTC metadata to serialized metadata in Exiftool syntax
    """

    def transform_semiptc_metadata_to_seret(self):
        """Transforms all semantic IPTC Photo Metadata to metadata serialized as Exif/IIM/XMP using ExifTool naming"""
        # This method iterates across the supported IPTC metadata properties supported by a derived class,
        #   the corresponding "semantic IPTC metadata to serialized metadata in Exiftool syntax"
        #   transformation methods are called.
        for iptcpmd_tlprop in self._supported_iptcpmd_tlprops:
            if iptcpmd_tlprop in self._semiptc2seret_registry.keys():
                self._semiptc2seret_registry[iptcpmd_tlprop]()

    def semiptc2seret_copyrightNotice(self):
        """Transforms the semantic IPTC property Copyright Notice to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._copyrightNotice is not None:
            self._semiptc2seret_simple_multi1(self._copyrightNotice, 'IFD0:Copyright', 'IPTC:CopyrightNotice',
                                            'XMP-dc:Rights')

    def semiptc2seret_creatorsExt(self):
        """Transforms the semantic IPTC property Creators Extensive to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._creatorsExt is not None:
            # Collect the properties of a creator in different caches
            xmpimgcreators = []
            creator_names = []
            creator_jobtitles = []
            creator_contactinfo = None
            for creatorExt in self._creatorsExt:
                if creatorExt.name is not None:
                    creator_names.append(creatorExt.name)
                if creatorExt.jobtitle is not None:
                    creator_jobtitles.append(creatorExt.jobtitle)
                if creator_contactinfo is None:
                    if creatorExt.creatorContactInfo is not None:
                        creator_contactinfo = creatorExt.creatorContactInfo
                xmpimgcreator = {}
                if creatorExt.identifiers is not None:
                    xmpimgcreator['ImageCreatorID'] = creatorExt.identifiers[0]
                if creatorExt.name is not None:
                    xmpimgcreator['ImageCreatorName'] = creatorExt.name
                xmpimgcreators.append(xmpimgcreator)
            # embed the caches as serialized metadata properties
            self._seret_metadata['XMP-plus:ImageCreator'] = xmpimgcreators
            if len(creator_names) > 0:
                self._seret_metadata['IFD0:Artist'] = creator_names[0]
                self._seret_metadata['IPTC:By-line'] = creator_names
                self._seret_metadata['XMP-dc:Creator'] = creator_names
            if len(creator_jobtitles) > 0:
                self._seret_metadata['IPTC:By-lineTitle'] = creator_jobtitles
                self._seret_metadata['XMP-photoshop:AuthorsPosition'] = creator_jobtitles[0]
            if creator_contactinfo is not None:
                self._seret_metadata['XMP-iptcCore:CreatorContactInfo'] = creator_contactinfo.todict_et()



    def semiptc2seret_creditLine(self):
        """Transforms the semantic IPTC property Credit Line to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._creditLine is not None:
            self._semiptc2seret_simple_multi1(self._creditLine, None, 'IPTC:Credit', 'XMP-photoshop:Credit')

    def semiptc2seret_dateCreated(self):
        """Transforms the semantic IPTC property Date Created to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._dateCreated is not None:
            # used format: YYYY-MM-DD"T"hh:mm:ss[tz]
            daypart = self._dateCreated[:10]
            daypartet = daypart.replace('-', ':')
            timepart = self._dateCreated[11:19]
            timezonepart = '+00:00'
            if (len(self._dateCreated) > 19):
                timezonepart = self._dateCreated[19:]
            self._seret_metadata['ExifIFD:DateTimeOriginal'] = daypartet + ' ' + timepart
            self._seret_metadata['IPTC:DateCreated'] = daypartet
            self._seret_metadata['IPTC:TimeCreated'] = timepart + timezonepart
            self._seret_metadata['XMP-photoshop:DateCreated'] = daypartet + ' ' + timepart + timezonepart

    def semiptc2seret_captionWriter(self):
        """Transforms the semantic IPTC property Caption Writer to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._captionWriter is not None:
            self._semiptc2seret_simple_multi1(self._captionWriter, None, 'IPTC:Writer-Editor',
                                              'XMP-photoshop:CaptionWriter')

    def semiptc2seret_description(self):
        """Transforms the semantic IPTC property Description/Caption to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._description is not None:
            self._semiptc2seret_simple_multi1(self._description, 'EXIF:ImageDescription', 'IPTC:Caption-Abstract',
                                            'XMP-dc:Description')

    def semiptc2seret_headline(self):
        """Transforms the semantic IPTC property Headline to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._headline is not None:
            self._semiptc2seret_simple_multi1(self._headline, None, 'IPTC:Headline', 'XMP-photoshop:Headline')

    def semiptc2seret_instructions(self):
        """Transforms the semantic IPTC property Instructions to metadata serialized as Exif/IIM/XMP
                            using ExifTool naming"""
        if self._instructions is not None:
            self._semiptc2seret_simple_multi1(self._instructions, None, 'IPTC:SpecialInstructions',
                                              'XMP-photoshop:Instructions')

    def semiptc2seret_intellectualGenre(self):
        """Transforms the semantic IPTC property Intellectual Genre to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._intellectualGenre is not None:
            self._semiptc2seret_simple_multi1(self._intellectualGenre, None, 'IPTC:ObjectAttributeReference',
                                              'XMP-iptcCore:IntellectualGenre')

    def semiptc2seret_jobid(self):
        """Transforms the semantic IPTC property Job Id to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._jobid is not None:
            self._semiptc2seret_simple_multi1(self._jobid, None, 'IPTC:OriginalTransmissionReference',
                                              'XMP-photoshop:TransmissionReference')

    def semiptc2seret_keywords(self):
        """Transforms the semantic IPTC property Keywords to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._keywords is not None:
            self._semiptc2seret_simple_multi1(self._keywords, None, 'IPTC:Keywords', 'XMP-dc:Subject')

    def semiptc2seret_usageTerms(self):
        """Transforms the semantic IPTC property Rights Usage Terms to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._usageTerms is not None:
            self._semiptc2seret_simple_multi1(self._usageTerms, None, None, 'XMP-xmpRights:UsageTerms')

    def semiptc2seret_sceneCodes(self):
        """Transforms the semantic IPTC property Scene Codes to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._sceneCodes is not None:
            self._semiptc2seret_simple_multi1(self._sceneCodes, None, None, 'XMP-iptcCore:Scene')

    def semiptc2seret_source(self):
        """Transforms the semantic IPTC property Source to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._source is not None:
            self._semiptc2seret_simple_multi1(self._source, None, 'IPTC:Source', 'XMP-photoshop:Source')

    def semiptc2seret_subjectCodes(self):
        """Transforms the semantic IPTC property Subject Code to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._subjectCodes is not None:
            self._semiptc2seret_simple_multi1(self._subjectCodes, None, 'IPTC:SubjectReference',
                                              'XMP-iptcCore:SubjectCode')

    def semiptc2seret_title(self):
        """Transforms the semantic IPTC property Title to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._title is not None:
            self._semiptc2seret_simple_multi1(self._title, 'IPTC:ObjectName', 'XMP-dc:Title')

    # ************************************************************
    # IPTC Extension schema properties

    def semiptc2seret_aboutCvTerms(self):
        """Transforms the semantic IPTC property CV-Term About Image to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._aboutCvTerms is not None:
            if len(self._aboutCvTerms) > 0:
                xmpcvterms = []
                for aboutCvTerm in self._aboutCvTerms:
                    xmpcvterms.append(aboutCvTerm.todict_et())
                self._seret_metadata['XMP-iptcExt:AboutCvTerm'] = xmpcvterms

    def semiptc2seret_additionalModelInfo(self):
        """Transforms the semantic IPTC property Additional Model Information to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._additionalModelInfo is not None:
            self._seret_metadata['XMP-iptcExt:AdditionalModelInformation'] = self._additionalModelInfo

    def semiptc2seret_artworkOrObjects(self):
        """Transforms the semantic IPTC property Artwork or Objects in the Image to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._artworkOrObjects is not None:
            pass

    def semiptc2seret_organisationInImageCodes(self):
        """Transforms the semantic IPTC property Code of Organisation Feature in the Image to metadata serialized
            as Exif/IIM/XMP using ExifTool naming"""
        if self._organisationInImageCodes is not None:
            self._seret_metadata['XMP-iptcExt:OrganisationInImageCode'] = self._organisationInImageCodes

    def semiptc2seret_organisationInImageNames(self):
        """Transforms the semantic IPTC property Name of Organisation Feature in the Image to metadata serialized
            as Exif/IIM/XMP using ExifTool naming"""
        if self._organisationInImageNames is not None:
            self._seret_metadata['XMP-iptcExt:OrganisationInImageName'] = self._organisationInImageNames

    def semiptc2seret_copyrightOwners(self):
        """Transforms the semantic IPTC property Copyright Owner to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._copyrightOwners is not None:
            self._semiptc2seret_plusentities_xmp(self._copyrightOwners, 'CopyrightOwner', 'XMP-plus:CopyrightOwner')

    def semiptc2seret_digitalImageGuid(self):
        """Transforms the semantic IPTC property Digital Image GUID to metadata serialized as Exif/IIM/XMP
                    using ExifTool naming"""
        if self._digitalImageGuid is not None:
            self._seret_metadata['XMP-iptcExt:DigitalImageGUID'] = self._digitalImageGuid

    def semiptc2seret_digitalSourceType(self):
        """Transforms the semantic IPTC property Digital Source Type to metadata serialized as Exif/IIM/XMP
                    using ExifTool naming"""
        if self._digitalSourceType is not None:
            self._seret_metadata['XMP-iptcExt:DigitalSourceType'] = self._digitalSourceType

    def semiptc2seret_embdEncRightsExprs(self):
        """Transforms the semantic IPTC property Embedded Encoded Rights Expression to metadata serialized
                    as Exif/IIM/XMP using ExifTool naming"""
        if self._embdEncRightsExprs is not None:
            if len(self._embdEncRightsExprs) > 0:
                xmpembdEncRightsExprs = []
                for embdEncRightsExpr in self._embdEncRightsExprs:
                    xmpembdEncRightsExprs.append(embdEncRightsExpr.todict_et())
                self._seret_metadata['XMP-iptcExt:EmbdEncRightsExpr'] = xmpembdEncRightsExprs

    def semiptc2seret_eventName(self):
        """Transforms the semantic IPTC property Event to metadata serialized as Exif/IIM/XMP
                    using ExifTool naming"""
        if self._eventName is not None:
            self._seret_metadata['XMP-iptcExt:Event'] = self._eventName

    def semiptc2seret_genres(self):
        """Transforms the semantic IPTC property Genre to metadata serialized as Exif/IIM/XMP
                    using ExifTool naming"""
        if self._genres is not None:
            if len(self._genres) > 0:
                xmpgenres = []
                for genre in self._genres:
                    xmpgenres.append(genre.todict_et())
                self._seret_metadata['XMP-iptcExt:Genre'] = xmpgenres

    def semiptc2seret_imageRating(self):
        """Transforms the semantic IPTC property Image Rating to metadata serialized as Exif/IIM/XMP
                    using ExifTool naming"""
        if self._imageRating is not None:
            rating_str = str(self._imageRating) + '.0'
            self._seret_metadata['XMP-xmp:Rating'] = rating_str

    def semiptc2seret_registryEntries(self):
        """Transforms the semantic IPTC property Image Registry Entry to metadata serialized as Exif/IIM/XMP
                    using ExifTool naming"""
        if self._registryEntries is not None:
            if len(self._registryEntries) > 0:
                xmpregentries = []
                for regentry in self._registryEntries:
                    xmpregentry = {}
                    if regentry.registryIdentifier is not None:
                        xmpregentry['RegOrgId'] = regentry.registryIdentifier
                    if regentry.assetIdentifier is not None:
                        xmpregentry['RegItemId'] = regentry.assetIdentifier
                    if regentry.role is not None:
                        xmpregentry['RegEntryRole'] = regentry.role
                    if xmpregentry != {}:
                        xmpregentries.append(xmpregentry)
                if len(xmpregentries) > 0:
                    self._seret_metadata['XMP-iptcExt:RegistryID'] = xmpregentries

    def semiptc2seret_suppliers(self):
        """Transforms the semantic IPTC property Image Supplier to metadata serialized as Exif/IIM/XMP
            using ExifTool naming"""
        if self._suppliers is not None:
            self._semiptc2seret_plusentities_xmp(self._suppliers, 'ImageSupplier', 'XMP-plus:ImageSupplier')

    def semiptc2seret_imageSupplierImageId(self):
        """Transforms the semantic IPTC property Image Supplier Image Id to metadata serialized as Exif/IIM/XMP
                    using ExifTool naming"""
        if self._imageSupplierImageId is not None:
            self._seret_metadata['XMP-plus:ImageSupplierImageID'] = self._imageSupplierImageId

    def semiptc2seret_linkedEncRightsExprs(self):
        """Transforms the semantic IPTC property Linked Encoded Rights Expression to metadata serialized as Exif/IIM/XMP
                    using ExifTool naming"""
        if self._linkedEncRightsExprs is not None:
            if len(self._linkedEncRightsExprs) > 0:
                xmplinkedEncRightsExprs = []
                for linkedEncRightsExpr in self._linkedEncRightsExprs:
                    xmplinkedEncRightsExprs.append(linkedEncRightsExpr.todict_et())
                self._seret_metadata['XMP-iptcExt:LinkedEncRightsExpr'] = xmplinkedEncRightsExprs

    def semiptc2seret_licensors(self):
        """Transforms the semantic IPTC property Licensor to metadata serialized as Exif/IIM/XMP
                    using ExifTool naming"""
        if self._licensors is not None:
            if len(self._licensors) > 0:
                xmplicensors = []
                licctr = 0  # PLUS: max 3 Licensor
                for licensor in self._licensors:
                    licctr += 1
                    if licctr > 3:  # PLUS spec: max 3 Licensor entities
                        break
                    xmplicensors.append(licensor.todict_et())
                self._seret_metadata['XMP-plus:Licensor'] = xmplicensors

    def semiptc2seret_locationCreated(self):
        """Transforms the semantic IPTC property Location Created to metadata serialized as Exif/IIM/XMP
                    using ExifTool naming"""
        if self._locationCreated is not None:
            xmplocationcreated = self._locationCreated.todict_et()
            if xmplocationcreated != {}:
                self._seret_metadata['XMP-iptcExt:LocationCreated'] = xmplocationcreated
            if self._deprlocationrole == IptcDeprecatedLocationRole.CREATED:
                self._semitptc2seret_deprec_location(self._locationCreated)

    def semiptc2seret_locationsShown(self):
        """Transforms the semantic IPTC property Location Shown in the Image to metadata serialized as Exif/IIM/XMP
                    using ExifTool naming"""
        if self._locationsShown is not None:
            if len(self._locationsShown) > 0:
                itemctr = 0
                xmplocationsshown = []
                for locationShown in self._locationsShown:
                    itemctr += 1
                    xmplocationshown = locationShown.todict_et()
                    if xmplocationsshown != {}:
                        xmplocationsshown.append(xmplocationshown)
                    if self._deprlocationrole == IptcDeprecatedLocationRole.SHOWN and itemctr == 1:
                        self._semitptc2seret_deprec_location(locationShown)
                self._seret_metadata['XMP-iptcExt:LocationShown'] = xmplocationsshown

    def semiptc2seret_minorModelAgeDisclosure(self):
        """Transforms the semantic IPTC property Minor Model Age Disclosure to metadata serialized
            as Exif/IIM/XMP using ExifTool naming"""
        if self._minorModelAgeDisclosure is not None:
            etcode:str = minorModelAgeDisclosure_plus2et(self._minorModelAgeDisclosure)
            if etcode != '':
                self._seret_metadata['XMP-plus:MinorModelAgeDisclosure'] = etcode

    def semiptc2seret_modelAges(self):
        """Transforms the semantic IPTC property Model Age to metadata serialized
            as Exif/IIM/XMP using ExifTool naming"""
        if self._modelAges is not None:
            self._seret_metadata['XMP-iptcExt:ModelAge'] = self._modelAges

    def semiptc2seret_modelReleaseDocuments(self):
        """Transforms the semantic IPTC property Model Release Document to metadata serialized
            as Exif/IIM/XMP using ExifTool naming"""
        if self._modelReleaseDocuments is not None:
            self._seret_metadata['XMP-plus:ModelReleaseID'] = self._modelReleaseDocuments

    def semiptc2seret_modelReleaseStatus(self):
        """Transforms the semantic IPTC property Model Release Status to metadata serialized
            as Exif/IIM/XMP using ExifTool naming"""
        if self._modelReleaseStatus is not None:
            etcode:str = modelReleaseStatus_plus2et(self._modelReleaseStatus)
            if etcode != '':
                self._seret_metadata['XMP-plus:ModelReleaseStatus'] = etcode

    def semiptc2seret_personInImageNames(self):
        """Transforms the semantic IPTC property Persons Shown in Image in the Image to metadata serialized
            as Exif/IIM/XMP using ExifTool naming"""
        if self._personInImageNames is not None:
            self._seret_metadata['XMP-iptcExt:PersonInImage'] = self._personInImageNames

    def semiptc2seret_personsShown(self):
        """Transforms the semantic IPTC property Persons Shown in the Image with Details to metadata serialized
                    as Exif/IIM/XMP using ExifTool naming"""
        if self._personsShown is not None:
            if len(self._personsShown) > 0:
                xmppersonsshown = []
                for personShown in self._personsShown:
                    personShown = personShown.todict_et()
                    if personShown != {}:
                        xmppersonsshown.append(personShown)
                self._seret_metadata['XMP-iptcExt:PersonInImageWDetails'] = xmppersonsshown

    def semiptc2seret_productsShown(self):
        """Transforms the semantic IPTC property Products Shown in Image to metadata serialized as Exif/IIM/XMP
                    using ExifTool naming"""
        if self._productsShown is not None:
            if len(self._productsShown) > 0:
                xmpproducts = []
                for product in self._productsShown:
                    xmpproduct = {}
                    if product.gtin is not None:
                        xmpproduct['ProductGTIN'] = product.gtin
                    if product.name is not None:
                        xmpproduct['ProductName'] = product.name
                    if product.description is not None:
                        xmpproduct['ProductDescription'] = product.description
                    if xmpproduct != {}:
                        xmpproducts.append(xmpproduct)
                if len(xmpproducts) > 0:
                    self._seret_metadata['XMP-iptcExt:ProductInImage'] = xmpproducts

    def semiptc2seret_propertyReleaseDocuments(self):
        """Transforms the semantic IPTC property Property Release Document to metadata serialized
            as Exif/IIM/XMP using ExifTool naming"""
        if self._propertyReleaseDocuments is not None:
            self._seret_metadata['XMP-plus:PropertyReleaseID'] = self._propertyReleaseDocuments

    def semiptc2seret_propertyReleaseStatus(self):
        """Transforms the semantic IPTC property Property Release Status to metadata serialized
            as Exif/IIM/XMP using ExifTool naming"""
        if self._propertyReleaseStatus is not None:
            etcode:str = propertyReleaseStatus_plus2et(self._propertyReleaseStatus)
            if etcode != '':
                self._seret_metadata['XMP-plus:PropertyReleaseStatus'] = etcode

    def semiptc2seret_webstatementRights(self):
        """Transforms the semantic IPTC property Web Statement of Rights to metadata serialized as Exif/IIM/XMP
                    using ExifTool naming"""
        if self._webstatementRights is not None:
            self._seret_metadata['XMP-xmpRights:WebStatement'] = self._webstatementRights

    # *********************************************************************************************
    # Method for serializing a simple, not-structured semantic IPTC metadata value
    #   to Exif, IIM and XMP metadata
    #
    def _semiptc2seret_simple_multi1(self, semiptcvalue, exifid: str = None, iimid: str = None, xmpid: str = None):
        """Transforms any simple semantic IPTC PMD property to multiple serialized Exif/IIM/XMP properties"""
        if exifid is not None:
            self._seret_metadata[exifid] = semiptcvalue
        if iimid is not None:
            self._seret_metadata[iimid] = semiptcvalue
        if xmpid is not None:
            self._seret_metadata[xmpid] = semiptcvalue

    def _semiptc2seret_plusentities_xmp(self, semiptcentities, pluspropname: str = None, xmpid: str = None):
        """Transforms (PLUS) Entities to XMP"""
        if semiptcentities is not None:
            seretlist = []
            for entity in semiptcentities:
                if pluspropname is not None:
                    seretlist.append(entity.todict_plus_et(pluspropname))
                else:
                    seretlist.append(entity.todict())
            if len(seretlist) > 0:
                self._seret_metadata[xmpid] = seretlist

    def _semitptc2seret_deprec_location(self, location: Location):
        """Transforms an IPTC Location structure to the set of deprecated IPTC location properties"""
        if location.city is not None:
            self._seret_metadata['IPTC:City'] = location.city
            self._seret_metadata['XMP-photoshop:City'] = location.city
        if location.countryCode is not None:
            self._seret_metadata['IPTC:Country-PrimaryLocationCode'] = location.countryCode
            self._seret_metadata['XMP-iptcCore:CountryCode'] = location.countryCode
        if location.countryName is not None:
            self._seret_metadata['IPTC:Country-PrimaryLocationName'] = location.countryName
            self._seret_metadata['XMP-photoshop:Country'] = location.countryName
        if location.provinceState is not None:
            self._seret_metadata['IPTC:Province-State'] = location.provinceState
            self._seret_metadata['XMP-photoshop:State'] = location.provinceState
        if location.sublocation is not None:
            self._seret_metadata['IPTC:Sub-location'] = location.sublocation
            self._seret_metadata['XMP-iptcCore:Location'] = location.sublocation


    """
        ****************************************************************************************************
        Region of methods for transforming serialized metadata in Exiftool syntax to semantic IPTC metadata
    """

    def transform_seret_metadata_to_semiptc(self):
        """Transforms serialized IPTC metadata using ExifTool naming to semantic IPTC Photo Metadata

        Note: currently only the IPTC metadata of the XMP format are transformed, merging values from
        the sources Exif, IPTC IIM and XMP requires a lot of coding."""
        # This method iterates across the supported IPTC metadata properties supported by a derived class,
        #   the corresponding "serialized metadata in Exiftool syntax to semantic IPTC metadata"
        #   transformation methods are called.
        for iptcpmd_tlprop in self._supported_iptcpmd_tlprops:
            if iptcpmd_tlprop in self._seret2semiptc_registry.keys():
                self._seret2semiptc_registry[iptcpmd_tlprop]()


    def seret2semiptc_copyrightNotice(self):
        self._copyrightNotice = self._seret2semiptc_prefXIE1('XMP-dc:Rights', 'IPTC:CopyrightNotice', 'IFD0:Copyright')

    def seret2semiptc_creatorsExt(self):
        self._creatorsExt = []
        # Reading the names of Creator(s), sequence (of appending): XMP, IIM Exif
        _orphanCreatornames = []
        if 'XMP-dc:Creator' in self._seret_metadata:
            if len(self._seret_metadata['XMP-dc:Creator']) > 0:
                for foundname in self._seret_metadata['XMP-dc:Creator']:
                    if foundname not in _orphanCreatornames:  # avoid appending a name twice
                        _orphanCreatornames.append(foundname)
        if 'IPTC:By-line' in self._seret_metadata:
            if isinstance(self._seret_metadata['IPTC:By-line'], str):
                foundname = self._seret_metadata['IPTC:By-line']
                if foundname not in _orphanCreatornames:  # avoid appending a name twice
                    _orphanCreatornames.append(foundname)
            elif isinstance(self._seret_metadata['IPTC:By-line'], list):
                if len(self._seret_metadata['IPTC:By-line']) > 0:
                    for foundname in self._seret_metadata['IPTC:By-line']:
                        if foundname not in _orphanCreatornames:  # avoid appending a name twice
                            _orphanCreatornames.append(foundname)
        if 'IFD0:Artist' in self._seret_metadata:
            if self._seret_metadata['IFD0:Artist'] not in _orphanCreatornames:  # avoid appending a name twice
                _orphanCreatornames.append(self._seret_metadata['IFD0:Artist'])
        _orphanCreatornames_ref = copy.deepcopy(_orphanCreatornames)  # the _ref will stay unchanged!
        # Reading job title(s) of Creators, sequence (of appending): XMP, IIM
        _orphanJobtitles = []
        if 'XMP-photoshop:AuthorsPosition' in self._seret_metadata:  # Only 1 XMP property may exist
            _orphanJobtitles.append(self._seret_metadata['XMP-photoshop:AuthorsPosition'])
        if 'IPTC:By-lineTitle' in self._seret_metadata:  # Multiple IIM properties may exist
            if isinstance(self._seret_metadata['IPTC:By-lineTitle'], str):  # A single value
                foundjobtitle = self._seret_metadata['IPTC:By-lineTitle']
                if foundjobtitle not in _orphanJobtitles:  # A single IIM value may be the same as the XMP value
                    _orphanJobtitles.append(foundjobtitle)
            elif isinstance(self._seret_metadata['IPTC:By-lineTitle'], list):  # More than 1 value
                foundctr = 0
                for foundjobtitle in self._seret_metadata['IPTC:By-lineTitle']:
                    foundctr += 1
                    if foundctr < 2:
                        if foundjobtitle not in _orphanJobtitles:  # check the first job title for double-occurrence
                            _orphanJobtitles.append(foundjobtitle)
                    else:
                        if not self._ipmd_parse_strict:  # no adding of job titles in IPTC PMD strict mode
                            _orphanJobtitles.append(foundjobtitle)
        # Read the creator contact info, a single XMP value only
        _creatorContactInfo = CreatorContactInfo()
        if 'XMP-iptcCore:CreatorContactInfo' in self._seret_metadata:
            xmpCreatorContactinfo = self._seret_metadata['XMP-iptcCore:CreatorContactInfo']
            if 'CiAdrCity' in xmpCreatorContactinfo:
                _creatorContactInfo.city = xmpCreatorContactinfo['CiAdrCity']
            if 'CiAdrCtry' in xmpCreatorContactinfo:
                _creatorContactInfo.country = xmpCreatorContactinfo['CiAdrCtry']
            if 'CiAdrExt' in xmpCreatorContactinfo:
                _creatorContactInfo.address = xmpCreatorContactinfo['CiAdrExt']
            if 'CiAdrPcode' in xmpCreatorContactinfo:
                _creatorContactInfo.postalCode = xmpCreatorContactinfo['CiAdrPcode']
            if 'CiAdrRegion' in xmpCreatorContactinfo:
                _creatorContactInfo.region = xmpCreatorContactinfo['CiAdrRegion']
            if 'CiEmailWork' in xmpCreatorContactinfo:
                _creatorContactInfo.emailwork = xmpCreatorContactinfo['CiEmailWork']
            if 'CiTelWork' in xmpCreatorContactinfo:
                _creatorContactInfo.phonework = xmpCreatorContactinfo['CiTelWork']
            if 'CiUrlWork' in xmpCreatorContactinfo:
                _creatorContactInfo.weburlwork = xmpCreatorContactinfo['CiUrlWork']

        # Read the Image Creator entities (in XMP): add name and identifier
        #   if the Image Creator name is the first in _orphanCreatornames_ref: add first job title and contact info
        #   if the Image Creator name is found in _orphanCreatornames remove it there
        if 'XMP-plus:ImageCreator' in self._seret_metadata:
            for _seret_imageCreator in self._seret_metadata['XMP-plus:ImageCreator']:
                if _seret_imageCreator != {}:
                    _sem_creatorExt = CreatorExt()
                    if _seret_imageCreator['ImageCreatorID']:
                        _sem_creatorExt.identifiers = []
                        _sem_creatorExt.identifiers.append(_seret_imageCreator['ImageCreatorID'])
                    if _seret_imageCreator['ImageCreatorName']:
                        _creatorname = _seret_imageCreator['ImageCreatorName']
                        if len(_orphanCreatornames_ref) > 0:
                            if _creatorname == _orphanCreatornames_ref[0]:
                                # if Image Creator's name is the first orphanCreatorname: add job title and contact
                                if len(_orphanJobtitles) > 0:
                                    _sem_creatorExt.jobtitle = _orphanJobtitles.pop()
                                if _creatorContactInfo != {}:
                                    _sem_creatorExt.creatorContactInfo = _creatorContactInfo
                                    _creatorContactInfo = None  # disable this variable for further use
                        if _creatorname in _orphanCreatornames:
                            _orphanCreatornames.remove(_creatorname)
                        _sem_creatorExt.name = _creatorname
                    self._creatorsExt.append(_sem_creatorExt)
        # if any orphan creator names are left: create for each one a Creator Ext
        #   if while creating the first Creator Ext the job title and/or the contact info is still available: add them
        if (len(_orphanCreatornames)) > 0:
            setcreatorctr = 1
            for _creatorname in _orphanCreatornames:
                _sem_creatorExt = CreatorExt()
                _sem_creatorExt.name = _creatorname
                if setcreatorctr < 2:
                    if len(_orphanJobtitles) > 0:
                        _sem_creatorExt.jobtitle = _orphanJobtitles.pop()
                    if _creatorContactInfo is not None:
                        _sem_creatorExt.creatorContactInfo = _creatorContactInfo
                self._creatorsExt.append(_sem_creatorExt)
                setcreatorctr += 1
        # finally: check if any creator was appended, if not set the class attribute to None
        if len(self._creatorsExt) == 0:
            self._creatorsExt = None

    def seret2semiptc_creditLine(self):
        self._creditLine = self._seret2semiptc_prefXI1('XMP-photoshop:Credit', 'IPTC:Credit')

    def seret2semiptc_dateCreated(self):
        et_datecreated = None
        if 'ExifIFD:DateTimeOriginal' in self._seret_metadata:
            et_datecreated = self._seret_metadata['ExifIFD:DateTimeOriginal']
        if 'XMP-photoshop:DateCreated' in self._seret_metadata:
            et_datecreated = self._seret_metadata['XMP-photoshop:DateCreated']
        elif 'IPTC:DateCreated' in self._seret_metadata:
            et_datecreated = self._seret_metadata['IPTC:DateCreated']
            if 'IPTC:TimeCreated' in self._seret_metadata:
                et_datecreated += ' ' + self._seret_metadata['IPTC:TimeCreated']
        if et_datecreated is not None:
            # datecreated format: 2019:10:16 19:01:00+00:00
            daypart = et_datecreated[:10]
            daypartISO8601 = daypart.replace(':', '-')
            timepart = et_datecreated[11:]
            self._dateCreated = daypartISO8601 + 'T' + timepart

    def seret2semiptc_captionWriter(self):
        self._captionWriter = self._seret2semiptc_prefXI1('XMP-photoshop:CaptionWriter', 'IPTC:Writer-Editor')

    def seret2semiptc_description(self):
        self._description = self._seret2semiptc_prefXIE1('XMP-dc:Description', 'IPTC:Caption-Abstract',
                                                         'EXIF:ImageDescription')

    def seret2semiptc_headline(self):
        self._headline = self._seret2semiptc_prefXI1('XMP-photoshop:Headline', 'IPTC:Headline')

    def seret2semiptc_instructions(self):
        self._instructions = self._seret2semiptc_prefXI1('XMP-photoshop:Instructions', 'IPTC:SpecialInstructions')

    def seret2semiptc_intellectualGenre(self):
        self._intellectualGenre = self._seret2semiptc_prefXI1('XMP-iptcCore:IntellectualGenre',
                                                              'IPTC:ObjectAttributeReference')

    def seret2semiptc_jobid(self):
        self._jobid = self._seret2semiptc_prefXI1('XMP-photoshop:TransmissionReference',
                                                  'IPTC:OriginalTransmissionReference')

    def seret2semiptc_keywords(self):
        self._keywords = self._seret2semiptc_prefXI1('XMP-dc:Subject', 'IPTC:Keywords')

    def seret2semiptc_usageTerms(self):
        if 'XMP-xmpRights:UsageTerms' in self._seret_metadata:
            self._usageTerms = self._seret_metadata['XMP-xmpRights:UsageTerms']

    def seret2semiptc_sceneCodes(self):
        if 'XMP-iptcCore:Scene' in self._seret_metadata:
            self._sceneCodes = self._seret_metadata['XMP-iptcCore:Scene']

    def seret2semiptc_source(self):
        self._source = self._seret2semiptc_prefXI1('XMP-photoshop:Source', 'IPTC:Source')

    def seret2semiptc_subjectCodes(self):
        self._subjectCodes = self._seret2semiptc_prefXI1('XMP-iptcCore:SubjectCode', 'IPTC:SubjectReference')

    def seret2semiptc_title(self):
        self._title = self._seret2semiptc_prefXI1('XMP-dc:Title', 'IPTC:ObjectName')

    # ************************************************************
    # IPTC Extension schema properties

    def seret2semiptc_aboutCvTerms(self):
        if 'XMP-iptcExt:AboutCvTerm' in self._seret_metadata:
            if len(self._seret_metadata['XMP-iptcExt:AboutCvTerm']) > 0:
                self._aboutCvTerms = []
                for seretAboutCvTerm in self._seret_metadata['XMP-iptcExt:AboutCvTerm']:
                    if seretAboutCvTerm != {}:
                        semAboutCvTerm = CvTerm()
                        semAboutCvTerm.loadfrom_seret(seretAboutCvTerm)
                        if semAboutCvTerm is not None:
                            self._aboutCvTerms.append(semAboutCvTerm)
                if len(self._aboutCvTerms) == 0:
                    self._aboutCvTerms = None

    def seret2semiptc_additionalModelInfo(self):
        if 'XMP-iptcExt:AdditionalModelInformation' in self._seret_metadata:
            self._additionalModelInfo = self._seret_metadata['XMP-iptcExt:AdditionalModelInformation']

    def seret2semiptc_organisationInImageCodes(self):
        if 'XMP-iptcExt:OrganisationInImageCode' in self._seret_metadata:
            self._organisationInImageCodes = self._seret_metadata['XMP-iptcExt:OrganisationInImageCode']

    def seret2semiptc_organisationInImageNames(self):
        if 'XMP-iptcExt:OrganisationInImageName' in self._seret_metadata:
            self._organisationInImageNames = self._seret_metadata['XMP-iptcExt:OrganisationInImageName']

    def seret2semiptc_copyrightOwners(self):
        if 'XMP-plus:CopyrightOwner' in self._seret_metadata:
            if len(self._seret_metadata['XMP-plus:CopyrightOwner']) > 0:
                self._copyrightOwners = []
            for seretCopyrightOwner in self._seret_metadata['XMP-plus:CopyrightOwner']:
                if seretCopyrightOwner != {}:
                    semEntity = Entity()
                    semEntity.loadfrom_plus_seret(seretCopyrightOwner, 'CopyrightOwner')
                    if semEntity is not None:
                        self._copyrightOwners.append(semEntity)
            if len(self._copyrightOwners) == 0:
                self._copyrightOwners = None

    def seret2semiptc_digitalImageGuid(self):
        if 'XMP-iptcExt:DigitalImageGUID' in self._seret_metadata:
            self._digitalImageGuid = self._seret_metadata['XMP-iptcExt:DigitalImageGUID']

    def seret2semiptc_digitalSourceType(self):
        if 'XMP-iptcExt:DigitalSourceType' in self._seret_metadata:
            self._digitalSourceType = self._seret_metadata['XMP-iptcExt:DigitalSourceType']

    def seret2semiptc_embdEncRightsExprs(self):
        if 'XMP-iptcExt:EmbdEncRightsExpr' in self._seret_metadata:
            if len(self._seret_metadata['XMP-iptcExt:EmbdEncRightsExpr']) > 0:
                self._embdEncRightsExprs = []
            for seretEmbdEncRightsExpr in self._seret_metadata['XMP-iptcExt:EmbdEncRightsExpr']:
                if seretEmbdEncRightsExpr != {}:
                    semEmbdEncRightsExpr = EmbdEncRightsExpr()
                    semEmbdEncRightsExpr.loadfrom_seret(seretEmbdEncRightsExpr)
                    if semEmbdEncRightsExpr is not None:
                        self._embdEncRightsExprs.append(semEmbdEncRightsExpr)
            if len(self._embdEncRightsExprs) == 0:
                self._embdEncRightsExprs = None

    def seret2semiptc_eventName(self):
        if 'XMP-iptcExt:Event' in self._seret_metadata:
            self._eventName = self._seret_metadata['XMP-iptcExt:Event']

    def seret2semiptc_genres(self):
        if 'XMP-iptcExt:Genre' in self._seret_metadata:
            if len(self._seret_metadata['XMP-iptcExt:Genre']) > 0:
                self._genres = []
                for seretGenre in self._seret_metadata['XMP-iptcExt:Genre']:
                    if seretGenre != {}:
                        semGenre = CvTerm()
                        semGenre.loadfrom_seret(seretGenre)
                        if semGenre is not None:
                            self._genres.append(semGenre)
                if len(self._genres) == 0:
                    self._genres = None

    def seret2semiptc_imageRating(self):
        if 'XMP-xmp:Rating' in self._seret_metadata:
            rating_str: str = self._seret_metadata['XMP-xmp:Rating']
            ratingparts = rating_str.split('.')
            if len(ratingparts) > 0:
                self._imageRating = int(ratingparts[0])
            else:
                self._imageRating = 0

    def seret2semiptc_registryEntries(self):
        if 'XMP-iptcExt:RegistryID' in self._seret_metadata:
            if len(self._seret_metadata['XMP-iptcExt:RegistryID']) > 0:
                self._registryEntries = []
            for seretRegentry in self._seret_metadata['XMP-iptcExt:RegistryID']:
                if seretRegentry != {}:
                    semRegentry = RegistryEntry()
                    semRegentry.loadfrom_seret(seretRegentry)
                    if semRegentry is not None:
                        self._registryEntries.append(semRegentry)
            if len(self._registryEntries) == 0:
                self._registryEntries = None

    def seret2semiptc_suppliers(self):
        if 'XMP-plus:ImageSupplier' in self._seret_metadata:
            if len(self._seret_metadata['XMP-plus:ImageSupplier']) > 0:
                self._suppliers = []
            for seretSupplier in self._seret_metadata['XMP-plus:ImageSupplier']:
                if seretSupplier != {}:
                    semEntity = Entity()
                    semEntity.loadfrom_plus_seret(seretSupplier, 'ImageSupplier')
                    if semEntity is not None:
                        self._suppliers.append(semEntity)
            if len(self._suppliers) == 0:
                self._suppliers = None

    def seret2semiptc_imageSupplierImageId(self):
        if 'XMP-plus:ImageSupplierImageID' in self._seret_metadata:
            self._imageSupplierImageId = self._seret_metadata['XMP-plus:ImageSupplierImageID']

    def seret2semiptc_linkedEncRightsExprs(self):
        if 'XMP-iptcExt:LinkedEncRightsExpr' in self._seret_metadata:
            if len(self._seret_metadata['XMP-iptcExt:LinkedEncRightsExpr']) > 0:
                self._linkedEncRightsExprs = []
            for seretLinkedEncRightsExpr in self._seret_metadata['XMP-iptcExt:LinkedEncRightsExpr']:
                if seretLinkedEncRightsExpr != {}:
                    semLinkedEncRightsExpr = LinkedEncRightsExpr()
                    semLinkedEncRightsExpr.loadfrom_seret(seretLinkedEncRightsExpr)
                    if semLinkedEncRightsExpr is not None:
                        self._linkedEncRightsExprs.append(semLinkedEncRightsExpr)
            if len(self._linkedEncRightsExprs) == 0:
                self._linkedEncRightsExprs = None

    def seret2semiptc_licensors(self):
        if 'XMP-plus:Licensor' in self._seret_metadata:
            if len(self._seret_metadata['XMP-plus:Licensor']) > 0:
                self._licensors = []
            for seretLicensor in self._seret_metadata['XMP-plus:Licensor']:
                if seretLicensor != {}:
                    semLicensor = Licensor()
                    semLicensor.loadfrom_seret(seretLicensor)
                    if semLicensor is not None:
                        self._licensors.append(semLicensor)
            if len(self._licensors) == 0:
                self._licensors = None

    def seret2semiptc_locationCreated(self):
        if 'XMP-iptcExt:LocationCreated' in self._seret_metadata:
            locationCreated = Location()
            locationCreated.loadfrom_seret(self._seret_metadata['XMP-iptcExt:LocationCreated'])
            self._locationCreated = locationCreated

    def seret2semiptc_locationsShown(self):
        if 'XMP-iptcExt:LocationShown' in self._seret_metadata:
            if len(self._seret_metadata['XMP-iptcExt:LocationShown']) > 0:
                self._locationsShown = []
            for xmplocation in self._seret_metadata['XMP-iptcExt:LocationShown']:
                locationShown = Location()
                locationShown.loadfrom_seret(xmplocation)
                self._locationsShown.append(locationShown)

    def seret2semiptc_minorModelAgeDisclosure(self):
        if 'XMP-plus:MinorModelAgeDisclosure' in self._seret_metadata:
            etcode: str = self._seret_metadata['XMP-plus:MinorModelAgeDisclosure']
            plusuri:str = minorModelAgeDisclosure_et2plus(etcode)
            if plusuri != '':
                self._minorModelAgeDisclosure = plusuri

    def seret2semiptc_modelAges(self):
        if 'XMP-iptcExt:ModelAge' in self._seret_metadata:
            self._modelAges = self._seret_metadata['XMP-iptcExt:ModelAge']

    def seret2semiptc_modelReleaseDocuments(self):
        if 'XMP-plus:ModelReleaseID' in self._seret_metadata:
            self._modelReleaseDocuments = self._seret_metadata['XMP-plus:ModelReleaseID']

    def seret2semiptc_modelReleaseStatus(self):
        if 'XMP-plus:ModelReleaseStatus' in self._seret_metadata:
            etcode: str = self._seret_metadata['XMP-plus:ModelReleaseStatus']
            plusuri: str = modelReleaseStatus_et2plus(etcode)
            if plusuri != '':
                self._modelReleaseStatus = plusuri

    def seret2semiptc_personInImageNames(self):
        if 'XMP-iptcExt:PersonInImage' in self._seret_metadata:
            self._personInImageNames = self._seret_metadata['XMP-iptcExt:PersonInImage']

    def seret2semiptc_personsShown(self):
        if 'XMP-iptcExt:PersonInImageWDetails' in self._seret_metadata:
            if len(self._seret_metadata['XMP-iptcExt:PersonInImageWDetails']) > 0:
                self._personsShown = []
            for seretPerson in self._seret_metadata['XMP-iptcExt:PersonInImageWDetails']:
                if seretPerson != {}:
                    _propsetcount = 0
                    semPerson = PersonWDetails()
                    if 'PersonId' in seretPerson:
                        _propsetcount += 1
                        semPerson.identifiers = seretPerson['PersonId']
                    if 'PersonName' in seretPerson:
                        _propsetcount += 1
                        semPerson.name = seretPerson['PersonName']
                    if 'PersonDescription' in seretPerson:
                        _propsetcount += 1
                        semPerson.description = seretPerson['PersonDescription']
                    if 'PersonCharacteristic' in seretPerson:
                        semPerson.characteristics = []
                        for seretAboutCvTerm in seretPerson['PersonCharacteristic']:
                            if seretAboutCvTerm != {}:
                                semAboutCvTerm = CvTerm()
                                semAboutCvTerm.loadfrom_seret(seretAboutCvTerm)
                                if semAboutCvTerm is not None:
                                    semPerson.characteristics.append(semAboutCvTerm)
                                    _propsetcount += 1
                    if _propsetcount > 0:
                        self._personsShown.append(semPerson)
            if len(self._personsShown) == 0:
                self._personsShown = None

    def seret2semiptc_productsShown(self):
        if 'XMP-iptcExt:ProductInImage' in self._seret_metadata:
            if len(self._seret_metadata['XMP-iptcExt:ProductInImage']) > 0:
                self._productsShown = []
            for seretProduct in self._seret_metadata['XMP-iptcExt:ProductInImage']:
                if seretProduct != {}:
                    semProduct = ProductWGtin()
                    semProduct.loadfrom_seret(seretProduct)
                    if semProduct is not None:
                        self._productsShown.append(semProduct)
            if len(self._productsShown) == 0:
                self._productsShown = None

    def seret2semiptc_propertyReleaseDocuments(self):
        if 'XMP-plus:PropertyReleaseID' in self._seret_metadata:
            self._propertyReleaseDocuments = self._seret_metadata['XMP-plus:PropertyReleaseID']

    def seret2semiptc_propertyReleaseStatus(self):
        if 'XMP-plus:PropertyReleaseStatus' in self._seret_metadata:
            etcode: str = self._seret_metadata['XMP-plus:PropertyReleaseStatus']
            plusuri: str = propertyReleaseStatus_et2plus(etcode)
            if plusuri != '':
                self._propertyReleaseStatus = plusuri

    def seret2semiptc_webstatementRights(self):
        if 'XMP-xmpRights:WebStatement' in self._seret_metadata:
            self._webstatementRights = self._seret_metadata['XMP-xmpRights:WebStatement']

    # *********************************************************************************************
    # Methods for parsing and reading simple semantic IPTC metadata values
    #   from the serialized Exif, IIM and XMP metadata
    #
    def _seret2semiptc_prefEXI1(self, exifid: str = None, xmpid: str = None, iimid: str = None) -> any:
        """Gets semantic IPTC metadata property from a set of serialized metadata, preference: Exif, XMP, IIM"""
        if exifid is None or xmpid is None or iimid is None:
            return None
        semiptc_value = None
        if exifid in self._seret_metadata:
            semiptc_value = self._seret_metadata[exifid]
            return semiptc_value
        if xmpid in self._seret_metadata:
            semiptc_value = self._seret_metadata[xmpid]
        elif iimid in self._seret_metadata:
            semiptc_value = self._seret_metadata[iimid]
        return semiptc_value

    def _seret2semiptc_prefXIE1(self, xmpid: str = None, iimid: str = None, exifid: str = None) -> any:
        """Gets semantic IPTC metadata property from a set of serialized metadata, preference: XMP, IIM, Exif"""
        if exifid is None or xmpid is None or iimid is None:
            return None
        semiptc_value = None
        if exifid in self._seret_metadata:
            semiptc_value = self._seret_metadata[exifid]
        if xmpid in self._seret_metadata:
            semiptc_value = self._seret_metadata[xmpid]
        elif iimid in self._seret_metadata:
            semiptc_value = self._seret_metadata[iimid]
        return semiptc_value

    def _seret2semiptc_prefXI1(self, xmpid: str = None, iimid: str = None) -> any:
        """Gets semantic IPTC metadata property from a set of serialized metadata, preference: XMP, IIM"""
        if xmpid is None or iimid is None:
            return None
        semiptc_value = None
        if xmpid in self._seret_metadata:
            semiptc_value = self._seret_metadata[xmpid]
        elif iimid in self._seret_metadata:
            semiptc_value = self._seret_metadata[iimid]
        return semiptc_value

    def _seret_propoccur_singleser(self, propid) -> PropertyOccurrence:
        """Tests the occurrence(s) if a single serialized metadata property"""
        if propid in self._seret_metadata:
            if isinstance(self._seret_metadata[propid], list):
                return PropertyOccurrence.MANY
            else:
                return PropertyOccurrence.ONE
        else:
            return PropertyOccurrence.NONE

    """
    def _seret_propoccur_XI1(self, xmpid: str = None, iimid: str = None) -> PropertyOccurrence:
        xmpoccurrence = self._seret_propoccur_singleser(xmpid)
        iimoccurrence = self._seret_propoccur_singleser(iimid)
        if xmpoccurrence == PropertyOccurrence.NONE and iimoccurrence == PropertyOccurrence.NONE:
            return PropertyOccurrence.NONE
        elif xmpoccurrence == PropertyOccurrence.ONE:
            return PropertyOccurrence.ONE
        elif iimoccurrence == PropertyOccurrence.ONE:
            return PropertyOccurrence.ONE
        elif xmpoccurrence == PropertyOccurrence.MANY:
            return PropertyOccurrence.MANY
        elif iimoccurrence == PropertyOccurrence.MANY:
            return PropertyOccurrence.MANY

    def _seret_propoccur_XIE1(self, xmpid: str = None, iimid: str = None, exifid: str = None) -> PropertyOccurrence:
        xmpoccurrence = self._seret_propoccur_singleser(xmpid)
        iimoccurrence = self._seret_propoccur_singleser(iimid)
        exifoccurrence = self._seret_propoccur_singleser(exifid)
        if xmpoccurrence == PropertyOccurrence.NONE and iimoccurrence == PropertyOccurrence.NONE \
                and exifoccurrence == PropertyOccurrence.NONE:
            return PropertyOccurrence.NONE
        elif xmpoccurrence == PropertyOccurrence.ONE:
            return PropertyOccurrence.ONE
        elif iimoccurrence == PropertyOccurrence.ONE:
            return PropertyOccurrence.ONE
        elif exifoccurrence == PropertyOccurrence.ONE:
            return PropertyOccurrence.ONE
        elif xmpoccurrence == PropertyOccurrence.MANY:
            return PropertyOccurrence.MANY
        elif iimoccurrence == PropertyOccurrence.MANY:
            return PropertyOccurrence.MANY
        elif exifoccurrence == PropertyOccurrence.MANY:
            return PropertyOccurrence.MANY
    """

    """
        ****************************************************************************************************
        Region of other internal methods 
    """

    def _generate_semiptc_metadata(self):
        """Generate _semiptc_metadata object from enabled IPTC PMD properties of this class"""
        self._semiptc_metadata = {}
        for semiptc_propname in self.semiptc_propnames:
            if getattr(self, semiptc_propname) is not None:
                semiptc_prop = getattr(self, semiptc_propname)
                if isinstance(semiptc_prop, str) or isinstance(semiptc_prop, int):
                    self._semiptc_metadata[semiptc_propname] = semiptc_prop
                elif isinstance(semiptc_prop, list):
                    list1 = []
                    for list1item in semiptc_prop:
                        if isinstance(list1item, str) or isinstance(list1item, int):
                            list1.append(list1item)
                        elif isinstance(list1item, list):
                            list2 = []
                            for list2item in semiptc_prop:
                                if isinstance(list2item, str) or isinstance(list2item, int):
                                    list1.append(list2item)
                                else:
                                    d = list2item.todict()
                                    list1.append(d)
                                list2.append(list2item)
                            list1.append(list2)
                        else:
                            d = list1item.todict()
                            list1.append(d)
                    self._semiptc_metadata[semiptc_propname] = list1
