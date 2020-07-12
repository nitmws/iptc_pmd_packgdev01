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
    # line below: switch between the role of the deprecated IPTC location properties (IPTC Core): CREATED or SHOWN
    iptcmd_out.deprlocationrole = IptcDeprecatedLocationRole.SHOWN
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
    t_cvterm1 = CvTerm()
    t_cvterm1.cvId = 'https://example.com/cvid/124123'
    t_cvterm1.cvTermId = 'https://example.com/termid/term22'
    t_cvterm1.cvTermName = 'Name of Term22'
    t_cvterm2 = CvTerm()
    t_cvterm2.cvId = 'https://example.com/cvid/58430'
    t_cvterm2.cvTermId = 'https://example.com/termid/term55'
    t_cvterm2.cvTermName = 'Name of Term55'
    iptcmd_out.aboutCvTerms = [t_cvterm1, t_cvterm2]
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
    iptcmd_out.locationCreated = t_location2
    iptcmd_out.locationsShown = [t_location1, t_location2]
    t_personShown1 = PersonWDetails()
    t_personShown1.identifiers = ['https://persons.example.com/id/2143312',
                                  'https://otherpersons.example.com/id/2143312']
    t_personShown1.name = 'Laura Hillinger'
    t_personShown1.description = 'Nice photo metadata editor and a secret artist'
    t_personShown1.characteristics = [t_cvterm1, t_cvterm2]
    t_personShown2 = PersonWDetails()
    t_personShown2.identifiers = ['https://persons.example.com/id/4543543',
                                  'https://otherpersons.example.com/id/758758']
    t_personShown2.name = 'Frank Muller'
    t_personShown2.description = 'Reliable event oraganizer'
    t_personShown2.characteristics = [t_cvterm2, t_cvterm1]
    iptcmd_out.personsShown = [t_personShown1, t_personShown2]
    iptcmd_out.webstatementRights = 'https://pizzashort.example.com/copyright-licensing'
    # now finalize and embed
    iptcmd_out.export_semiptc_as_jsonfile('./semiptc-all_sem.json')
    iptcmd_out.export_self_as_jsonfile('./iptcmd_out-self.json')
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
        res_log.write('\n* Copyright Notice: ' + iptcmd_in.copyrightNotice)
        creatorsExt_list = []
        for creatorExt in iptcmd_in.creatorsExt:
            creatorExt_dict = creatorExt.todict()
            creatorsExt_list.append(creatorExt_dict)
        res_log.write('\n* Creator Extensive: ' + json.dumps(creatorsExt_list, indent=2))
        res_log.write('\n* Credit Line: ' + iptcmd_in.creditLine)
        res_log.write('\n* Date Created: ' + iptcmd_in.dateCreated)
        res_log.write('\n* Caption Writer: ' + iptcmd_in.captionWriter)
        res_log.write('\n* Description: ' + iptcmd_in.description)
        res_log.write('\n* Headline: ' + iptcmd_in.headline)
        res_log.write('\n* Instructions: ' + iptcmd_in.instructions)
        res_log.write('\n* Intellectual Genre: ' + iptcmd_in.intellectualGenre)
        res_log.write('\n* Job Id: ' + iptcmd_in.jobid)
        res_log.write('\n* Keywords (multiple): ' + ', '.join(iptcmd_in.keywords))
        res_log.write('\n* Rights Usage Terms: ' + iptcmd_in.usageTerms)
        res_log.write('\n* Scene Codes (multiple): ' + ', '.join(iptcmd_in.sceneCodes))
        res_log.write('\n* Source: ' + iptcmd_in.source)
        res_log.write('\n* Subject Codes (multiple): ' + ', '.join(iptcmd_in.subjectCodes))
        res_log.write('\n* Title: ' + iptcmd_in.title)
        res_log.write('\n***** IPTC Extension Schema')
        aboutCvTerm_list = []
        for aboutCvTerm in iptcmd_in.aboutCvTerms:
            aboutCvTerm_dict = aboutCvTerm.todict()
            aboutCvTerm_list.append(aboutCvTerm_dict)
        res_log.write('\n* About CV-Terms: ' + json.dumps(aboutCvTerm_list, indent=2))
        licensors_list = []
        for licensor in iptcmd_in.licensors:
            licensor_dict = licensor.todict()
            licensors_list.append(licensor_dict)
        res_log.write('\n* Licensors: ' + json.dumps(licensors_list, indent=2))
        res_log.write('\n* Location Created: ' + json.dumps(iptcmd_in.locationCreated.todict(), indent=2))
        locationsShown_list = []
        for locationShown in iptcmd_in.locationsShown:
            locationShown_dict = locationShown.todict()
            locationsShown_list.append(locationShown_dict)
        res_log.write('\n* Locations Shown: ' + json.dumps(locationsShown_list, indent=2))
        personsShown_list = []
        for personShown in iptcmd_in.personsShown:
            personShown_dict = personShown.todict()
            personsShown_list.append(personShown_dict)
        res_log.write('\n* Persons Shown: ' + json.dumps(personsShown_list, indent=2))

# ************** MAIN

semiptc2seret()

seret2semiptc()


