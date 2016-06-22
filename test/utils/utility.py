from copy import deepcopy


class Utility(object):
    """
    Store for resuable snippets of code.
    """

    @classmethod
    def dict_search(cls, obj, key):
        """
        Search a dictionary recursively for a key.
        Args:
            obj (dict): The dictionary to search in
            key (str): The key to search
        Returns:
            mixed: Value at key if found, None otherwise
        """

        if key in obj:
            return obj[key]

        for k, v in obj.items():
            if isinstance(v, dict):
                item = cls.dict_search(v, key)

                if item is not None:
                    return item

    @classmethod
    def merge(cls, source, target=False, copy=True):
        """
        Merges a target dict into a source dict.
        Basically it does source.update(target) or makes a new dict; however this allows for target
        to be False or None and ignores that as needed as opposed to raising an
        exception
        Args:
            source (dict): The dictionary to merge into
            target (iterable): Thing to merge. If non dict passed, indecies are
                               used as keys
        Returns:
            dict: The merged dict
        """
        if not target:
            target = {}

        # @TODO Make this work for other iterable as well
        if type(target) is dict:
            if not copy:
                source.update(target)
                return
            else:
                rtn = deepcopy(source)
                rtn.update(target)
                return rtn

    @classmethod
    def filter(cls, collection, targets):
        # @TODO Make this work for other iterable as well
        return {key: collection[key] for key in targets if key in collection}
