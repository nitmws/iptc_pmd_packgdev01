import os
import json
from pathlib import Path
from dataclasses import dataclass
from typing import List, Set, Dict, Tuple, Optional, Type
from enum import Enum
from .tools import *

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

@dataclass
class EmbdEncRightsExpr(IptcStructure):
  rightsExprLangId: Optional[str] = None
  rightsExprEncType: Optional[str] = None
  encRightsExpr: Optional[str] = None

@dataclass
class Entity(IptcStructure):
  identifiers: Optional[List[str]] = None
  name: Optional[str] = None

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

@dataclass
class Licensor(IptcStructure):
  licensorID: Optional[str] = None
  licensorName: Optional[str] = None
  licensorURL: Optional[str] = None

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

@dataclass
class PersonWDetails(IptcStructure):
  characteristics: Optional[List[Type[CvTerm]]] = None
  description: Optional[str] = None
  identifiers: Optional[List[str]] = None
  name: Optional[str] = None

@dataclass
class ProductWGtin(IptcStructure):
  description: Optional[str] = None
  gtin: Optional[str] = None
  name: Optional[str] = None

@dataclass
class RegistryEntry(IptcStructure):
  assetIdentifier: Optional[str] = None
  registryIdentifier: Optional[str] = None
  role: Optional[str] = None

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
    _imageCreators: Optional[List[Type[Entity]]] = None
    _imageRating: Optional[int] = None
    _imageRegion: Optional[List[Type[ImageRegion]]] = None
    _registryEntries: Optional[List[Type[RegistryEntry]]] = None
    _suppliers: Optional[List[Type[Entity]]] = None
    _imageSupplierImageId: Optional[str] = None
    _licensors: Optional[List[Type[Licensor]]] = None
    _linkedEncRightsExprs: Optional[List[Type[LinkedEncRightsExpr]]] = None
    _locationCreated: Optional[Type[Location]] = None
    _locationsShown: Optional[List[Type[Location]]] = None
    _maxAvailHeight: Optional[int] = None
    _maxAvailWidth: Optional[int] = None
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
                         '_eventName', '_genres', '_imageCreators', '_imageRating', '_imageRegion', '_registryEntries',
                         '_suppliers', '_imageSupplierImageId', '_licensors', '_linkedEncRightsExprs',
                         '_locationCreated', '_locationsShown', '_maxAvailHeight', '_maxAvailWidth',
                         '_minorModelAgeDisclosure', '_modelAges', '_modelReleaseDocuments', '_modelReleaseStatus',
                         '_organisationInImageNames', '_personInImageNames', '_personsShown', '_productsShown',
                         '_propertyReleaseDocuments', '_propertyReleaseStatus', '_webstatementRights')

    def __init__(self):
        self._currentdir: str = ''
        self._supported_iptcpmd_tlprops = ()  # Tuple of semantic IPTC metadata property names supported by a (sub)class
        self._deprlocationrole: IptcDeprecatedLocationRole = IptcDeprecatedLocationRole.SHOWN
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


    """
        *******************************************************************
        Exporting and importing metadata to JSON files
    """

    def export_semiptc_as_jsonfile(self, json_fp):
        """Exports the semantic IPTC Photo Metadata of this class to a JSON file"""
        self._semiptc_metadata = {}
        for semiptc_propname in self.semiptc_propnames:
            if getattr(self, semiptc_propname) is not None:
                semiptc_prop = getattr(self, semiptc_propname)
                if isinstance(semiptc_prop, str) or isinstance(semiptc_prop, int):
                    self._semiptc_metadata[semiptc_propname] = semiptc_prop
                elif isinstance(semiptc_prop, list):
                    list1 = []
                    for listitem in semiptc_prop:
                        if isinstance(listitem, str) or isinstance(listitem, int):
                            list1.append(listitem)
                        else:
                            d = listitem.todict()
                            list1.append(d)
                    self._semiptc_metadata[semiptc_propname] = list1
        # return
        ## sorry, the JSON serialization does not work currently
        filename = Path(json_fp)
        filename = filename.with_suffix('.json')
        with filename.open(mode='w') as _f:
            _f.write(json.dumps(self._semiptc_metadata, indent=2,
                                ensure_ascii=False, sort_keys=True))

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
        """Transforms serialized semantic IPTC Photo Metadata ot IPTC metadata using ExifTool naming"""
        # This method iterates across the supported IPTC metadata properties supported by a derived class,
        #   the corresponding "semantic IPTC metadata to serialized metadata in Exiftool syntax"
        #   transformation methods are called.
        for iptcpmd_tlprop in self._supported_iptcpmd_tlprops:
            if iptcpmd_tlprop in self._semiptc2seret_registry.keys():
                self._semiptc2seret_registry[iptcpmd_tlprop]()

    def semiptc2seret_copyrightNotice(self):
        if self._copyrightNotice is not None:
            self._seret_metadata['IFD0:Copyright'] = self._copyrightNotice
            self._seret_metadata['IPTC:CopyrightNotice'] = self._copyrightNotice
            self._seret_metadata['XMP-dc:Rights'] = self._copyrightNotice

    def semiptc2seret_creatorsExt(self):
        if self._creatorsExt is not None:
            if len(self._creatorsExt) > 0:
                creatorname = self._creatorsExt[0].name
                if creatorname != '':
                    self._seret_metadata['IFD0:Artist'] = creatorname
                    self._seret_metadata['IPTC:By-line'] = creatorname
                    xmpcreator = [creatorname]
                    self._seret_metadata['XMP-dc:Creator'] = xmpcreator
                xmpimgcreators = []
                for creatorExt in self._creatorsExt:
                    xmpimgcreator = {}
                    if creatorExt.identifiers is not None:
                        xmpimgcreator['ImageCreatorID'] = creatorExt.identifiers[0]
                    if creatorExt.name is not None:
                        xmpimgcreator['ImageCreatorName'] = creatorExt.name
                    xmpimgcreators.append(xmpimgcreator)
                self._seret_metadata['XMP-plus:ImageCreator'] = xmpimgcreators

    def semiptc2seret_creditLine(self):
        if self._creditLine is not None:
            self._seret_metadata['IPTC:Credit'] = self._creditLine
            self._seret_metadata['XMP-photoshop:Credit'] = self._creditLine

    def semiptc2seret_description(self):
        if self._description is not None:
            self._seret_metadata['EXIF:ImageDescription'] = self._description
            self._seret_metadata['IPTC:Caption-Abstract'] = self._description
            self._seret_metadata['XMP-dc:Description'] = self._description

    def semiptc2seret_headline(self):
        if self._headline is not None:
            self._seret_metadata['IPTC:Headline'] = self._headline
            self._seret_metadata['XMP-photoshop:Headline'] = self._headline

    def semiptc2seret_keywords(self):
        if self._keywords is not None:
            for keyword in self._keywords:
                if keyword != '':
                    self._seret_metadata['IPTC:Keywords'] = keyword
                    self._seret_metadata['XMP-dc:Subject'] = keyword

    def semiptc2seret_title(self):
        if self._title is not None:
            self._seret_metadata['IPTC:ObjectName'] = self._title
            self._seret_metadata['XMP-dc:Title'] = self._title

    def semiptc2seret_locationsShown(self):
        if self._locationsShown is not None:
            if len(self._locationsShown) > 0:
                itemctr = 0
                xmplocationsshown = []
                for locationShown in self._locationsShown:
                    itemctr += 1
                    xmplocationshown = {}
                    xmplocationshown['LocationId'] = locationShown.identifiers
                    xmplocationshown['City'] = locationShown.city
                    xmplocationshown['CountryCode'] = locationShown.countryCode
                    xmplocationshown['CountryName'] = locationShown.countryName
                    xmplocationshown['ProvinceState'] = locationShown.provinceState
                    xmplocationshown['Sublocation'] = locationShown.sublocation
                    xmplocationshown['WorldRegion'] = locationShown.worldRegion
                    xmplocationsshown.append(xmplocationshown)
                    if self._deprlocationrole == IptcDeprecatedLocationRole.SHOWN and itemctr == 1:
                        self._seret_metadata['IPTC:City'] = locationShown.city
                        self._seret_metadata['XMP-photoshop:City'] = locationShown.city
                        self._seret_metadata['IPTC:Country-PrimaryLocationCode'] = locationShown.countryCode
                        self._seret_metadata['XMP-iptcCore:CountryCode'] = locationShown.countryCode
                        self._seret_metadata['IPTC:Country-PrimaryLocationName'] = locationShown.countryName
                        self._seret_metadata['XMP-photoshop:Country'] = locationShown.countryName
                        self._seret_metadata['IPTC:Province-State'] = locationShown.provinceState
                        self._seret_metadata['XMP-photoshop:State'] = locationShown.provinceState
                        self._seret_metadata['IPTC:Sub-location'] = locationShown.sublocation
                        self._seret_metadata['XMP-iptcCore:Location'] = locationShown.sublocation
                self._seret_metadata['XMP-iptcExt:LocationShown'] = xmplocationsshown

    def semiptc2seret_licensors(self):
        if self._licensors is not None:
            if len(self._licensors) > 0:
                xmplicensors = []
                licctr = 1  # PLUS: max 3 Licensor
                for licensor in self._licensors:
                    if licctr > 3:
                        break
                    else:
                        licctr += 1
                    xmplicensor = {}
                    if licensor.licensorID is not None:
                        xmplicensor['LicensorID'] = licensor.licensorID
                    if licensor.licensorName is not None:
                        xmplicensor['LicensorName'] = licensor.licensorName
                    if licensor.licensorURL is not None:
                        xmplicensor['LicensorURL'] = licensor.licensorURL
                    xmplicensors.append(xmplicensor)
                self._seret_metadata['XMP-plus:Licensor'] = xmplicensors

    def semiptc2seret_webstatementRights(self):
        if self._webstatementRights is not None:
            self._seret_metadata['XMP-xmpRights:WebStatement'] = self._webstatementRights

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
        if 'XMP-dc:Rights' in self._seret_metadata:
            self._copyrightNotice = self._seret_metadata['XMP-dc:Rights']

    def seret2semiptc_creatorsExt(self):
        self._creatorsExt = []
        _orphanCreatornames = []
        if 'XMP-dc:Creator' in self._seret_metadata:
            if len(self._seret_metadata['XMP-dc:Creator']) > 0:
                for _creatorname in self._seret_metadata['XMP-dc:Creator']:
                    _orphanCreatornames.append(_creatorname)
        if 'XMP-plus:ImageCreator' in self._seret_metadata:
            for _seret_imageCreator in self._seret_metadata['XMP-plus:ImageCreator']:
                if _seret_imageCreator != {}:
                    _sem_creatorExt = CreatorExt()
                    if _seret_imageCreator['ImageCreatorID']:
                        _sem_creatorExt.identifiers = []
                        _sem_creatorExt.identifiers.append(_seret_imageCreator['ImageCreatorID'])
                    if _seret_imageCreator['ImageCreatorName']:
                        _creatorname = _seret_imageCreator['ImageCreatorName']
                        if _creatorname in _orphanCreatornames:
                            _orphanCreatornames.remove(_creatorname)
                        _sem_creatorExt.name = _creatorname
                    self._creatorsExt.append(_sem_creatorExt)
        if (len(_orphanCreatornames)) > 0:
            for _creatorname in _orphanCreatornames:
                _sem_creatorExt = CreatorExt()
                _sem_creatorExt.name = _creatorname
                self._creatorsExt.append(_sem_creatorExt)

    def seret2semiptc_creditLine(self):
        if 'XMP-photoshop:Credit' in self._seret_metadata:
            self._creditLine = self._seret_metadata['XMP-photoshop:Credit']

    def seret2semiptc_description(self):
        if 'EXIF:ImageDescription' in self._seret_metadata:
            self._creditLine = self._seret_metadata['EXIF:ImageDescription']
        if 'XMP-dc:Description' in self._seret_metadata:
            self._creditLine = self._seret_metadata['XMP-dc:Description']
        elif 'IPTC:Caption-Abstract' in self._seret_metadata:
            self._creditLine = self._seret_metadata['IPTC:Caption-Abstract']

    def seret2semiptc_headline(self):
        if 'XMP-photoshop:Headline' in self._seret_metadata:
            self._headline = self._seret_metadata['XMP-photoshop:Headline']
        elif 'IPTC:Headline' in self._seret_metadata:
            self._headline = self._seret_metadata['IPTC:Headline']

    def seret2semiptc_keywords(self):
        if 'XMP-dc:Subject' in self._seret_metadata:
            self._keywords = self._seret_metadata['XMP-dc:Subject']
        elif 'IPTC:Keywords' in self._seret_metadata:
            self._keywords = self._seret_metadata['IPTC:Keywords']

    def seret2semiptc_title(self):
        if 'XMP-dc:Title' in self._seret_metadata:
            self._title = self._seret_metadata['XMP-dc:Title']
        elif 'IPTC:ObjectName' in self._seret_metadata:
            self._title = self._seret_metadata['IPTC:ObjectName']

    def seret2semiptc_licensors(self):
        if 'XMP-plus:Licensor' in self._seret_metadata:
            if len(self._seret_metadata['XMP-plus:Licensor']) > 0:
                self._licensors = []
            for _xmplicensor in self._seret_metadata['XMP-plus:Licensor']:
                if _xmplicensor != {}:
                    _propsetcount = 0
                    _semlicensor = Licensor()
                    if 'LicensorID' in _xmplicensor:
                        _propsetcount += 1
                        _semlicensor.licensorID = _xmplicensor['LicensorID']
                    if 'LicensorName' in _xmplicensor:
                        _propsetcount += 1
                        _semlicensor.licensorName = _xmplicensor['LicensorName']
                    if 'LicensorURL' in _xmplicensor:
                        _propsetcount += 1
                        _semlicensor.licensorURL = _xmplicensor['LicensorURL']
                    if _propsetcount > 0:
                        self._licensors.append(_semlicensor)
            if len(self._licensors) == 0:
                self._licensors = None

    def seret2semiptc_webstatementRights(self):
        if 'XMP-xmpRights:WebStatement' in self._seret_metadata:
            self._webstatementRights = self._seret_metadata['XMP-xmpRights:WebStatement']
