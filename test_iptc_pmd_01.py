from pathlib import PurePath
import os
import sys
from iptc_photometadata.exiftool import Exiftool
from iptc_photometadata.specific01 import IptcPhotometadataForSe


def main():
    currentdir = os.path.dirname(sys.argv[0])
    if PurePath(sys.argv[0]).match('Contents/Resources/*.py'):  # This is an .app package
        currentdir = str(PurePath(currentdir).parents[2])

    et = Exiftool('')
    et.currentdir = currentdir

    # Test 1: read ExifTool metadata from a JSON file and transform it to IPTC metadata
    iptcmdse1 = IptcPhotometadataForSe()
    iptcmdse1.currentdir = currentdir
    iptcmdse1.import_seret_from_jsonfile('./myiptcpmd01.json')
    iptcmdse1.transform_seret_metadata_to_semiptc()
    print(iptcmdse1.creatornames)
    print(iptcmdse1.copyright_notice)

    # Test 2: set IPTC metadata attributes, transform them to ExifTool JSON and embed the metadata to an image file
    iptcmdse2 = IptcPhotometadataForSe()
    iptcmdse2.set_first_creator('Jane Doee')
    iptcmdse2.credit = 'Jane Doee/ABC Photo Agency'
    iptcmdse2.copyright_notice = '(c) 2020 Copyright ABC Photo Agency. All rights reserved'
    iptcmdse2.webstatementrightsurl = 'https://abcphotos.example.com/our-webstatement-of-rights'
    iptcmdse2.licensorurl = 'https://abcphotos.example.com/license-photos/pic4711'
    iptcmdse2.transform_semiptc_metadata_to_seret()
    et.etdata = iptcmdse2.seret_metadata
    embedresult = et.embeddata_using_json('./images/test-image-1.jpg')  # a single image
    print(embedresult)

    # Test 3: set IPTC metadata attributes, transform them to ExifTool JSON and embed the metadata to folder of images
    iptcmdse3 = IptcPhotometadataForSe()
    iptcmdse3.set_first_creator('Jane Doea')
    iptcmdse3.credit = 'Jane Doea/XYZ Stock Photos'
    iptcmdse3.copyright_notice = '(c) 2020 Copyright XYZ Stock Photos. All rights reserved'
    iptcmdse3.webstatementrightsurl = 'https://xyzphotos.example.com/our-webstatement-of-rights'
    iptcmdse3.licensorurl = 'https://xyzphotos.example.com/license-photos/pic341234312'
    iptcmdse3.transform_semiptc_metadata_to_seret()
    et.etdata = iptcmdse3.seret_metadata
    embedresult = et.embeddata_using_json('./images/someimg')  # a single image
    print(embedresult)

# ************** MAIN

main()