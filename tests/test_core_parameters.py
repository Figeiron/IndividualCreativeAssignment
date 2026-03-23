import unittest
from core.parameter import Parameter, BoolParameter, ParameterSchema, MappedChoiceParameter
from UI.common.presentation.hint import OrderHint
from core.validator import RangeValidator
from core.errors import ValidationError


class TestParameters(unittest.TestCase):
    def test_parameter_basic_conversion(self):
        param = Parameter(name="age", display_name="Вік", parse=int)
        self.assertEqual(param.convert("25"), 25)
        self.assertIsInstance(param.convert("25"), int)

    def test_parameter_bool_conversion(self):
        param = BoolParameter(name="active", display_name="Активний")
        self.assertTrue(param.convert("true"))
        self.assertTrue(param.convert("yes"))
        self.assertTrue(param.convert("1"))
        self.assertTrue(param.convert("так"))
        self.assertFalse(param.convert("false"))
        self.assertFalse(param.convert("no"))
        self.assertFalse(param.convert("0"))

    def test_parameter_validation_error(self):
        param = Parameter(name="age", display_name="Вік", parse=int)
        with self.assertRaises(ValueError):
            param.convert("abc")

    def test_range_validator(self):
        validator = RangeValidator(min_val=1, max_val=10)
        # Should not raise
        validator(5)
        validator(1)
        validator(10)

        with self.assertRaises(ValidationError) as cm:
            validator(0)
        self.assertEqual(str(cm.exception), "Value must be greater than 1")

        with self.assertRaises(ValidationError) as cm:
            validator(11)
        self.assertEqual(str(cm.exception), "Value must be less than 10")

    def test_parameter_with_validators(self):
        param = Parameter(
            name="score",
            display_name="Рахунок",
            parse=int,
            validators=[RangeValidator(min_val=0, max_val=100)]
        )
        self.assertEqual(param.convert("50"), 50)

        with self.assertRaises(ValueError) as cm:
            param.convert("-5")
        self.assertIn("Value must be greater than 0", str(cm.exception))

    def test_UI_parameter_proxy(self):
        TEST_PARAM = ParameterSchema(
            name="test",
            display_name="Тест",
            description="Тестовий параметр",
            parse_type=int
        )
        print(TEST_PARAM.with_range(1,10).with_hints(additional_hints=[OrderHint(1)]).build())

    def test_mapped_choice_parameter(self):
        choices = [("Label A", 100), ("Label B", 200)]
        param = MappedChoiceParameter(
            name="test",
            display_name="Тест",
            parse=str,
            choices=choices
        )
        self.assertEqual(param.convert("Label A"), 100)
        self.assertEqual(param.convert("Label B"), 200)

        with self.assertRaises(ValueError):
            param.convert("Invalid Label")


if __name__ == '__main__':
    unittest.main()
