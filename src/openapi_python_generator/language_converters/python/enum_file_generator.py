from openapi_python_generator.models import EnumFiles
from typing import Optional

def generate_enum_file(
    enum_path: str
) -> Optional[EnumFiles] :

 
    """
    Generate the API SDK.
    """
    try:
        # read the enum file
        with open(enum_path, "r") as file:
            content = file.read()
            file_name = enum_path.split("/")[-1].split(".")[0]
            # extract classes names in the file
            classes = [line.split(" ")[1].split("(")[0] for line in content.split("\n") if "class" in line]

            return EnumFiles(
                file_name=file_name,
                content=content,
                classes=classes
            
            )
        return None
    except Exception as e:
        return None