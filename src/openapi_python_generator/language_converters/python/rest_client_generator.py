from openapi_pydantic import OpenAPI

from openapi_python_generator.language_converters.python.jinja_config import (
    REST_CLIENT_TEMPLATE,
)
from openapi_python_generator.language_converters.python.jinja_config import (
    create_jinja_env,
)
from openapi_python_generator.models import RestClient
from openapi_python_generator.models import LibraryConfig

def generate_rest_client(
    data: OpenAPI, library_config: LibraryConfig
) -> RestClient:
    """
    Generate the API model.
    """
    jinja_env = create_jinja_env()
    return RestClient(
        file_name="rest_client",
        content=jinja_env.get_template(REST_CLIENT_TEMPLATE).render(
            **data.model_dump(), library_import=str(library_config.library_name), async_client=bool(library_config.include_async)
        ),
        library_import= str(library_config.library_name),
        async_client = bool(library_config.include_async),
    )
