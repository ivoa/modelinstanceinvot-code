import xmlschema


class Validator:

    def __init__(self, xsd_path):
        self.xmlschema = xmlschema.XMLSchema11(xsd_path)

    def validate_file(self, xml_path: str, verbose=False) -> bool:
        if verbose is True:
            try :
                self.xmlschema.validate(xml_path)
                return True
            except Exception as e:
                print(e)
                return False
        else :
            return self.xmlschema.is_valid(xml_path)
        
    def validate_string(self, xml_string: str, verbose=False) -> bool:
        if verbose is True:
            try :
                self.xmlschema.validate(xml_string)
                return True
            except Exception as e:
                print(e)
                return False
        else :
            return self.xmlschema.is_valid(xml_string)
