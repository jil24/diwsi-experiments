import sys, os
import tomllib
import logging

# force python to load from 
#sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'src'))

import diwsi.system

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

with open(sys.argv[1], "rb") as f:
  settings = tomllib.load(f)

system_objects = {}

#for setting, value in settings['System'].items():

# setup controller device
if "controller_device_module" in settings['System']:
  module_name = settings['System']["controller_device_module"]
  module_settings = settings[module_name]
  system_objects["controller_device_module"] = diwsi.system.ControllerDeviceModule(module_name, **module_settings)
  logger.info("loading controller device module: {}".format(module_name))

# setup stage control module
if "stage_control_module" in settings['System']:
  module_name = settings['System']["stage_control_module"]
  module_settings = settings[module_name]
  system_objects["stage_control_module"] = diwsi.system.StageControlModule(module_name, device_object=system_objects["controller_device_module"], **module_settings)
  logger.info("loading stage control module: {}".format(module_name))

# interface module
if "interface_module" in settings['System']:
  module_name = settings['System']["interface_module"]
  module_settings = settings[module_name]
  system_objects["interface_module"] = diwsi.system.InterfaceModule(module_name, stage_control_object=system_objects["stage_control_module"], **module_settings)
  logger.info("loading stage control module: {}".format(module_name))
  system_objects["interface_module"].begin()