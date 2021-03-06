#!/usr/bin/env python

import re
import os
import sys
import os.path
import unittest
import shutil

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

import generators.libretro.libretroControllers as libretroControllers
import controllersConfig as controllersConfig
shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/retroarchcustom.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/retroarchcustom.cfg.origin")))

shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../resources/es_input.cfg.origin")), \
                os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_input.cfg")))

# Injecting test recalbox.conf
libretroControllers.settingsRoot = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp"))
# Injecting test es_input
controllersConfig.esInputs = os.path.abspath(os.path.join(os.path.dirname(__file__), "tmp/es_input.cfg"))

# Test objects
basicInputs1 = {'a': controllersConfig.Input("a", "button", "10", "1")}
basicController1 = controllersConfig.Controller("contr1", "joypad", "GUID1", "0", "Joypad1RealName", basicInputs1)
PS3UUID = "060000004c0500006802000000010000"
GPIOUUID = "15000000010000000100000000010000"


class TestLibretroController(unittest.TestCase):
    def test_generate_simple_controller(self):
        config = libretroControllers.generateControllerConfig(basicController1)
        self.assertTrue('input_device = "Joypad1RealName"' in config)
        self.assertTrue('input_driver = "udev"' in config)
        self.assertTrue('input_a_btn = 10' in config)

    def test_generate_ps3_controller_buttons(self):
        controllers = controllersConfig.loadControllerConfig(0, PS3UUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = libretroControllers.generateControllerConfig(controllers["1"])
        self.assertTrue('input_device = "p1controller"' in config)
        self.assertTrue('input_driver = "udev"' in config)
        self.assertTrue('input_select_btn = 0' in config)
        self.assertTrue('input_a_btn = 13' in config)
        self.assertTrue('input_start_btn = 3' in config)
        self.assertTrue('input_b_btn = 14' in config)
        self.assertTrue('input_l2_btn = 8' in config)
        self.assertTrue('input_r_btn = 11' in config)
        self.assertTrue('input_y_btn = 15' in config)
        self.assertTrue('input_x_btn = 12' in config)
        self.assertTrue('input_l_btn = 10' in config)

    def test_generate_ps3_controller_joysticks(self):
        controllers = controllersConfig.loadControllerConfig(0, PS3UUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = libretroControllers.generateControllerConfig(controllers["1"])
        self.assertTrue('input_device = "p1controller"' in config)
        self.assertTrue('input_driver = "udev"' in config)
        self.assertTrue('input_l_y_plus_axis = +1' in config)
        self.assertTrue('input_l_y_minus_axis = -1' in config)
        self.assertTrue('input_l_x_plus_axis = +0' in config)
        self.assertTrue('input_l_x_minus_axis = -0' in config)

    def test_generate_joystick_as_directions(self):
        controllers = controllersConfig.loadControllerConfig(0, GPIOUUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = libretroControllers.generateControllerConfig(controllers["1"])
        self.assertTrue('input_device = "p1controller"' in config)
        self.assertTrue('input_up_axis = -1' in config)
        self.assertTrue('input_down_axis = +1' in config)
        self.assertTrue('input_right_axis = +0' in config)
        self.assertTrue('input_left_axis = -0' in config)

    def test_generate_specials(self):
        controllers = controllersConfig.loadControllerConfig(0, GPIOUUID, "p1controller", -1, 0, "p2controller", -1, 0,
                                                             "p3controller", -1, 0, "p4controller")
        config = libretroControllers.generateControllerConfig(controllers["1"])
        print config
        self.assertTrue('input_exit_emulator_btn = 7' in config)


class TestLibretroGeneratorGetValue(unittest.TestCase):
    def test_on_button(self):
        val = libretroControllers.getConfigValue(controllersConfig.Input("a", "button", "10", "1"))
        self.assertEquals("10", val)

    def test_on_axis(self):
        val = libretroControllers.getConfigValue(controllersConfig.Input("down", "axis", "10", "1"))
        self.assertEquals("+10", val)
        val = libretroControllers.getConfigValue(controllersConfig.Input("down", "axis", "10", "-1"))
        self.assertEquals("-10", val)

    def test_on_hat(self):
        val = libretroControllers.getConfigValue(controllersConfig.Input("down", "hat", "2", "1"))
        self.assertEquals("h2up", val)
        val = libretroControllers.getConfigValue(controllersConfig.Input("down", "hat", "3", "8"))
        self.assertEquals("h3left", val)

    def test_on_key(self):
        val = libretroControllers.getConfigValue(controllersConfig.Input("down", "key", "2", "1"))
        self.assertEquals("2", val)
        val = libretroControllers.getConfigValue(controllersConfig.Input("down", "key", "3", "8"))
        self.assertEquals("3", val)


if __name__ == '__main__':
    unittest.main()
