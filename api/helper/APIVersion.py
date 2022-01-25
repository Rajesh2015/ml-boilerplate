from typing import Tuple, Optional, Union, Dict, Type, Callable

from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI
from starlette.routing import Mount


class APIVersion:

    def __init__(self, major_version, minor_version):
        self._major_version = major_version
        self._minor_version = minor_version

    def to_tuple(self) -> Tuple[int, int]:
        return self._major_version, self._minor_version

    def to_str(self) -> str:
        return f"v{self._major_version}_{self._minor_version}"


def version_app(
        app: FastAPI,
        default_api_version: APIVersion,
        exception_handlers: Optional[Dict[Union[int, Type[Exception]], Callable]],
        **kwargs
):
    app = VersionedFastAPI(
        app,
        version=default_api_version.to_str(),  # Version that appears at the top of the API docs
        default_version=default_api_version.to_tuple(),  # Version at which unversioned endpoints start to be available
        exception_handlers=exception_handlers,
        **kwargs
    )

    # Hack: Register exception handlers in all mounted subapps
    # We need this workaround because fastapi-versioning is not passing them downstream to sub-apps by default
    mounted_routes = [route for route in app.routes if isinstance(route, Mount)]

    if exception_handlers is not None:
        for mounted_route in mounted_routes:
            for exc, exc_handler in exception_handlers.items():
                mounted_route.app.add_exception_handler(exc, exc_handler)

    return app
