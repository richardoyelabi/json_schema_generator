import unittest
from schema_generator.schema_reader import SchemaReader
from schema_generator.json_manager import JSONObject

import json
import os
from typing import List, Tuple


class TestSchemaGeneration(unittest.TestCase):
    def setUp(self) -> None:
        test_data_folder: str = "tests/fixtures/test_data/"
        test_schema_folder: str = "tests/fixtures/test_schema/"
        test_data_files: tuple = ("test_data_1.json", "test_data_1.json")
        test_schema_files: tuple = ("test_schema_1.json", "test_schema_2.json")

        test_data_filenames: tuple = tuple([
            os.path.abspath(os.path.join(test_data_folder, data_file)) 
            for data_file in test_data_files
        ])
        test_schema_filenames: tuple = tuple([
            os.path.abspath(os.path.join(test_schema_folder, schema_file)) 
            for schema_file in test_schema_files
        ])

        self.json_objects: List[Tuple[JSONObject, JSONObject]] = []

        for instance_files in zip(
            test_data_filenames, test_schema_filenames, strict=True):

            with(
                open(instance_files[0]) as data_file,
                open(instance_files[1]) as schema_file
            ):
                test_data_object: JSONObject = json.load(data_file)
                test_schema_object: JSONObject = json.load(schema_file)

                self.json_objects.append((test_data_object, test_schema_object))

        self.schema_readers: List[SchemaReader] = [
            SchemaReader(instance[0]) for instance in self.json_objects
        ]
        self.schemas: List[JSONObject] = [
            schema_reader.schema for schema_reader in self.schema_readers
        ]

    def test_sample_json(self):
        pass

    def test_keys_of_interest(self):
        for index, instance in enumerate(self.json_objects):
            schema_reader = self.schema_readers[index]
            schema = self.schemas[index]

            keys_of_interest = schema_reader._keys_of_interest
            schema_keys = schema.keys()

            for key in keys_of_interest:
                self.assertIn(key, schema_keys)
            
            self.assertEqual(len(schema_keys), len(keys_of_interest))

    def test_paddings(self):
        pass


class TestGetListItemTypes(unittest.TestCase):
    """
    Test SchemaReader._get_list_item_types.
    """
    def setUp(self) -> None:
        json_object = dict()
        self.schema_reader = SchemaReader(json_object)

    def run_test(self):
        obj = [
            3, 5,
            "test string\n", 
            3.2, 
            False, 
            [2,3,"four"], 
            0.34, 
            {"key": 74123, "nan": "value"}
        ]
        types = self.schema_reader._get_list_item_types(obj)
        self.assertEqual(types, [int, str, float, bool, list, dict])


if __name__=='__main__':
    unittest.main()