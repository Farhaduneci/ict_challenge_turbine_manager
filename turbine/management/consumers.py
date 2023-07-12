import asyncio
import json
from functools import wraps

from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework.exceptions import PermissionDenied, ValidationError

from config.settings.base import TURBINE_DELAY

from .constants import CommandChoices, Errors, Messages
from .serializers import CommandSerializer
from .services import flush_turbine_data, generate_and_save_turbine_data


def requires_admin_access(func):
    """A decorator that checks if the user is an admin.

    If the user is not an admin, the function is not called and a special error
    message is sent to the client.
    """

    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        if not self.scope["user"].is_superuser:
            raise PermissionDenied(Errors.ADMIN_ACCESS_REQUIRED)

        return await func(self, *args, **kwargs)

    return wrapper


class TurbineConsumer(AsyncWebsocketConsumer):
    """A consumer that sends turbine data to the client periodically.

    Also acts as the management interface for the turbine.
    """

    def __init__(self, turbine_state: bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.TURBINE_STATE = turbine_state

    async def send_periodically(self):
        while self.TURBINE_STATE:
            turbine_data = await generate_and_save_turbine_data()
            await self.send(text_data=json.dumps({"data": turbine_data}))

            await asyncio.sleep(TURBINE_DELAY)

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        try:
            serializer = CommandSerializer(data={"command": text_data})
            serializer.is_valid(raise_exception=True)

            await self.command_dispatcher(command=serializer.validated_data["command"])

        except ValidationError:
            await self.send(
                text_data=json.dumps(
                    {
                        "error": Errors.INVALID_COMMAND,
                        "commands": [command.name for command in CommandChoices],
                    }
                )
            )

    async def command_dispatcher(self, *, command: str):
        """Call the appropriate method based on the command received."""

        command_map = {
            CommandChoices.FLUSH.name: self.flush_turbine_data,
            CommandChoices.START.name: self.start_turbine,
            CommandChoices.STOP.name: self.stop_turbine,
        }

        try:
            response = await command_map[command]()
            await self.send(text_data=json.dumps({"message": response}))

        except PermissionDenied as ex:
            await self.send(text_data=json.dumps({"error": ex.detail}))

    @requires_admin_access
    async def flush_turbine_data(self):
        await flush_turbine_data()

        return {"message": Messages.DATABASE_FLUSHED}

    @requires_admin_access
    async def start_turbine(self):
        if self.TURBINE_STATE:
            return {"error": Errors.TURBINE_ALREADY_RUNNING}

        self.TURBINE_STATE = True
        asyncio.create_task(self.send_periodically())

        return {"message": Messages.TURBINE_STARTED}

    @requires_admin_access
    async def stop_turbine(self):
        if not self.TURBINE_STATE:
            return {"error": Errors.TURBINE_ALREADY_STOPPED}

        self.TURBINE_STATE = False
        return {"message": Messages.TURBINE_STOPPED}
