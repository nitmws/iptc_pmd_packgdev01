from pathlib import PurePath
import os
import sys
from iptc_photometadata.exiftool import Exiftool
from iptc_photometadata.common import CreatorExt, CreatorContactInfo, Licensor
from iptc_photometadata.generic import IptcPhotometadataGeneric



def main():
    currentdir = os.path.dirname(sys.argv[0])
    if PurePath(sys.argv[0]).match('Contents/Resources/*.py'):  # This is an .app package
        currentdir = str(PurePath(currentdir).parents[2])

    et = Exiftool('')
    et.currentdir = currentdir

    # Test 1: set some properties and embed them
    iptcmdgen1 = IptcPhotometadataGeneric()
    iptcmdgen1.currentdir = currentdir
    # set properties
    t_creator = CreatorExt()
    t_creator.identifiers = ['https://linkedin.example.com/user3143123432']
    t_creator.name = 'John Boltenheimer'
    t_creator.jobtitle = 'Staff photographer'
    t_creatorcontact = CreatorContactInfo()
    t_creatorcontact.weburlwork = 'https://photoatwork.example.com'
    t_creator.creatorContactInfo = t_creatorcontact
    iptcmdgen1.creatorsExt = [t_creator]
    iptcmdgen1.copyrightNotice = '(c) 2020 Copyright Pizzashots, all rights reserved'
    iptcmdgen1.description = 'The best tasting Quattro Stagione pizza worldwide.'
    iptcmdgen1.webstatementRights = 'https://pizzashort.example.com/copyright-licensing'
    t_licensor = Licensor()
    t_licensor.licensorID = 'https://pizzashort.example.com'
    t_licensor.licensorName = 'Pizzashots Inc.'
    t_licensor.licensorURL = 'https://pizzashort.example.com/shot/1341234'
    iptcmdgen1.licensors = [t_licensor]
    # now finalize and embed
    iptcmdgen1.export_semiptc_as_jsonfile('./iptcmdgen1-sem.json')
    iptcmdgen1.transform_semiptc_metadata_to_seret()
    et.etdata = iptcmdgen1.seret_metadata
    embedresult = et.embeddata_using_json('./images/test-image-1.jpg')  # a single image
    print(embedresult)


# ************** MAIN

main()

