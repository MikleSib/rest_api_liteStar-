from litestar import Litestar
from litestar.openapi import OpenAPIConfig
from litestar.di import Provide

from app.api.users import UserController
from app.database.config import provide_session, on_startup


app = Litestar(
    route_handlers=[UserController],
    openapi_config=OpenAPIConfig(
        title="API",
        version="1.0.0",
        components=[],
        use_handler_docstrings=True,
    ),
    dependencies={"db_session": Provide(provide_session, sync_to_thread=False)},
    on_startup=[on_startup],
) 