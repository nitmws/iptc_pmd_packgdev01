# CHANGELOG of the iptc_photometadata package (under development)

(History: latest on top)

* 2020-07-04: serialization of all attributes of the IptcPhotometadata class to a JSON file. Tricky part: transform the attributes of a type of a custom class to a dictionary. class IptcStructure added with a todict method, all classes representing an IPTC structure are a subclass of IptcStructure. TODO: structure classes with attributes being another IptcStructure need a custom todict()