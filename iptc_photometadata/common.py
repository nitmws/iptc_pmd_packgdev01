import os
import json
import copy
from pathlib import Path
from dataclasses import dataclass
from typing import List, Set, Dict, Tuple, Optional, Type
from enum import Enum

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
        """Transforms all semantic IPTC Photo Metadata to metadata serialized as Exif/IIM/XMP using ExifTool naming"""
        # This method iterates across the supported IPTC metadata properties supported by a derived class,
        #   the corresponding "semantic IPTC metadata to serialized metadata in Exiftool syntax"
        #   transformation methods are called.
        for iptcpmd_tlprop in self._supported_iptcpmd_tlprops:
            if iptcpmd_tlprop in self._semiptc2seret_registry.keys():
                self._semiptc2seret_registry[iptcpmd_tlprop]()

    def semiptc2seret_copyrightNotice(self):
        if self._copyrightNotice is not None:
            self._semiptc2seret_simple_multi1(self._copyrightNotice, 'IFD0:Copyright', 'IPTC:CopyrightNotice',
                                            'XMP-dc:Rights')

    def semiptc2seret_creatorsExt(self):
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
        if self._creditLine is not None:
            self._semiptc2seret_simple_multi1(self._creditLine, None, 'IPTC:Credit', 'XMP-photoshop:Credit')

    def semiptc2seret_dateCreated(self):
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
        if self._captionWriter is not None:
            self._semiptc2seret_simple_multi1(self._captionWriter, None, 'IPTC:Writer-Editor',
                                              'XMP-photoshop:CaptionWriter')

    def semiptc2seret_description(self):
        if self._description is not None:
            self._semiptc2seret_simple_multi1(self._description, 'EXIF:ImageDescription', 'IPTC:Caption-Abstract',
                                            'XMP-dc:Description')

    def semiptc2seret_headline(self):
        if self._headline is not None:
            self._semiptc2seret_simple_multi1(self._headline, None, 'IPTC:Headline', 'XMP-photoshop:Headline')

    def semiptc2seret_instructions(self):
        if self._instructions is not None:
            self._semiptc2seret_simple_multi1(self._instructions, None, 'IPTC:SpecialInstructions',
                                              'XMP-photoshop:Instructions')

    def semiptc2seret_intellectualGenre(self):
        if self._intellectualGenre is not None:
            self._semiptc2seret_simple_multi1(self._intellectualGenre, None, 'IPTC:ObjectAttributeReference',
                                              'XMP-iptcCore:IntellectualGenre')

    def semiptc2seret_jobid(self):
        if self._jobid is not None:
            self._semiptc2seret_simple_multi1(self._jobid, None, 'IPTC:OriginalTransmissionReference',
                                              'XMP-photoshop:TransmissionReference')

    def semiptc2seret_keywords(self):
        if self._keywords is not None:
            self._semiptc2seret_simple_multi1(self._keywords, None, 'IPTC:Keywords', 'XMP-dc:Subject')

    def semiptc2seret_usageTerms(self):
        if self._usageTerms is not None:
            self._semiptc2seret_simple_multi1(self._usageTerms, None, None, 'XMP-xmpRights:UsageTerms')

    def semiptc2seret_sceneCodes(self):
        if self._sceneCodes is not None:
            self._semiptc2seret_simple_multi1(self._sceneCodes, None, None, 'XMP-iptcCore:Scene')

    def semiptc2seret_source(self):
        if self._source is not None:
            self._semiptc2seret_simple_multi1(self._source, None, 'IPTC:Source', 'XMP-photoshop:Source')

    def semiptc2seret_subjectCodes(self):
        if self._subjectCodes is not None:
            self._semiptc2seret_simple_multi1(self._subjectCodes, None, 'IPTC:SubjectReference',
                                              'XMP-iptcCore:SubjectCode')

    def semiptc2seret_title(self):
        if self._title is not None:
            self._semiptc2seret_simple_multi1(self._title, 'IPTC:ObjectName', 'XMP-dc:Title')

    def semiptc2seret_licensors(self):
        if self._licensors is not None:
            if len(self._licensors) > 0:
                xmplicensors = []
                licctr = 0  # PLUS: max 3 Licensor
                for licensor in self._licensors:
                    licctr += 1
                    if licctr > 3:  # PLUS spec: max 3 Licensor entities
                        break
                    xmplicensor = {}
                    if licensor.licensorID is not None:
                        xmplicensor['LicensorID'] = licensor.licensorID
                    if licensor.licensorName is not None:
                        xmplicensor['LicensorName'] = licensor.licensorName
                    if licensor.licensorURL is not None:
                        xmplicensor['LicensorURL'] = licensor.licensorURL
                    xmplicensors.append(xmplicensor)
                self._seret_metadata['XMP-plus:Licensor'] = xmplicensors

    def semiptc2seret_locationCreated(self):
        if self._locationCreated is not None:
            xmplocationcreated = {}
            if self._locationCreated.identifiers is not None:
                xmplocationcreated['LocationId'] = self._locationCreated.identifiers
            if self._locationCreated.city is not None:
                xmplocationcreated['City'] = self._locationCreated.city
            if self._locationCreated.countryCode is not None:
                xmplocationcreated['CountryCode'] = self._locationCreated.countryCode
            if self._locationCreated.countryName is not None:
                xmplocationcreated['CountryName'] = self._locationCreated.countryName
            if self._locationCreated.provinceState is not None:
                xmplocationcreated['ProvinceState'] = self._locationCreated.provinceState
            if self._locationCreated.sublocation is not None:
                xmplocationcreated['Sublocation'] = self._locationCreated.sublocation
            if self._locationCreated.worldRegion is not None:
                xmplocationcreated['WorldRegion'] = self._locationCreated.worldRegion
            if xmplocationcreated != {}:
                self._seret_metadata['XMP-iptcExt:LocationCreated'] = xmplocationcreated
            if self._deprlocationrole == IptcDeprecatedLocationRole.CREATED:
                if self._locationCreated.city is not None:
                    self._seret_metadata['IPTC:City'] = self._locationCreated.city
                    self._seret_metadata['XMP-photoshop:City'] = self._locationCreated.city
                if self._locationCreated.countryCode is not None:
                    self._seret_metadata['IPTC:Country-PrimaryLocationCode'] = self._locationCreated.countryCode
                    self._seret_metadata['XMP-iptcCore:CountryCode'] = self._locationCreated.countryCode
                if self._locationCreated.countryName is not None:
                    self._seret_metadata['IPTC:Country-PrimaryLocationName'] = self._locationCreated.countryName
                    self._seret_metadata['XMP-photoshop:Country'] = self._locationCreated.countryName
                if self._locationCreated.provinceState is not None:
                    self._seret_metadata['IPTC:Province-State'] = self._locationCreated.provinceState
                    self._seret_metadata['XMP-photoshop:State'] = self._locationCreated.provinceState
                if self._locationCreated.sublocation is not None:
                    self._seret_metadata['IPTC:Sub-location'] = self._locationCreated.sublocation
                    self._seret_metadata['XMP-iptcCore:Location'] = self._locationCreated.sublocation

    def semiptc2seret_locationsShown(self):
        if self._locationsShown is not None:
            if len(self._locationsShown) > 0:
                itemctr = 0
                xmplocationsshown = []
                for locationShown in self._locationsShown:
                    itemctr += 1
                    xmplocationshown = {}
                    if locationShown.identifiers is not None:
                        xmplocationshown['LocationId'] = locationShown.identifiers
                    if locationShown.city is not None:
                        xmplocationshown['City'] = locationShown.city
                    if locationShown.countryCode is not None:
                        xmplocationshown['CountryCode'] = locationShown.countryCode
                    if locationShown.countryName is not None:
                        xmplocationshown['CountryName'] = locationShown.countryName
                    if locationShown.provinceState is not None:
                        xmplocationshown['ProvinceState'] = locationShown.provinceState
                    if locationShown.sublocation is not None:
                        xmplocationshown['Sublocation'] = locationShown.sublocation
                    if locationShown.worldRegion is not None:
                        xmplocationshown['WorldRegion'] = locationShown.worldRegion
                    xmplocationsshown.append(xmplocationshown)
                    if self._deprlocationrole == IptcDeprecatedLocationRole.SHOWN and itemctr == 1:
                        if locationShown.city is not None:
                            self._seret_metadata['IPTC:City'] = locationShown.city
                            self._seret_metadata['XMP-photoshop:City'] = locationShown.city
                        if locationShown.countryCode is not None:
                            self._seret_metadata['IPTC:Country-PrimaryLocationCode'] = locationShown.countryCode
                            self._seret_metadata['XMP-iptcCore:CountryCode'] = locationShown.countryCode
                        if locationShown.countryName is not None:
                            self._seret_metadata['IPTC:Country-PrimaryLocationName'] = locationShown.countryName
                            self._seret_metadata['XMP-photoshop:Country'] = locationShown.countryName
                        if locationShown.provinceState is not None:
                            self._seret_metadata['IPTC:Province-State'] = locationShown.provinceState
                            self._seret_metadata['XMP-photoshop:State'] = locationShown.provinceState
                        if locationShown.sublocation is not None:
                            self._seret_metadata['IPTC:Sub-location'] = locationShown.sublocation
                            self._seret_metadata['XMP-iptcCore:Location'] = locationShown.sublocation
                self._seret_metadata['XMP-iptcExt:LocationShown'] = xmplocationsshown

    def semiptc2seret_webstatementRights(self):
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

    def seret2semiptc_locationCreated(self):
        if 'XMP-iptcExt:LocationCreated' in self._seret_metadata:
            self._locationCreated = Location()
            xmplocation = self._seret_metadata['XMP-iptcExt:LocationCreated']
            if 'LocationId' in xmplocation:
                self._locationCreated.identifiers = xmplocation['LocationId']
            if 'City' in xmplocation:
                self._locationCreated.city = xmplocation['City']
            if 'CountryCode' in xmplocation:
                self._locationCreated.countryCode = xmplocation['CountryCode']
            if 'CountryName' in xmplocation:
                self._locationCreated.countryName = xmplocation['CountryName']
            if 'ProvinceState' in xmplocation:
                self._locationCreated.provinceState = xmplocation['ProvinceState']
            if 'Sublocation' in xmplocation:
                self._locationCreated.sublocation = xmplocation['Sublocation']
            if 'WorldRegion' in xmplocation:
                self._locationCreated.worldRegion = xmplocation['WorldRegion']

    def seret2semiptc_locationsShown(self):
        if 'XMP-iptcExt:LocationShown' in self._seret_metadata:
            if len(self._seret_metadata['XMP-iptcExt:LocationShown']) > 0:
                self._locationsShown = []
            for xmplocation in self._seret_metadata['XMP-iptcExt:LocationShown']:
                _location = Location()
                if 'LocationId' in xmplocation:
                    _location.identifiers = xmplocation['LocationId']
                if 'City' in xmplocation:
                    _location.city = xmplocation['City']
                if 'CountryCode' in xmplocation:
                    _location.countryCode = xmplocation['CountryCode']
                if 'CountryName' in xmplocation:
                    _location.countryName = xmplocation['CountryName']
                if 'ProvinceState' in xmplocation:
                    _location.provinceState = xmplocation['ProvinceState']
                if 'Sublocation' in xmplocation:
                    _location.sublocation = xmplocation['Sublocation']
                if 'WorldRegion' in xmplocation:
                    _location.worldRegion = xmplocation['WorldRegion']
                self._locationsShown.append(_location)


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


