from core.parameter import ParameterSchema, IndexParameter, BoolParameter

MATERIAL_IDX = ParameterSchema(
    name="material_index",
    display_name="Матеріал",
    description="Вибір індексу матеріалу",
    parse_type=int,
    parameter_cls=IndexParameter
)

DIAMETER = ParameterSchema(
    name="diameter",
    display_name="Діаметр",
    description="Діаметр в мм",
    parse_type=float
)

LENGTH = ParameterSchema(
    name="length",
    display_name="Довжина",
    description="Довжина в мм",
    parse_type=float
)

ANGLE = ParameterSchema(
    name="angle",
    display_name="Кут",
    description="Кут в градусах",
    parse_type=float
)

SEGMENTS = ParameterSchema(
    name="segments",
    display_name="Сегменти",
    description="Кількість сегментів",
    parse_type=int
)

HAS_SALARY = ParameterSchema(
    name="has_salary",
    display_name="Заробітня плата",
    description="Чи включається заробітня плата",
    parse_type=bool,
    parameter_cls=BoolParameter
)
