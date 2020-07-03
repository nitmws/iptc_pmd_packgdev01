"""
    This module provides specific IPTC photo metadata classes
    Draft: 2020-06-25/MS
"""
from .common import IptcPhotometadata, Licensor




class IptcPhotometadataForSe(IptcPhotometadata):
    """IPTC Photo Metadata for search engines

        The class is derived from the generic Photometadata class, including ExifTool as worker.
        The set of supported IPTC properties is taylored to the need of search engines like Google.
    """
    supported_iptcprops = ('creatorsExt', 'copyrightNotice', 'creditLine', 'webstatementRights', 'licensors')

    def __init__(self):
        super().__init__()
        self._supported_iptcpmd_tlprops = self.supported_iptcprops
        self._semiptc_metadata['creatorNames'] = self.creatornames
        self._semiptc_metadata['copyrightNotice'] = self.copyright_notice
        self._semiptc_metadata['creditLine'] = self.credit
        self._semiptc_metadata['webstatementRights'] = self.webstatementrightsurl
        self._semiptc_metadata['licensors'] = self.licensors

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
        _creator = {'name': value}
        self._semiptc_metadata['creatorsExt'].append(_creator)

    def set_first_creator(self, value):
        """Sets an image creator name as the first and only one of the creator names"""
        _creator = {'name': value}
        self._semiptc_metadata['creatorsExt'] = []
        self._semiptc_metadata['creatorsExt'].append(_creator)
        

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
        self._semiptc_metadata['webstatementRights'] = value

    @property
    def licensors(self):
        """Gets a set of licensors"""
        item = ''
        if self._licensors is not None:
            if self._licensors[0]['licensorURL'] is not None:
                item = self._licensors[0]['licensorURL']
        return item

    @property
    def licensorurl(self):
        """Gets licensorURL from the first licensor in the array"""
        if self._licensors is None:
            return ''
        else:
            if self._licensors[0].licensorUrl:
                return self._licensors[0].licensorUrl
            else:
                return ''

    @licensorurl.setter
    def licensorurl(self, value, licensoridx=0):
        """Sets licensorURL for one of the licensors in the array, by default for the first licensor"""
        if self._licensors is not None:
            listlen = len(self._licensors)
            if licensoridx < listlen:
                self._licensors[licensoridx]['licensorURL'] = value
        else:
            self._licensors = []
            if licensoridx == 0:
                _licensor = Licensor()
                _licensor.licensorURL = value
                list(self._licensors).append(_licensor)


