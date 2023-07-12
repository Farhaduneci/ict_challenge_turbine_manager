from datetime import datetime
from secrets import randbelow

from asgiref.sync import sync_to_async

from turbine.turbine_data.models import TurbineData


@sync_to_async
def create_user(**kwargs):
    return TurbineData.objects.create(**kwargs)


@sync_to_async
def flush_turbine_data():
    TurbineData.objects.all().delete()


async def generate_and_save_turbine_data():
    # The volume of fuel consumed in liters
    V = randbelow(15)

    # The temperature in degrees Celsius
    T = randbelow(1000)

    # RPS
    S = randbelow(10_000)

    # Mass of the exhaust gas in kilograms per second
    G = randbelow(1000)

    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    turbine_data = {
        "created_at": time,
        "temperature": T,
        "exhaust_mass": G,
        "fuel_consumed": V,
        "rotations_per_second": S,
    }

    await create_user(**turbine_data)

    return turbine_data
