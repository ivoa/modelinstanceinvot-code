'''
Code imported from SVOM
Created on 29 mai 2019

@author: michel
'''
import json
import re
import urllib
import ssl
from utils import logger
from utils.json_encoder import MyEncoder


class DictUtils():
    """
    static class processing implementing convenient operation on dictionaries
    """

    @staticmethod
    def get_required_value(dictionary, key):
        """
        returns dictionary[key] if available and rises an exception otherwise
        :param dictionary: dictionary
        :type dictionary: Python Dict
        :param key: key of the searched value
        :type key: string
        :return: the value attached to the key
        :rtype: any supported Dict value
        """
        if not dictionary:
            raise Exception("Cannot get any value for None dict")

        if key in dictionary.keys():
            return dictionary[key]
        raise Exception("missing key: {}".format(key))

    @staticmethod
    def get_fatal_value(dictionary, key):
        """
        returns dictionary[key] if available and trigger a system exit otherwise
        :param dictionary: dictionary
        :type dictionary: Python Dict
        :param key: key of the searched value
        :type key: string
        :return: the value attached to the key
        :rtype: any supported Dict value
        """
        if not dictionary:
            raise Exception("Cannot get any value for None dict")
        if key in dictionary.keys():
            return dictionary[key]
        raise Exception("missing key: {}".format(key))
        return None  # just for Pylint

    @staticmethod
    def get_optional_value(dictionary, key, null=None):
        """
        returns dictionary[key] if available or a null value otherwise
        :param dictionary: dictionary
        :type dictionary: Python Dict
        :param key: key of the searched value
        :type key: string
        :param null: value taken when the key os not available (None by default)
        :type null: string
        :return: the value attached to the key or the null value
        :rtype: any supported Dict value
        """
        if not dictionary:
            return null

        if dictionary and key in dictionary.keys():
            return dictionary[key]
        return null

    @staticmethod
    def remove_comment(dictionary):
        """
        Remove all comment keys ("$desc")
        not recursive
        :param dictionary: dictionary
        :type dictionary: Python Dict
        """
        if dictionary and "$desc" in dictionary.keys():
            dictionary.pop("$desc")

    @staticmethod
    def read_dict_from_file(filename, fatal=False):
        """
        Read a Dict in filename, rises an exception if something goes wrong
        :param filename: filename
        :type filename: string
        :param fatal: trigger a systeml exit if true
        :type fatal: boolean
        :return: the Dict extracted from the file
        :rtype: Python Dict
        """
        try:
            logger.debug("Reading json from %s", filename)
            with open(filename, 'r') as file:
                return json.load(file)

        except Exception as exception:
            if fatal is True:
                raise Exception("reading {}". format(filename))
            else:
                logger.error("{} reading {}". format(exception, filename))

    @staticmethod
    def write_dict_from_file(dictionary, filename, fatal=False):
        """
        Wrtite the dictionary in filename, rises an exception if something goes wrong
        :param filename: filename
        :type filename: string
        :param fatal: trigger a systeml exit if true
        :type fatal: boolean
        """
        try:
            logger.debug("Writing json in %s", filename)
            with open(filename, 'w') as file:
                file.write(json.dumps(dictionary, indent=2, sort_keys=True))

        except Exception as exception:
            if fatal is True:
                raise Exception("writing {}". format(filename))
            else:
                logger.error("{} writing {}". format(exception, filename))

    @staticmethod
    def read_dict_from_url(url, fatal=False):
        """
        Read a Dict from url, rises an exception if something goes wrong
        :param url: url
        :type url: string
        :param fatal: trigger a systeml exit if true
        :type fatal: boolean
        :return: the Dict extracted from the file
        :rtype: Python Dict
        """
        try:
            logger.debug("Reading json from %s", url)
            open_url = urllib.request.urlopen(url, context=ssl._create_unverified_context())
            if open_url.getcode() == 200:
                return  json.loads(open_url.read().decode('utf-8'))
            raise Exception("{} return code {}".format(url, open_url.getcode()))

        except Exception as exception:
            if fatal is True:
                raise Exception("reading {}". format(url))
            logger.error("{} reading {}". format(exception, url))
            return None  # just for Pylint

    @staticmethod
    def get_pretty_json(dictionnary):
        """
        :return: A pretty string representation of the dictionary
        :rtype: Python Dict
        """
        return json.dumps(dictionnary,
                          indent=2,
                          sort_keys=True,
                          cls=MyEncoder)

    @staticmethod
    def get_permanent_string(text):
        """
        This method make the string independent of a specific run context
        It us used to format object in a way they can be checked in unit demo
        dates values are replaced with DATE
        and the seq_id with SEQID.
        :param text: string to be formated
        :type text: string
        """
        replaced = re.sub("svom_mxt_proto_any_.*", "svom_mxt_proto_any_SEQID", text)
        replaced = re.sub("svom_test_.*", "svom_test_any_SEQID", replaced)
        replaced = re.sub("[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}", "DATE", replaced)
        return replaced

    @staticmethod
    def get_permanent_object(dico):
        """
        This method make the object content independent of a specific run context
        It us used to format object in a way they can be checked in unit demo
        dates values are replaced with DATE
        and the seq_id with SEQID.
        :param dico: object to be formated
        :type dico: anything
        """
        retour = None
        if isinstance(dico, str):
            retour = DictUtils.get_permanent_string(dico)
        elif isinstance(dico, bytes):
            retour = DictUtils.get_permanent_string(dico.decode("utf-8"))
        elif isinstance(dico, list):
            for idx, item in enumerate(dico):
                dico[idx] = DictUtils.get_permanent_object(item)
            retour = dico
        elif isinstance(dico, dict):
            for key, value in dico.items():
                dico[key] = DictUtils.get_permanent_object(value)
            retour = dico
        else:
            retour = dico
        return retour

    @staticmethod
    def get_prefixed_keys_dict(dictionnary, prefix):
        """
        Returns a copy of dict with all keys prefixed with prefix
        Works only art root level, no recursion
        :param dictionnary: dict on which key prefixes must be applied
        :type dictionnary: dict
        :param prefix:prefix to be aplied to the keys
        :type prefix: string
        :rtype: prefixed dict
        """
        retour = {}
        for key in dictionnary.keys():
            retour[prefix + "_" + key] = dictionnary[key]
        return retour
