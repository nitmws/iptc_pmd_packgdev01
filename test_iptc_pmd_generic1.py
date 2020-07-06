from pathlib import PurePath
import os
import sys
from iptc_photometadata.exiftool import Exiftool
from iptc_photometadata.common import *
from iptc_photometadata.generic import IptcPhotometadataGeneric



def main():
    currentdir = os.path.dirname(sys.argv[0])
    if PurePath(sys.argv[0]).match('Contents/Resources/*.py'):  # This is an .app package
        currentdir = str(PurePath(currentdir).parents[2])

    et = Exiftool('')
    et.currentdir = currentdir

    print('========== TEST 1 ============')
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
    iptcmdgen1.creditLine = "J Boltenheimer/Pizzashots"
    iptcmdgen1.description = 'The best tasting Quattro Stagione pizza worldwide.'
    iptcmdgen1.headline = 'The best headline about a pizza'
    iptcmdgen1.keywords = ['Keyword 01', 'Keyword 02']
    iptcmdgen1.webstatementRights = 'https://pizzashort.example.com/copyright-licensing'
    t_licensor = Licensor()
    t_licensor.licensorID = 'https://pizzashort.example.com'
    t_licensor.licensorName = 'Pizzashots Inc.'
    t_licensor.licensorURL = 'https://pizzashort.example.com/shot/1341234'
    iptcmdgen1.licensors = [t_licensor]
    t_location = Location()
    t_location.identifiers = ['https://locids1.example.com/4311', 'https://locids2.example.com/134234']
    t_location.sublocation = 'Sublocation1'
    t_location.city = 'Citynice1'
    t_location.provinceState = 'Province A1'
    t_location.countryName = 'Country A1'
    t_location.countryCode = 'CA1'
    t_location.worldRegion = 'Worldreagion A1'
    iptcmdgen1.locationsShown = [t_location]
    # now finalize and embed
    iptcmdgen1.export_semiptc_as_jsonfile('./iptcmdgen1-sem.json')
    iptcmdgen1.transform_semiptc_metadata_to_seret()
    iptcmdgen1.export_seret_as_jsonfile('./iptcmdgen1-seret.json')
    # et.etdata = iptcmdgen1.seret_metadata
    # embedresult = et.embeddata_using_json('./images/test-image-1.jpg')  # a single image
    # print(embedresult)

    print('========== TEST 2 ============')
    # Test 2: get some properties
    iptcmdgen2 = IptcPhotometadataGeneric()
    iptcmdgen2.currentdir = currentdir
    iptcmdgen2.import_seret_from_jsonfile('./IPTC-PhMdStd2019.1_x-All.json')
    iptcmdgen2.transform_seret_metadata_to_semiptc()
    # get properties
    print(iptcmdgen2.description)
    print(iptcmdgen2.keywords)

# ************** MAIN

main()

