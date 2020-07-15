# iptc_pmd_packgdev01

## Developing and testing the design of a package for transforming IPTC photo metadata

State of the project: UNDER DEVELOPMENT. Not all IPTC Photo Metadata properties are implemented yet, a few transformations are not complete. A first round of testing is implemented. Current designs may be changed. See the progress in the [CHANGELOG](/iptc_photometadata/CHANGELOG.md) file.

The use case: The [IPTC Photo Metadata Standard](https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata) defines metadata properties at a semantic level first: a name/label for the property, a definition of what kind of data should be filled in and a basic data type like text or number. Next the standard defines how the value of such a metadata property is filled into fields of up to three different metadata formats used for embedding metadata into an image file: IPTC IIM (in use since 1995), ISO XMP (in use since 2002) and Exif (in use since 1995). This definition is also used for retrieving embedded metadata from an image file and setting the value of a property at its semantic level.

The goals of this package are a/ to transform the value of a semantic IPTC property into the defined metadata formats (and then to embed them), and b/ (to retrieve embedded metadata and) to transform metadata values of these three formats into a single value for a semantic IPTC property.

The challenge: in an image file the value of a description/caption of an image may be embedded in three different formats (IIM, XMP, Exif). In an ideal case the value is exactly the same in all formats, in less ideal cases the values are different. The value of which format takes precedence over other other formats? The code of this package follows the Guidelines of the Metadata Working Group, last version published in 2010. 

Note: the value of a semantic IPTC property is typically the one edited by a metadata user interface ("metadata panel").

## The directories

* Root directory: applications testing the package. Script name starts with test_. Further some files required for and created by running the tests.

* [/iptc_photometadata](/iptc_photometadata): Directory of the IPTC Photo Metadata package.
* [/images](/images): Directory of images for embedding and retrieving embedded photo metadata
* [/no-metadata-test-images](/no-metadata-test-images): Directory with image files have not any metadata embedded. Can be copied to the /images directory and used there.

## Outline of the design

* Object Oriented Programming is used with Python classes.
* To support the proper use data types the Python typing (type hinting) is used.
* To support the use of the created photo metadata the Exiftool class (in exiftool.py) enables embedding them into image files and to retrieve them from image files.
* The class IptcPhotometadata (in common.py) has all IPTC Photo Metadata Standard properties as (internal) attributes. And it supports the transformations of semantic properties to embedding formats (IIM, XMP, Exif) and the transformation of data in the embedding formats to semantic properties. But this class is designed as abstract class.
* Each metadata structure of the IPTC standard is expressed as Python class (in common.py)
* A subclass of IptcPhotometadata must define which metadata releated to IPTC properties are supported by it and for each supported property a Python property getter and setter must be created. Example: a user interface may deliver only identifiers of locations while the Location class defines a rich structure of sub-properties. The getters and setters have to take care that the user interface value Location Identifier is inserted properly into a Location class instance and read from it.
* The class IptcPhotometadataGeneric (in generic.py) covers (and supports) all metadata properties of the IPTC standard.
* The class IptcPhotometadataForSe supports only a small set of IPTC metadata relevant for search engines - and sometimes with a simplified structure.

## Testing

The major test of the current development is the test_iptc_pmd_generic_all1.py file. 

The semiptc2seret function transforms all (currently implemented) IPTC metadata properties (= semiptc) from the semantic level to their IIM/XMP/Exif serializations, the keys of the created key/value pairs follow the naming of Exiftool (= seret). The data are stored as JSON file (semiptc-all-_seret.json)

The seret2semiptc function reads the JSON file of the semiptc2seret function and merges the up to three variants of the value of a metadata property to a single value of the IPTC property at the semantic level. The label of a semantic property and its values are written to a text file (semiptc-all_readResults.txt). (For structured properties the JSON format is used.) A human eye has to check if the generated semantic IPTC property is correct.

