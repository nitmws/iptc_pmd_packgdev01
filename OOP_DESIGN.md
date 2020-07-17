# OOP Design of the IPTC Photometadata project

This file documents the development state of 2020-07-16.

* This project builds on the OOP features of Python 3, in particular on classes.
* The Python features dataclasses.dataclass and @property decorator is used
* The Python helper type hint (typing) is used

## The classes
The generic design is:
* The abstract class IptcPhotometadata (in common.py) supports all photo metadata properties defined by the [IPTC Photo Metadata (PMD) Standard](https://www.iptc.org/std/photometadata/specification/IPTC-PhotoMetadata) and provides methods for transforming them (more details below)
* Note: the names of the IPTC properties in this class follows the JSON naming defined by the standard. This naming syntax is different to the recommended Python naming but it simplifies the linking between IPTC Standard and Python code.
* Each IPTC PMD property is an internal attribute of the class, its name is prefixed with an underscore _. This should show Python editors: don't access the attribute directly. 
* For the getting and setting values of these attributes a Python class property should be used.
* Such class properties are defined by a subclass of IptcPhotometadata: it defines which IPTC properties are supported by it by defining a Python property for each of them.  The corresponding programming rule is: get and set only an IPTC property which is supported by a subclass of IptcPhotometadata and providing a Python property for it. (See also the Real User sections below.)
* The class IptcPhotometadata supports the transformation of the semantic IPTC properties defined by the IPTC PMD Standard (name, semantics, basic data type, cardinality) into expressions of this property in the IPTC IIM format, the ISO XMP format and the Exif Tag format. (The name of methods doing that starts with semipt2seret_.)
* The class IptcPhotometadata supports the transformation of a collection of metadata "fields" related to a semantic IPTC PMD property in the formats IPTC IIM, ISO XMP and the Exif Tag into a single value which is applied to the corresponding internal attribute representing the IPTC PMD property.
* Which IPTC PMD properties are supported by an instance of a subclass of IptcPhotometadata is set by the class attribute semiptc_propnames, a tuple of all supported internal attribute names. (The class IptcPhotometadata sets a default value of all IPTC PMD properties.)
* All the structures defined by the IPTC PMD Standard (e.g. Location, Registry Entry) are implemented as a specific Python class, all of them are a subclass of the IptcStructure class.
* The class IptcPhotometadata supports the use of ExifTool for embedding metadata into image files and retrieving metadata from them. This is done by the Exiftool class (in exiftool.py) with a core functionality created by Henry Sautter, a few methods for an API accessible for the IptcPhotometadata class were added.
   
##  Real use of the abstract classes:

* (See as examples: the class IptcPhotometadataGeneric (in generiy.py) support all IPTC PMD properties and the class IptcPhotometadataForSe (in specific.py) supporting only a few properties.)
* A subclass of IptcPhotometadata must be created and all the IPTC PMD properties to be supported by it must be defined - "on paper" first.
* This subclass must have:
    * a property getter and setter for each supported property. BUT: Some transactions could be made by them, e.g. in the IptcPhotometadataForSe class the licensorUrl is the supported property but internally a corresponding Licensor structure/class is set and the licensorUrl is applied to the corresponding attribute of the Licensor class. This means a metadata property exposed to the outside by a subclass must not be a one-on-one of an IPTC PMD property. Actually the properties of such a subclass should follow the needs from outside the class, e.g. a form in a GUI.
    * The class attribute semiptc_propnames must be set accordingly: the tuple must include all internal attribute names which are set by the getters and setters of the properties of this subclass. 

### Embedding photo metadata

Such a subclass can be instantiated by a Python script and used for **embedding metadata** this way:
* Set the properties with values from this script
* If the to be set property is an IPTC PMD structure: instantiate a corresponding class and set the property with this instance
* Execute the method transform_semiptc_metadata_to_seret(). Result: all set property values are transformed to IPTC IIM, ISO XMP and Exif Tags. This Python dictionary is kept as public property seret_metadata.
* If the metadata should be embedded: create and instance of the Exiftool class and hand over the seret_metadata of the IPTC class to the Exiftool class property etdata. Then execute the Exiftool method embeddata_using_json with the image file name of the path of a folder with image files as parameter.

Examples of such a script: 
* test_iptc_pmd_generic_all1.py, it uses the IptcPhotometadataGeneric subclass. Its function semiptc2seret implements what was explained above.
* test_iptc_pmd_01.py, it uses the IptcPhotometadataForSe subclass. Its main function implements what was explained above.

### Retrieving mbedded photo metadata

Such a subclass can be instantiated by a Python script and used for **retrieving metadata** this way:

* Create an instance of the Exiftool class and execute its method retrievedata with the file name of the image file as parameter. The retrieved metadata are stored as attribute of this class.
* Copy the metadata from the Exiftool class (property: etdata) to the IptcPhotometadata subclass (property: seret_metadata)
* With the subclass instance execute the method transform_seret_metadata_to_semiptc. It transforms the multiple IIM/XMP/Exif values to a single semantic IPTC PMD property value and stores it in the corresponding attribute of the class.
* Get the IPTC PMD property values by reading the corresponding Python properties of this class.

Example of such a script: 
* test_iptc_pmd_generic_all1.py, it uses the IptcPhotometadataGeneric subclass. Its function seret2semiptc implements what was explained above.
