from typing import Optional

from openapi_pydantic import OpenAPI

from openapi_python_generator.language_converters.python import common
from openapi_python_generator.language_converters.python.api_config_generator import (
    generate_api_config,
)
from openapi_python_generator.language_converters.python.model_generator import (
    generate_models,
)
from openapi_python_generator.language_converters.python.service_generator import (
    generate_services,
)
from openapi_python_generator.language_converters.python.service_class_generator import (
    generate_class_services,
)
from openapi_python_generator.language_converters.python.rest_client_generator import (
    generate_rest_client,
)
from openapi_python_generator.language_converters.python.enum_file_generator import generate_enum_file
from openapi_python_generator.language_converters.python.sdk_generator import generate_sdk
from openapi_python_generator.models import ConversionResult
from openapi_python_generator.models import LibraryConfig


def generator(
    data: OpenAPI,
    library_config: LibraryConfig,
    env_token_name: Optional[str] = None,
    use_orjson: bool = False,
    use_class: bool = False,
    enum_path: Optional[tuple[str]] = None,
    custom_template_path: Optional[str] = None,
) -> ConversionResult:
    """
    Generate Python code from an OpenAPI 3.0 specification.
    """

    common.set_use_orjson(use_orjson)
    common.set_custom_template_path(custom_template_path)

    if data.components is not None:
        models = generate_models(data.components)
    else:
        models = []

    if data.paths is not None:
        services = generate_services(data.paths, library_config) if not use_class else generate_class_services(data.paths, library_config)
    else:
        services = []

    api_config = generate_api_config(data, env_token_name)

    enum_classes = []
    if enum_path is not None:
        enum_files = [generate_enum_file(path) for path in enum_path]
        for enum in enum_files:
            if enum is not None:
                enum_classes += enum.classes 
    else:
        enum_files = []

    sdk = None
    rest_client = None
    if use_class:
        sdk = generate_sdk(data, env_token_name,  
                        classes=[ {"class_name" :service.class_name , "file_name": service.file_name} for service in services ], 
                        enum_classes=[ {"class_name" :enum , "method_name": common.camel_case_split(enum)} for enum in enum_classes])
    
        rest_client = generate_rest_client(data, library_config) 

    return ConversionResult(
        models=models,
        services=services,
        api_config=api_config,
        sdk=sdk,
        rest_client=rest_client,
        enum_files=[enum_file for enum_file in enum_files if enum_file is not None],
    )
