"""
    This module provides specific IPTC photo metadata classes
"""
from dataclasses import dataclass
from .common import IptcPhotometadata, CreatorExt, CreatorContactInfo, Licensor


@dataclass
class IptcPhotometadataForSe(IptcPhotometadata):
    """IPTC Photo Metadata for search engines

        The class is derived from the generic Photometadata class.
        The set of supported IPTC properties is taylored to the need of search engines like Google.
    """

    supported_iptcprops = ('creatorsExt', 'copyrightNotice', 'creditLine', 'webstatementRights', 'licensors')

    def __init__(self):
        super().__init__()
        self._supported_iptcpmd_tlprops = self.supported_iptcprops

    @property
    def creatornames(self):
        """Gets names of image creators"""
        namelist = []
        if self._creatorsExt is not None:
            for _creatorExt in self._creatorsExt:
                if _creatorExt.name is not None:
                    namelist.append(_creatorExt.name)
        return ', '.join(namelist)

    @creatornames.setter
    def creatornames(self, value):
        """Sets = appends a single image creator with name"""
        _creator = CreatorExt()
        _creator.name = value
        self._creatorsExt.append(_creator)

    def set_first_creator(self, value):
        """Sets an image creator name as the first and only one of the creator names"""
        _creator = CreatorExt()
        _creator.name = value
        self._creatorsExt = []
        self._creatorsExt.append(_creator)

    def set_first_creatorwithweburl_TEST(self, name, weburl):
        """Sets an image creator name as the first and only one of the creator names + plus a web url"""
        _creator = CreatorExt()
        _creator.name = name
        _contactinfo = CreatorContactInfo()
        _contactinfo.weburlwork = weburl
        _creator.creatorContactInfo = _contactinfo
        self._creatorsExt = []
        self._creatorsExt.append(_creator)

    @property
    def copyright_notice(self):
        """Gets copyright notice"""
        return self._copyrightNotice

    @copyright_notice.setter
    def copyright_notice(self, value):
        """Sets copyright notice"""
        self._copyrightNotice = value

    @property
    def credit(self):
        """Gets credit line"""
        return self._creditLine

    @credit.setter
    def credit(self, value):
        """Sets credit line"""
        self._creditLine = value

    @property
    def webstatementrightsurl(self):
        """Gets web statement of rights"""
        return self._webstatementRights

    @webstatementrightsurl.setter
    def webstatementrightsurl(self, value):
        """Sets web statement of rights"""
        self._webstatementRights = value

    @property
    def licensorurl(self):
        """Gets licensorURL from the first licensor in the array"""
        if self._licensors is None:
            return ''
        else:
            if len(self._licensors) > 0:
                if self._licensors[0].licensorURL:
                    return self._licensors[0].licensorURL
                else:
                    return ''

    @licensorurl.setter
    def licensorurl(self, value):
        """Sets licensorURL for the first licensor in the array"""
        if self._licensors is not None:
            if len(self._licensors) > 0:
                self._licensors[0].licensorURL = value
        else:
            self._licensors = []
            _licensor = Licensor()
            _licensor.licensorURL = value
            self._licensors.append(_licensor)
            pass



