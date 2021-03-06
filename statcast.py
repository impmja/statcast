import screen_reader
from mode import Mode
from screen_reader import ScreenReader
import time
from lifxlan import LifxLAN
from plugins.hp_handler import HpHandler
from plugins.energy_handler import EnergyHandler
from plugins.combo_points_handler import ComboPointsHandler
from plugins.rage_handler import RageHandler
from statcast_runner import StatcastRunner

MAX_CONNECTION_RETRIES = 5

lifx = LifxLAN(1)
print("Connecting...")

light = None
for i in range(MAX_CONNECTION_RETRIES):
    try:
        light = lifx.get_multizone_lights()[0]
        break
    except:
        print("Retrying...")
        time.sleep(1)

if light is None:
    raise Exception("Failed to connect to LIFX device! Please try again.")

print("Connected!")

statcast_runner = StatcastRunner(
    light,
    ScreenReader(pixel_value_to_mode_dict = {
        0: Mode.HP,
        1: Mode.COMBO_POINTS,
        2: Mode.ENERGY,
        3: Mode.RAGE
    }),
    plugins = {
        Mode.HP: HpHandler(light),
        Mode.COMBO_POINTS: ComboPointsHandler(light),
        Mode.ENERGY: EnergyHandler(light),
        Mode.RAGE: RageHandler(light)
})
statcast_runner.run()
