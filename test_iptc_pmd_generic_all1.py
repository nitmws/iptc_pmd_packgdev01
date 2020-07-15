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
    iptcmd_out.additionalModelInfo = 'Models are elegant'
    iptcmd_out.organisationInImageCodes = ['ADBE', 'IPTC']
    iptcmd_out.organisationInImageNames = ['Adobe', 'International Press Telecommunication Council']
    t_entity1 = Entity()
    t_entity1.identifiers = ['https://organisations.example.com/id/2143312',
                                  'https://otherorgs.example.com/id/2143312']
    t_entity1.name = 'The Entity No 1'
    t_entity2 = Entity()
    t_entity2.identifiers = ['https://organisations.example.com/id/94543892',
                             'https://otherorgs.example.com/id/98457243']
    t_entity2.name = 'The Entity No 2'
    iptcmd_out.copyrightOwners = [t_entity1, t_entity2]
    iptcmd_out.digitalImageGuid = 'https://reg.example.org/imageguid/1k4h34hk134kj34l3k2'
    iptcmd_out.digitalSourceType = 'http://cv.iptc.org/newscodes/digitalsourcetype/digitalCapture'
    iptcmd_out.eventName = 'The Great Event'
    iptcmd_out.genres = [t_cvterm1, t_cvterm2]
    iptcmd_out.imageRating = 2

    t_regentry1 = RegistryEntry()
    t_regentry1.registryIdentifier = 'https://example.org/registry/4535345'
    t_regentry1.assetIdentifier = 'https://4535345.registries.example.org/asset/897987'
    t_regentry1.role = 'https://cv.example.org/registryrole/supplier'
    t_regentry2 = RegistryEntry()
    t_regentry2.registryIdentifier = 'https://example.org/registry/8914343'
    t_regentry2.assetIdentifier = 'https://8914343.registries.example.org/asset/12314123432'
    t_regentry2.role = 'https://cv.example.org/registryrole/distributor'
    iptcmd_out.registryEntries = [t_regentry1, t_regentry2]
    iptcmd_out.suppliers = [t_entity1, t_entity2]
    iptcmd_out.imageSupplierImageId = 'LifePhotos13423423'


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
    iptcmd_out.personInImageNames = ['Henriette Fillinger', 'Carl Subunder']
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
    t_productShown1 = ProductWGtin()
    t_productShown1.gtin = '4013389438797'
    t_productShown1.name = 'GRAUPNER ULTRAMAT 18 12/230V LADER'
    t_productShown1.description = 'Preiswertes computergesteuertes Universal-Schnellladegeraet'
    t_productShown2 = ProductWGtin()
    t_productShown2.gtin = '020334700612'
    t_productShown2.name = 'TRAXXAS SLASH 4X4 #25 MARK JENKINS RTR 1/16'
    t_productShown2.description = 'The Traxxas Slash set the standard for short-course fun and versatility'
    iptcmd_out.productsShown = [t_productShown1, t_productShown2]
    iptcmd_out.webstatementRights = 'https://pizzashort.example.com/copyright-licensing'
    # now finalize and embed
    iptcmd_out.export_semiptc_as_jsonfile('./semiptc-all_sem.json')
    iptcmd_out.export_self_as_jsonfile('./iptcmd_out-self.json')
    iptcmd_out.transform_semiptc_metadata_to_seret()
    iptcmd_out.export_seret_as_jsonfile('./semiptc-all_seret.json')
    et.etdata = iptcmd_out.seret_metadata
    embedresult = et.embeddata_using_json('./images/test-image-1.jpg')  # a single image
    print(embedresult)


def create_thinglist(in_thing):
    thing_list = []
    for thing in in_thing:
        thing_dict = thing.todict()
        thing_list.append(thing_dict)
    return thing_list


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
        res_log.write('\n* Creator Extensive: ' + json.dumps(create_thinglist(iptcmd_in.creatorsExt), indent=2))
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
        res_log.write('\n* About CV-Terms: ' + json.dumps(create_thinglist(iptcmd_in.aboutCvTerms), indent=2))
        res_log.write('\n* Addl Model Information: ' + iptcmd_in.additionalModelInfo)
        res_log.write('\n* Organisation in Image/Codes: ' + ', '.join(iptcmd_in.organisationInImageCodes))
        res_log.write('\n* Organisation in Image/Names: ' + ', '.join(iptcmd_in.organisationInImageNames))
        res_log.write('\n* Copyright Owners: ' + json.dumps(create_thinglist(iptcmd_in._copyrightOwners), indent=2))
        res_log.write('\n* Digital Image GUID: ' + iptcmd_in.digitalImageGuid)
        res_log.write('\n* Digital Source Type: ' + iptcmd_in.digitalSourceType)
        res_log.write('\n* Event Name: ' + iptcmd_in.eventName)
        res_log.write('\n* Genres: ' + json.dumps(create_thinglist(iptcmd_in.genres), indent=2))
        res_log.write('\n* Image Rating: ' + str(iptcmd_in.imageRating))
        res_log.write('\n* Image Registry Entry: ' + json.dumps(create_thinglist(iptcmd_in.registryEntries), indent=2))
        res_log.write('\n* Image Supplier: ' + json.dumps(create_thinglist(iptcmd_in.suppliers), indent=2))
        res_log.write('\n* Image Supplier Image Id: ' + iptcmd_in.imageSupplierImageId)


        res_log.write('\n* Licensors: ' + json.dumps(create_thinglist(iptcmd_in.licensors), indent=2))
        res_log.write('\n* Location Created: ' + json.dumps(iptcmd_in.locationCreated.todict(), indent=2))
        res_log.write('\n* Locations Shown: ' + json.dumps(create_thinglist(iptcmd_in.locationsShown), indent=2))
        res_log.write('\n* Persons Shown: ' + ', '.join(iptcmd_in.personInImageNames))
        res_log.write('\n* Persons Shown with Details: ' + json.dumps(create_thinglist(iptcmd_in.personsShown),
                                                                      indent=2))
        res_log.write('\n* Products Shown: ' + json.dumps(create_thinglist(iptcmd_in.productsShown), indent=2))
        res_log.write('\n* Web Statement of Rights/Copyright URL: ' + iptcmd_in.webstatementRights)



# ************** MAIN

semiptc2seret()

seret2semiptc()


