'''
Created on 31 mars 2020

@author: laurentmichel
'''
from astropy.io.votable import parse
from client.inst_builder import logger, table_mapper
from client.translator.instance_from_votable import InstanceFromVotable
from client.translator.json_mapping_builder import JsonMappingBuilder
from client.inst_builder.table_mapper import TableMapper
from client.inst_builder.json_block_extractor import JsonBlockExtractor

class VodmlInstance(object):
    '''
    This class manages the transformation of a VOTable mapping blocks into a 
    model instance serialized in a Python {}
    '''

    def __init__(self, votable_path, exit_validation=True):
        #
        # One table_mapper per TABLE_MAPPING
        # table ID or name taken as keys
        #
        self.table_mappers = {}
        self.votable_path = votable_path   
        #
        # Dict translation of the <MODEL_INSTANCE> block
        #
        self.json_view = {}       
        # Convert the XML mapping block in a dictionary
        self.build_json_view(exit_validation=exit_validation)
        # Make the dictionary  compliant with JSON mapping syntax
        self.build_json_mapping()
        # Build the table_mapper
        self.build_table_mapper_map()
        
      
    def build_json_view(self, exit_validation=True):
        """
        Convert the XML mapping block into a dictionary (XML2json transform)
        """
        logger.info("Extracting the MODEL_INSTANCE block")
        instanceFromVotable = InstanceFromVotable(self.votable_path, exit_validation=exit_validation)
        instanceFromVotable._extract_vodml_block()
        logger.info("Validating the MODEL_INSTANCE block")
        instanceFromVotable._validate_vodml_block()
        logger.info("Extracting the raw JSON block")        
        self.json_view = instanceFromVotable.json_block     

    def build_json_mapping(self):
        """
        Replace in the  XML2json the elements related to the model (COLLECTION, INSTANCE, ATTRIBUTE) with their roles
        The other element, the parser directives (TABLE_ROW_TEMPLATE...), are kept in place
        """
        logger.info("Formating the JSON view")
        builder = JsonMappingBuilder(json_dict=self.json_view)
        builder.revert_compositions("COLLECTION")
        builder.revert_templates()
        builder.revert_elements("INSTANCE")
        builder.revert_elements("ATTRIBUTE")
        self.json_view = builder.json

    def build_table_mapper_map(self):
        """
        Build one TableMapper for each mapped table (TABLE_MAPPING) and store them 
        in a map using the table ID (or name if no ID) as keys.
        TODO map the first table by default
        """
        logger.info("Looking for tables matching TABLE_MAPPING ")
        votable = parse(self.votable_path)
        for template_key in self.json_view["MODEL_INSTANCE"]["TABLE_MAPPING"].keys():
            logger.info("Looking for a table matching TABLE_MAPPING %s", template_key)

            name = None
            parsed_table = None
            for table in votable.iter_tables():
                if  template_key == table.ID:
                    logger.info("Table with ID = %s found", template_key)
                    name = table.ID
                    parsed_table = table
                    break
            if name == None:
                for table in votable.iter_tables():
                    if  template_key == table.name:
                        logger.info("Table with name = %s found", template_key)
                        name = table.name
                        parsed_table = table
                        break
            if name == None:
                raise Exception("Cannot find table with name or ID equals to None")
            else:
                logger.info("Add TableMapper for table %s", name)
                self.table_mappers[template_key] = TableMapper(
                    template_key,
                    self.votable_path,
                    parsed_table=parsed_table,
                    json_inst_dict=self.json_view)

    def populate_templates(self, resolve_dmrefs=False):
        """
        resolve all @ref with values read in the VOTable
        if resolve_dmrefs is true, the INSTANCE references are replaces with a copies of the actual objects
        """
        for k, v in self.table_mappers.items():
            logger.info("populate template %s", k)
            v.resolve_refs_and_values(resolve_dmrefs=resolve_dmrefs)
            v.map_columns()        
 
    def connect_join_iterators(self):
        """
        Connect the table iterators located in the mapping blocks (TABLE_RAW_TEMPLATE) 
        with the VOTable parser
        """
        logger.info("connect join iterators")
        parse_tables = {}
        for template, table_mapper in self.table_mappers.items():
            parse_tables[template] = table_mapper.parsed_table
            
        for template, table_mapper in self.table_mappers.items():
            for target, join_iterator in table_mapper.join_iterators.items():
                logger.info("join template %s with template %s", template, target)
                join_iterator.connect_votable(parse_tables[target])

    def get_root_element(self, root_class):
        """
        Look for the table mapper (TABLE_MAPPING) having one child matching root_class
        The root element is selected accordiing one of these criteria
        - having no role attribute (should never occur actually)
        - having an empty dmrole
        - having dmrole = root
        
        :param root_class: dmtype of the root class
        :type root_class: string
        :return: the table mapper of the table containing the root element (or None)
        :rtype: TableMapper instance
        """
        for template, table_mapper in self.table_mappers.items():
            logger.info("Looking for %s instances in template %s", root_class, template)
            json_block_extract = JsonBlockExtractor(table_mapper.json)
            retour = json_block_extract.search_subelement_by_type(root_class)
            for block in retour:
                if "@dmrole" not in block.keys():
                    logger.info("found (no role)")
                    return table_mapper
                role = block["@dmrole"]
                if role == "" or role == "root":
                    logger.info("found with role=%s", role)
                    return table_mapper
        return None
