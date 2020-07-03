from pathlib import Path
from dataclasses import dataclass
import typing
from typing import List, Set, Dict, Tuple, Optional, Type
import os
import json


"""
    ===========================================================================
    Specific IPTC Photo Metadata structure classes
"""

@dataclass
class CreatorContactInfo:
  address: Optional[str] = None
  city: Optional[str] = None
  country: Optional[str] = None
  emailwork: Optional[str] = None
  phonework: Optional[str] = None
  postalCode: Optional[str] = None
  region: Optional[str] = None
  weburlwork: Optional[str] = None

@dataclass
class ArtworkOrObject:
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
class CvTerm:
  cvId: Optional[str] = None
  cvTermId: Optional[str] = None
  cvTermName: Optional[str] = None
  cvTermRefinedAbout: Optional[str] = None

@dataclass
class EmbdEncRightsExpr:
  rightsExprLangId: Optional[str] = None
  rightsExprEncType: Optional[str] = None
  encRightsExpr: Optional[str] = None

@dataclass
class Entity:
  identifiers: Optional[List[str]] = None
  name: Optional[str] = None

@dataclass
class RegionBoundaryPoint:
  rbX: Optional[int] = None
  rbY: Optional[int] = None

@dataclass
class RegionBoundary:
  rbShape: Optional[str] = None
  rbUnit: Optional[str] = None
  rbX: Optional[int] = None
  rbY: Optional[int] = None
  rbW: Optional[int] = None
  rbH: Optional[int] = None
  rbRx: Optional[int] = None
  rbVertices: Optional[List[Type[RegionBoundaryPoint]]] = None

@dataclass
class ImageRegion:
  regionBoundary: Optional[Type[RegionBoundary]] = None
  rId: Optional[str] = None
  name: Optional[str] = None
  rCtype: Optional[List[Type[Entity]]] = None
  rRole: Optional[List[Type[Entity]]] = None
  any: Optional[List[dict]] = None

@dataclass
class LinkedEncRightsExpr:
  rightsExprLangId: Optional[str] = None
  rightsExprEncType: Optional[str] = None
  linkedRightsExpr: Optional[str] = None

@dataclass
class Licensor:
  licensorID: Optional[str] = None
  licensorName: Optional[str] = None
  licensorURL: Optional[str] = None

@dataclass
class Location:
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
class PersonWDetails:
  characteristics: Optional[List[Type[CvTerm]]] = None
  description: Optional[str] = None
  identifiers: Optional[List[str]] = None
  name: Optional[str] = None

@dataclass
class ProductWGtin:
  description: Optional[str] = None
  gtin: Optional[str] = None
  name: Optional[str] = None

@dataclass
class RegistryEntry:
  assetIdentifier: Optional[str] = None
  registryIdentifier: Optional[str] = None
  role: Optional[str] = None

@dataclass
class CreatorExt:
    identifiers: List[str] = None
    name: Optional[str] = None
    jobtitle: Optional[str] = None
    creatorContactInfo: Optional[Type[CreatorContactInfo]] = None

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
    _jobtitle: Optional[str] = None
    _creditLine: Optional[str] = None
    _dateCreated: Optional[str] = None
    _description: Optional[str] = None
    _captionWriter: Optional[str] = None
    _headline: Optional[str] = None
    _instructions: Optional[str] = None
    _intellectualGenre: Optional[str] = None
    _jobid: Optional[str] = None
    _keywords: Optional[List[str]] = None
    _provinceState: Optional[str] = None
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

    iptc_serializationformats = ('IIM', 'XMP')
    iptc_deprecatedlocationrole = ('created', 'shown')

    def __init__(self):
        self._currentdir = ''
        self._supported_iptcpmd_tlprops = ()  # Tuple of semantic IPTC metadata property names supported by a (sub)class
        # Preferred iptc_serializationformat while reading and parsing serialized metadata
        self._serialization_pref_read = self.iptc_serializationformats[1]
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
    def serialization_pref_read(self):
        return self._serialization_pref_read

    @serialization_pref_read.setter
    def serialization_pref_read(self, iptc_serializationformat_index ):
        if iptc_serializationformat_index in range(0, 1):
            self._serialization_pref_read = self.iptc_serializationformats[iptc_serializationformat_index]

    @property
    def semiptc_metadata(self):
        """Gets dictionary of semantic IPTC Photo Metadata"""
        return self._semiptc_metadata

    @semiptc_metadata.setter
    def semiptc_metadata(self, semiptc_metadata):
        """Sets dictionary of semantic IPTC Photo Metadata"""
        self._semiptc_metadata = semiptc_metadata

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

    """
        *******************************************************************
        Exporting and importing metadata to JSON files
    """

    def export_semiptc_as_jsonfile(self, json_fp):
        """Exports the semantic IPTC Photo Metadata of this class to a JSON file"""
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
                    self._seret_metadata = json.load(pmdfile)

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

    def semiptc2seret_creatorsExt(self):
        if self._creatorsExt is not None:
            if len(self._creatorsExt) > 0:
                creatorname = self._creatorsExt[0].get('name', '')
                if creatorname != '':
                    self._seret_metadata['IFD0:Artist'] = self._
                    self._seret_metadata['IPTC:By-line'] = creatorname
                    xmpcreator = [creatorname]
                    self._seret_metadata['XMP-dc:Creator'] = xmpcreator

    def semiptc2seret_copyrightNotice(self):
        if self._copyrightNotice is not None:
            self._seret_metadata['IFD0:Copyright'] = self._copyrightNotice
            self._seret_metadata['IPTC:CopyrightNotice'] = self._copyrightNotice
            self._seret_metadata['XMP-dc:Rights'] = self._copyrightNotice

    def semiptc2seret_creditLine(self):
        if self._creditLine is not None:
            self._seret_metadata['IPTC:Credit'] = self._creditLine
            self._seret_metadata['XMP-photoshop:Credit'] = self._creditLine

    def semiptc2seret_webstatementRights(self):
        if self._webstatementRights is not None:
            self._seret_metadata['XMP-xmpRights:WebStatement'] = self._webstatementRights

    def semiptc2seret_licensors(self):
        if self._licensors is not None:
            if len(self._licensors) > 0:
                if self._licensors[0].licensorURL is not None:
                    xmplicensor = {'LicensorURL': self._licensors[0].licensorURL}
                    xmplicensors = [xmplicensor]
                    self._seret_metadata['XMP-plus:Licensor'] = xmplicensors

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

    def seret2semiptc_copyrightNotice(self):
        if 'XMP-dc:Rights' in self._seret_metadata:
            self._copyrightNotice = self._seret_metadata['XMP-dc:Rights']

    def seret2semiptc_creditLine(self):
        if 'XMP-photoshop:Credit' in self._seret_metadata:
            self._creditLine = self._seret_metadata['XMP-photoshop:Credit']

    def seret2semiptc_webstatementRights(self):
        if 'XMP-xmpRights:WebStatement' in self._seret_metadata:
            self._webstatementRights = self._seret_metadata['XMP-xmpRights:WebStatement']

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

