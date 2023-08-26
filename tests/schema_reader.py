from unittest import TestCase, mock
from schema_generator.schema_reader import SchemaReader


import copy


class SchemaReaderTest(TestCase):
    def setUp(self) -> None:
        self.test_data_obj = mock.MagicMock(name="test_data_obj")
        self.schema_reader = SchemaReader(self.test_data_obj)

    def test_init(self):
        """Test that SchemaReader object is initialized correctly."""
        self.assertEqual(self.schema_reader.obj, self.test_data_obj)
        self.assertEqual(self.schema_reader._keys_of_interest, ("message",))
        self.assertEqual(self.schema_reader._default_object_schema, {
            "type": "",
            "tag": "",
            "description": "",
            "required": False
        })

    def test_obj_subset_to_read(self):
        self.assertEqual(
            self.schema_reader.obj_subset_to_read, 
            {"message": self.test_data_obj.get("message")}
        )

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
        
    @mock.patch.object(SchemaReader, "_build_array_schema_items")
    @mock.patch.object(SchemaReader, "_get_list_item_types")
    @mock.patch.object(SchemaReader, "_build_object_schema_properties")
    def test__get_object_schema(
        self,
        _build_object_schema_properties,
        _get_list_item_types,
        _build_array_schema_items
    ):
        test_integer: int = 1
        test_number: float = 1.0
        test_boolean: bool = True
        test_string: str = "test"
        test_null: None = None
        test_enum: list = ["test1"]
        test_array: list = ["test1", "test2", 2.3, 2, 3.2, 59]
        test_object: dict = {"test": "test"}

        
        for test_obj in (
            test_integer,
            test_number,
            test_boolean,
            test_string,
            test_null,
            test_enum,
            test_array,
            test_object
        ):
            with self.subTest(test_obj=test_obj):
                schema_reader = self.schema_reader
                expected_schema = copy.deepcopy(schema_reader._default_object_schema)

                if test_obj is test_integer:
                    schema = schema_reader._get_object_schema(test_obj)
                    expected_schema["type"] = "integer"
                    self.assertEqual(schema, expected_schema)

                elif test_obj is test_number:
                    schema = schema_reader._get_object_schema(test_obj)
                    expected_schema["type"] = "number"
                    self.assertEqual(schema, expected_schema)

                elif test_obj is test_boolean:
                    schema = schema_reader._get_object_schema(test_obj)
                    expected_schema["type"] = "boolean"
                    self.assertEqual(schema, expected_schema)

                elif test_obj is test_string:
                    schema = schema_reader._get_object_schema(test_obj)
                    expected_schema["type"] = "string"
                    self.assertEqual(schema, expected_schema)

                elif test_obj is test_null:
                    schema = schema_reader._get_object_schema(test_obj)
                    expected_schema["type"] = "null"
                    self.assertEqual(schema, expected_schema)

                elif test_obj is test_enum:
                    _get_list_item_types.return_value = [str]

                    schema = schema_reader._get_object_schema(test_obj)

                    expected_schema["type"] = "enum"

                    _get_list_item_types.assert_called_once_with(test_obj)

                    self.assertEqual(schema, expected_schema)
                    
                    _get_list_item_types.reset_mock(
                        return_value=True,
                        side_effect=False
                    )

                elif test_obj is test_array:
                    schema = schema_reader._get_object_schema(test_obj)

                    expected_schema["type"] = "array"
                    expected_schema["items"] = _build_array_schema_items.return_value

                    _get_list_item_types.assert_called_once_with(test_obj)
                    _get_list_item_types.reset_mock(
                        return_value=False,
                        side_effect=False
                    )
                    
                    _build_array_schema_items.assert_called_once_with(
                        test_obj, _get_list_item_types.return_value)
                    _build_array_schema_items.reset_mock(
                        return_value=False,
                        side_effect=False
                    )

                    self.assertEqual(schema, expected_schema)

                elif test_obj is test_object:
                    schema = schema_reader._get_object_schema(test_obj)

                    _build_object_schema_properties.assert_called_once_with(test_obj)

                else:
                    with self.assertRaises(ValueError):
                        schema = schema_reader._get_object_schema(test_obj)

    @mock.patch.object(SchemaReader, "_get_object_schema")
    def test__build_object_schema_properties(self, _get_object_schema):
        test_obj = {"test1": "test1", "test2": "test2"}
        schema_reader = self.schema_reader
        props = schema_reader._build_object_schema_properties(test_obj)

        expected_props = {
            "test1": schema_reader._get_object_schema.return_value,
            "test2": schema_reader._get_object_schema.return_value
        }

        _get_object_schema.assert_has_calls(
            [mock.call(value) for value in test_obj.values()]
        )

        self.assertEqual(props, expected_props)


    @mock.patch.object(SchemaReader, "_get_object_schema")
    def test__build_array_schema_items(self, _get_object_schema):
        homo_test_obj = [3.3]
        heter_test_obj = ["test1", "test2", 2.3, 2, 3.2, 59]
        homo_list_item_types = [float]
        heter_list_item_types = [str, float, int]

        for test_obj, list_item_types in zip(
            (homo_test_obj, heter_test_obj),
            (homo_list_item_types, heter_list_item_types)
        ):
            schema_reader = self.schema_reader
            items = schema_reader._build_array_schema_items(test_obj, list_item_types)
            
            if test_obj is homo_test_obj:
                _get_object_schema.assert_called_once_with(3.3)
                self.assertEqual(items, _get_object_schema.return_value)

                _get_object_schema.reset_mock()

            elif test_obj is heter_test_obj:
                _get_object_schema.assert_has_calls(
                    [mock.call(item) for item in heter_test_obj]
                )
                self.assertEqual(
                    items,
                    {"anyOf": 
                     [_get_object_schema.return_value for item in heter_test_obj]}
                )

                _get_object_schema.reset_mock()

    def test__get_list_item_types(self):
        test_obj = ["test1", "test2", 2.3, 2, 3.2, 59]
        expected_list_item_types = [str, float, int]
        list_item_types = self.schema_reader._get_list_item_types(test_obj)
        self.assertEqual(list_item_types, expected_list_item_types)
