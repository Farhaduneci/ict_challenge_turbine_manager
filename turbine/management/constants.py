from django.db import models


class CommandChoices(models.Choices):
    FLUSH = "FLUSH"
    START = "START"
    STOP = "STOP"


class Errors:
    INVALID_COMMAND = "Invalid command!"
    ADMIN_ACCESS_REQUIRED = "You do not have admin access!"
    TURBINE_ALREADY_RUNNING = "Turbine is already running!"
    TURBINE_ALREADY_STOPPED = "Turbine is already stopped!"


class Messages:
    DATABASE_FLUSHED = "Turbine data flushed successfully."
    TURBINE_STARTED = "Turbine started successfully."
    TURBINE_STOPPED = "Turbine stopped successfully."
