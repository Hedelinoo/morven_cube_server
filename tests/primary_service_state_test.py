from morven_cube_server.helper.kociemba_extend import Kociemba
from morven_cube_server.models.end_of_program_report import EndOfProgramReport
from morven_cube_server.models.program import Program
from morven_cube_server.models.program_settings import ArduinoConstants
from morven_cube_server.services.primary_service_state import PrimaryArduinoService


async def test_connect():
    service = PrimaryArduinoService()
    await service.connect("/COM5", 115200)


async def test_send_program():
    service = PrimaryArduinoService()
    await service.connect("/COM5", 115200)
    await service.send_program(
        program=Program(
            start_pattern="",
            arduino_constants=ArduinoConstants(
                acc100=20000,
                acc50=20000,
                cc100=1,
                cc50=1,
                is_double=True,
                max_speed=2000
            ),
            id=0,
            instructions=Kociemba.solve(
                "DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD"),

        )
    )
    async for data in service.handle_received_updates():
        if type(data) is EndOfProgramReport:
            assert(data.program_id
            =="0")
            break
