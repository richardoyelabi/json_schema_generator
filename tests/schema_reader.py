from unittest import TestCase, mock
from schema_generator.schema_reader import SchemaReader

import json


class SchemaReaderTest(TestCase):
    def setUp(self) -> None:
        test_data_path: str = "tests/fixtures/test_data/test_data_1.json"
        test_schema_path = "tests/fixtures/test_schema/test_schema_1.json"

        with (
            open(test_data_path) as test_data_file,
            open(test_schema_path) as test_schema_file
        ):
            self.test_data_obj = json.load(test_data_file)
            self.test_schema_obj = json.load(test_schema_file)

        self.schema_reader = SchemaReader(self.test_data_obj)

    def test_init(self):
        """Test that SchemaReader object is initialized correctly."""
        self.assertEqual(self.schema_reader.obj, self.test_data_obj)
        self.assertEqual(self.schema_reader._keys_of_interest, ("message",))
        self.assertEqual(
            self.schema_reader.obj_subset_to_read, 
            {"message": self.test_data_obj["message"]}
        )
        self.assertEqual(self.schema_reader._default_object_schema, {
            "type": "",
            "tag": "",
            "description": "",
            "required": False
        })

    def test_schema(self):
        self.assertEqual(self.schema_reader.schema, self.test_schema_obj)

    def test__build_schema_on_empty_dict(self):
        """Test _build_schema for {"message": {}}."""
        test_obj = {"message": {}}
        schema_reader = SchemaReader(test_obj)
        schema = schema_reader._build_schema()
        self.assertEqual(schema, test_obj)
        
    @mock.patch.object(SchemaReader, "_get_object_schema")
    def test__build_schema(self, _get_object_schema):
        self.schema_reader._build_schema()
        _get_object_schema.assert_called_once_with(
            self.schema_reader.obj_subset_to_read)
