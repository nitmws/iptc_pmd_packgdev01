# CHANGELOG of the iptc_photometadata package (under development)

Note: details of the development work, including the implementation of each IPTC PMD property, are logged on [this web page](https://docs.google.com/spreadsheets/d/e/2PACX-1vTFUFwH3Qqu3EZ_m6EJgCY5P1c88aTJMJEm9oQ7rdp_agy-K3-Lf2xKUxC8dpBi2UqVes3X3Hfy5tx5/pubhtml).

(History: latest on top)

* 2020-07-18: class IptcPhotometadata: model and property releated IPTC properties implemented. See 2020-07-18 data in development work web page.
* 2020-07-14: class IptcPhotometadataGeneric: all getters and setters with typing. Class IptcPhotometadata: some IPTC Extension properties implemented, see 2020-07-14 data in development work web page.
* 2020-07-13: IPTC Extension properties implemented (see 2020-07-13 data in development work web page). Three properties removed: ImageCreator, Max Available Width/Heigth.
* 2020-07-12: IPTC Extension properties aboutCvTerms, personsShown implemented, implementation of other properties improved
* 2020-07-10: all IPTC Core Schema properties: semiptc2seret and seret2semiptc transformations implemented. IPTC Core Schema properties: semiptc2seret and seret2semiptc transformations implemented for LocationCreated and LocationShown 
* 2020-07-06: IptcPhotometadataGeneric: generic methods for semiptc2seret and seret2semiptc transformations added.
* 2020-07-04: semiptc2seret & seret2semiptc for properties: description, headline, keywords, title, locationsShown (semiptc2seret) added.
* 2020-07-04: class IptcPhotometadataGeneric (in generic.py) added. It has all "hidden" attributes of the IptcPhotometadata class as accessible properties.
* 2020-07-04: serialization of all attributes of the IptcPhotometadata class to a JSON file. Tricky part: transform the attributes of a type of a custom class to a dictionary. class IptcStructure added with a todict method, all classes representing an IPTC structure are a subclass of IptcStructure. TODO: structure classes with attributes being another IptcStructure need a custom todict()
