from aiohttp import web
from morven_cube_server.all_routes import routes
from morven_cube_server.background_tasks.update_state_with_current_sensor_data import update_state_with_current_sensor_data
from morven_cube_server.background_tasks.connect_to_arduinos import connect_to_arduinos
from morven_cube_server.states.primary_arduino_state import PrimaryArduinoState
from morven_cube_server.states.server_state import ServerState
from morven_cube_server.state_handler.background_task import add_background_task
from morven_cube_server.state_handler.provider import provide

from morven_cube_server.services.primary_arduino_service import PrimaryArduinoService
from morven_cube_server.services.secondary_arduino_service import SecondaryArduinoService
from routes import *


def run_server() -> None:
    app = web.Application()
    app.add_routes(routes=routes)

    provide(app=app, value=PrimaryArduinoService(),
            valueType=PrimaryArduinoService)
    provide(app=app, value="",
            valueType=SecondaryArduinoService)

    provide(app=app, value=ServerState(), valueType=ServerState)
    provide(app=app, value=PrimaryArduinoState(),
            valueType=PrimaryArduinoState)

    add_background_task(
        app=app,
        task_func=connect_to_arduinos
    )
    add_background_task(
        app=app,
        task_func=update_state_with_current_sensor_data,
    )

    web.run_app(app, host='localhost', port=9000)
