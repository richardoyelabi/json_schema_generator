from .json_manager import JSONObject

from typing import Tuple
import copy


class SchemaReader:
    """
    Reads schema of native python object that would qualify as valid json.

    :param: python object that qualifies as valid json.

    Does not check that passed object is actually valid json.
    That is the responsibility of the caller.
    """

    _default_object_schema: dict = {
        "type": "",
        "tag": "",
        "description": "",
        "required": False
    }

    _keys_of_interest: Tuple = ("message",)

    schema: JSONObject = {}

    def __init__(self, obj: JSONObject) -> None:
        self.obj = obj

    @property
    def obj_subset_to_read(self):
        return {
            key: self.obj.get(key) for key in self._keys_of_interest
        }

    @property
    def schema(self):
        return self._build_schema()

    def _build_schema(self) -> JSONObject:
        """
        Build schema of objects whose keys are in self._keys_of_interest.
        """
        obj = self.obj_subset_to_read

        if not obj and isinstance(obj, dict):
            return obj
        
        schema = self._get_object_schema(obj)
        return schema

    def _get_object_schema(self, obj: JSONObject) \
        -> JSONObject:
        """
        Recursively build up schema of 'obj'.
        """

        schema = copy.deepcopy(self._default_object_schema)

        if isinstance(obj, int) and not isinstance(obj, bool):
            schema["type"] = "integer"

        elif isinstance(obj, float):
            schema["type"] = "number"

        elif isinstance(obj, bool):
            schema["type"] = "boolean"

        elif isinstance(obj, str):
            schema["type"] = "string"

        elif obj is None:
            schema["type"] = "null"

        elif isinstance(obj, dict):
            schema = self._build_object_schema_properties(obj)

        elif isinstance(obj, list):
            list_item_types = self._get_list_item_types(obj)

            if len(list_item_types)==1 and \
                issubclass(list_item_types[0], str):
                schema["type"] = "enum"

            else:
                schema["type"] = "array"
                schema["items"] = self._build_array_schema_items(
                    obj, list_item_types)

        else:
            raise ValueError("Invalid object schema.")
        
        return schema
        
    def _build_object_schema_properties(self, obj: dict) -> dict:
        """
        Build up 'properties' of json objects of the 'object' type.
        """
        props = {key: self._get_object_schema(value) 
                 for key, value in obj.items()}
        return props
    
    def _build_array_schema_items(
            self, obj: list, list_item_types: list) -> list:
        """
        Build up 'items' of json objects of the 'array' type.
        """
        no_of_types = len(list_item_types)
        if no_of_types==1:
            items = self._get_object_schema(obj[0])
        else:
            items = {}
            if no_of_types!=0:
                items["anyOf"] = [self._get_object_schema(item) 
                                  for item in obj]
        return items
    
    def _get_list_item_types(self, obj: list) -> list:
        """
        Get list of the unique data types of the items in the 'obj' list.
        """
        types = {type(item) for item in obj}
        types = list(types)
        return types
