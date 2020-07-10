from pathlib import PurePath
import os
import sys
from iptc_photometadata.exiftool import Exiftool
from iptc_photometadata.common import *
from iptc_photometadata.generic import IptcPhotometadataGeneric

currentdir = os.path.dirname(sys.argv[0])
if PurePath(sys.argv[0]).match('Contents/Resources/*.py'):  # This is an .app package
    currentdir = str(PurePath(currentdir).parents[2])


def semiptc2seret():
    et = Exiftool('')
    et.currentdir = currentdir

    print('========== semantic IPTC TO IPTC serialized ET md ============')
    iptcmd_out = IptcPhotometadataGeneric()
    iptcmd_out.currentdir = currentdir
    # set properties - it follows the sequence of properties in the project sheet
    # Core schema metadata
    iptcmd_out.copyrightNotice = '(c) 2020 Copyright Pizzashots, all rights reserved'
    creatorExt1 = CreatorExt()
    creatorExt1.identifiers = ['https://linkedin.example.com/user3143123432']
    creatorExt1.name = 'John Boltenheimer'
    creatorExt1.jobtitle = 'Staff photographer'
    creatorContactInfo = CreatorContactInfo()
    creatorContactInfo.address = 'Image House'
    creatorContactInfo.city = 'Ambersville'
    creatorContactInfo.postalCode = 'ABC234 Q12'
    creatorContactInfo.region = 'Humbershire'
    creatorContactInfo.country = 'United Kingdom of Phantasia'
    creatorContactInfo.phonework = '+40 123 38388382'
    creatorContactInfo.emailwork = 'johnb@photoatwork.com'
    creatorContactInfo.weburlwork = 'https://photoatwork.example.com'
    creatorExt1.creatorContactInfo = creatorContactInfo
    iptcmd_out.creatorsExt = []
    iptcmd_out.creatorsExt.append(creatorExt1)
    creatorExt2 = CreatorExt()
    creatorExt2.identifiers = ['https://linkedin.example.com/user830939']
    creatorExt2.name = 'Jane Morano'
    creatorExt2.jobtitle = 'Photographer'
    creatorContactInfo = CreatorContactInfo()
    creatorContactInfo.weburlwork = 'https://janem.example.com'
    creatorExt2.creatorContactInfo = creatorContactInfo
    iptcmd_out.creatorsExt.append(creatorExt2)

    iptcmd_out.creditLine = "J Boltenheimer/Pizzashots"
    iptcmd_out.dateCreated = '2020-07-07T12:13:14+02:00'
    iptcmd_out.captionWriter = 'Bobby Captionwriter'
    iptcmd_out.description = 'The best tasting Quattro Stagione pizza worldwide.'
    iptcmd_out.headline = 'The best headline about a pizza'
    iptcmd_out.intellectualGenre = 'iptcgenre:History'
    iptcmd_out.jobid = 'Jid134231'
    iptcmd_out.instructions = 'Our instruction: country XYZ out'
    iptcmd_out.keywords = ['Keyword 01', 'Keyword 02']
    iptcmd_out.usageTerms = 'The rightful usage terms'
    iptcmd_out.sceneCodes = ['SceneCode 01', 'SceneCode 02']
    iptcmd_out.source = 'The best Source of all'
    iptcmd_out.subjectCodes = ['SubjectCode 01', 'SubjectCode 02']

    iptcmd_out.title = 'A Title'
    # Extension schema metadata
    t_licensor = Licensor()
    t_licensor.licensorID = 'https://pizzashort.example.com'
    t_licensor.licensorName = 'Pizzashots Inc.'
    t_licensor.licensorURL = 'https://pizzashort.example.com/shot/1341234'
    iptcmd_out.licensors = [t_licensor]
    t_location1 = Location()
    t_location1.identifiers = ['https://locids1.example.com/4311', 'https://locids2.example.com/134234']
    t_location1.sublocation = 'Sublocation1'
    t_location1.city = 'Citynice1'
    t_location1.provinceState = 'Province A1'
    t_location1.countryName = 'Country A1'
    t_location1.countryCode = 'CA1'
    t_location1.worldRegion = 'Worldregion A1'
    t_location2 = Location()
    t_location2.identifiers = ['https://locids1.example.com/4312', 'https://locids2.example.com/1342342']
    t_location2.sublocation = 'Sublocation2'
    t_location2.city = 'Citynice2'
    t_location2.provinceState = 'Province A2'
    t_location2.countryName = 'Country A2'
    t_location2.countryCode = 'CA2'
    t_location2.worldRegion = 'Worldregion A2'
    iptcmd_out.locationCreated = t_location1
    iptcmd_out.locationsShown = [t_location1, t_location2]
    iptcmd_out.webstatementRights = 'https://pizzashort.example.com/copyright-licensing'
    # now finalize and embed
    iptcmd_out.export_semiptc_as_jsonfile('./semiptc-all_sem.json')
    iptcmd_out.transform_semiptc_metadata_to_seret()
    iptcmd_out.export_seret_as_jsonfile('./semiptc-all_seret.json')
    # et.etdata = iptcmd_out.seret_metadata
    # embedresult = et.embeddata_using_json('./images/test-image-1.jpg')  # a single image
    # print(embedresult)


def seret2semiptc():
    print('========== IPTC serialized ET md TO semantic IPTC ============')
    iptcmd_in = IptcPhotometadataGeneric()
    iptcmd_in.currentdir = currentdir
    iptcmd_in.import_seret_from_jsonfile('./semiptc-all_seret.json')  # ./semiptc-all_seret.json
    iptcmd_in.transform_seret_metadata_to_semiptc()
    with open('./semiptc-all_readResults.txt', 'w') as res_log:
        res_log.write('Results from reading a file with serialized IPTC PMD using ExifTool naming:\n')
        # get properties
        res_log.write('\n***** IPTC Core Schema')
        res_log.write('\nCopyright Notice: ' + iptcmd_in.copyrightNotice)
        creatorsExt_list = []
        for creatorExt in iptcmd_in.creatorsExt:
            creatorExt_dict = creatorExt.todict()
            creatorsExt_list.append(creatorExt_dict)
        res_log.write('\nCreator Extensive: ' + json.dumps(creatorsExt_list, indent=2))
        res_log.write('\nCredit Line: ' + iptcmd_in.creditLine)
        res_log.write('\nDate Created: ' + iptcmd_in.dateCreated)
        res_log.write('\nCaption Writer: ' + iptcmd_in.captionWriter)
        res_log.write('\nDescription: ' + iptcmd_in.description)
        res_log.write('\nHeadline: ' + iptcmd_in.headline)
        res_log.write('\nInstructions: ' + iptcmd_in.instructions)
        res_log.write('\nIntellectual Genre: ' + iptcmd_in.intellectualGenre)
        res_log.write('\nJob Id: ' + iptcmd_in.jobid)
        res_log.write('\nKeywords (multiple): ' + ', '.join(iptcmd_in.keywords))
        res_log.write('\nRights Usage Terms: ' + iptcmd_in.usageTerms)
        res_log.write('\nScene Codes (multiple): ' + ', '.join(iptcmd_in.sceneCodes))
        res_log.write('\nSource: ' + iptcmd_in.source)
        res_log.write('\nSubject Codes (multiple): ' + ', '.join(iptcmd_in.subjectCodes))
        res_log.write('\nTitle: ' + iptcmd_in.title)
        res_log.write('\n***** IPTC Extension Schema')
        res_log.write('\nLocation Created: ' + json.dumps(iptcmd_in.locationCreated.todict(), indent=2))
        locationsShown_list = []
        for locationShown in iptcmd_in.locationsShown:
            locationShown_dict = locationShown.todict()
            locationsShown_list.append(locationShown_dict)
        res_log.write('\nLocations Shown: ' + json.dumps(locationsShown_list, indent=2))

# ************** MAIN

semiptc2seret()

seret2semiptc()


