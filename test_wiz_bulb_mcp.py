import unittest
from unittest.mock import MagicMock, patch

import wiz_bulb_mcp


class WizBulbToolTests(unittest.TestCase):
    def test_turn_on_targets_specific_bulb(self):
        controller = MagicMock()
        controller.turn_on.return_value = True
        with patch.object(wiz_bulb_mcp.bulb_manager, "get_controller", return_value=(controller, "10.0.0.2", 38899)) as mock_get:
            result = wiz_bulb_mcp.turn_on_bulb("10.0.0.2", 38899)

        mock_get.assert_called_once_with("10.0.0.2", 38899)
        controller.turn_on.assert_called_once()
        self.assertIn("10.0.0.2:38899", result)
        self.assertIn("✅", result)

    def test_set_warm_white_validates_brightness_and_targets_bulb(self):
        controller = MagicMock()
        controller.set_warm_white.return_value = True
        with patch.object(wiz_bulb_mcp.bulb_manager, "get_controller", return_value=(controller, "10.0.0.3", 39000)):
            result = wiz_bulb_mcp.set_warm_white(80, "10.0.0.3", 39000)

        controller.set_warm_white.assert_called_once_with(80)
        self.assertIn("10.0.0.3:39000", result)
        self.assertIn("80%", result)

    def test_set_warm_white_rejects_invalid_brightness(self):
        result = wiz_bulb_mcp.set_warm_white(-1)
        self.assertIn("❌", result)
        self.assertIn("between 0 and 100", result)

    def test_set_daylight_targets_bulb(self):
        controller = MagicMock()
        controller.set_daylight.return_value = True
        with patch.object(wiz_bulb_mcp.bulb_manager, "get_controller", return_value=(controller, "10.0.0.4", 38899)):
            result = wiz_bulb_mcp.set_daylight(50, "10.0.0.4", 38899)

        controller.set_daylight.assert_called_once_with(50)
        self.assertIn("10.0.0.4:38899", result)
        self.assertIn("50%", result)

    def test_get_bulb_status_formats_response(self):
        controller = MagicMock()
        controller.get_status.return_value = {
            "result": {"state": True, "dimming": 70, "sceneId": 11}
        }
        with patch.object(wiz_bulb_mcp.bulb_manager, "get_controller", return_value=(controller, "10.0.0.5", 38900)):
            result = wiz_bulb_mcp.get_bulb_status("10.0.0.5", 38900)

        controller.get_status.assert_called_once()
        self.assertIn("ON", result)
        self.assertIn("70%", result)
        self.assertIn("Warm White", result)
        self.assertIn("10.0.0.5:38900", result)

    def test_adjust_brightness_requires_light_on(self):
        controller = MagicMock()
        controller.get_status.return_value = {"result": {"state": False}}
        with patch.object(wiz_bulb_mcp.bulb_manager, "get_controller", return_value=(controller, "10.0.0.6", 38899)):
            result = wiz_bulb_mcp.adjust_brightness(40, "10.0.0.6", 38899)

        controller.get_status.assert_called_once()
        self.assertIn("currently off", result)

    def test_adjust_brightness_updates_scene(self):
        controller = MagicMock()
        controller.get_status.return_value = {
            "result": {"state": True, "sceneId": 12}
        }
        controller.send_command.return_value = {}
        with patch.object(wiz_bulb_mcp.bulb_manager, "get_controller", return_value=(controller, "10.0.0.7", 38901)):
            result = wiz_bulb_mcp.adjust_brightness(55, "10.0.0.7", 38901)

        controller.get_status.assert_called_once()
        controller.send_command.assert_called_once()
        self.assertIn("55%", result)
        self.assertIn("Daylight", result)
        self.assertIn("10.0.0.7:38901", result)

    def test_get_bulb_info_reports_active_target(self):
        controller = MagicMock()
        with patch.object(wiz_bulb_mcp.bulb_manager, "get_controller", return_value=(controller, "10.0.0.8", 38902)):
            result = wiz_bulb_mcp.get_bulb_info("10.0.0.8", 38902)

        self.assertIn("Default IP Address", result)
        self.assertIn("Active target: 10.0.0.8:38902", result)

    def test_turn_off_targets_specific_bulb(self):
        controller = MagicMock()
        controller.turn_off.return_value = True
        with patch.object(wiz_bulb_mcp.bulb_manager, "get_controller", return_value=(controller, "10.0.0.9", 38903)):
            result = wiz_bulb_mcp.turn_off_bulb("10.0.0.9", 38903)

        controller.turn_off.assert_called_once()
        self.assertIn("10.0.0.9:38903", result)
        self.assertIn("✅", result)


if __name__ == "__main__":
    unittest.main()
