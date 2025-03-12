from typing import Optional, List, Any

from openapi_pydantic import OpenAPI

from openapi_python_generator.language_converters.python.jinja_config import (
    SDK_TEMPLATE,
)

from openapi_python_generator.models import ServiceSDK
from openapi_python_generator.language_converters.python.jinja_config import (
    create_jinja_env,
)

def generate_sdk(
    data: OpenAPI, env_token_name: Optional[str] = None, classes: List[Any] = [], enum_classes: List[Any] = []
) -> ServiceSDK:

 
    """
    Generate the API SDK.
    """
    jinja_env = create_jinja_env()
    return ServiceSDK(
        file_name="sdk",
        content=jinja_env.get_template(SDK_TEMPLATE).render(
            env_token_name=env_token_name, **data.model_dump(),  classes=classes, enum_classes=enum_classes
        ),
        classes=classes, 
        enum_classes=enum_classes
    )