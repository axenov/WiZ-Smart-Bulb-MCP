#!/usr/bin/env python3
"""
Wiz Smart Bulb MCP Server
Controls Wiz smart bulbs via UDP commands
Supports multiple languages and intelligent brightness control
"""

import os
import socket
import json
from typing import Optional, Dict, Any
from fastmcp import FastMCP

# Environment variables for bulb configuration
BULB_IP = os.getenv("WIZ_BULB_IP", "192.168.0.148")
BULB_PORT = int(os.getenv("WIZ_BULB_PORT", "38899"))

class WizBulbController:
    """Controller for Wiz smart bulbs via UDP"""
    
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
    
    def send_command(self, command: dict) -> Optional[Dict[str, Any]]:
        """Send UDP command to the bulb and return response"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            
            message = json.dumps(command).encode('utf-8')
            sock.sendto(message, (self.ip, self.port))
            
            # Try to receive response
            try:
                data, addr = sock.recvfrom(1024)
                response = json.loads(data.decode())
                sock.close()
                return response
            except socket.timeout:
                sock.close()
                return None
        except Exception as e:
            print(f"Error sending command: {e}")
            return None
    
    def get_status(self) -> Optional[Dict[str, Any]]:
        """Get current bulb status"""
        command = {
            "method": "getPilot",
            "params": {}
        }
        return self.send_command(command)
    
    def turn_off(self) -> bool:
        """Turn off the bulb"""
        command = {
            "id": 1,
            "method": "setState",
            "params": {"state": False}
        }
        return self.send_command(command) is not None
    
    def set_warm_white(self, dimming: int = 100) -> bool:
        """Set bulb to warm white"""
        command = {
            "id": 1,
            "method": "setPilot",
            "params": {"sceneId": 11, "dimming": dimming}
        }
        return self.send_command(command) is not None
    
    def set_daylight(self, dimming: int = 100) -> bool:
        """Set bulb to daylight"""
        command = {
            "id": 1,
            "method": "setPilot",
            "params": {"sceneId": 12, "dimming": dimming}
        }
        return self.send_command(command) is not None

# Initialize the bulb controller
bulb_controller = WizBulbController(BULB_IP, BULB_PORT)

# Create FastMCP server
app = FastMCP("wiz-bulb-controller")

@app.tool()
def turn_off_bulb() -> str:
    """Turn off the light/lamp/bulb. Use this when user asks to turn off the light, switch off the lamp, or turn off the bulb. 
    This will completely turn off the smart light bulb."""
    success = bulb_controller.turn_off()
    if success:
        return f"✅ Light turned off successfully (IP: {BULB_IP}:{BULB_PORT})"
    else:
        return f"❌ Failed to turn off light (IP: {BULB_IP}:{BULB_PORT})"

@app.tool()
def set_warm_white(dimming: int = 100) -> str:
    """Set the light/lamp/bulb to warm white color. Use this when user asks for warm light, cozy lighting, or warm white.
    Default brightness is 100% (full brightness) unless user specifically asks for different brightness.
    
    Args:
        dimming: Brightness level (0-100). Only use values other than 100 if user specifically asks for different brightness like 'make it dimmer', 'less bright', 'brighter', etc.
    """
    if not 0 <= dimming <= 100:
        return "❌ Brightness value must be between 0 and 100"
    
    success = bulb_controller.set_warm_white(dimming)
    
    if success:
        brightness_text = f"at {dimming}% brightness" if dimming != 100 else "at full brightness"
        return f"✅ Light set to warm white {brightness_text} (IP: {BULB_IP}:{BULB_PORT})"
    else:
        return f"❌ Failed to set light to warm white (IP: {BULB_IP}:{BULB_PORT})"

@app.tool()
def set_daylight(dimming: int = 100) -> str:
    """Set the light/lamp/bulb to daylight/white color. Use this when user asks for bright light, daylight, white light, or natural lighting.
    Default brightness is 100% (full brightness) unless user specifically asks for different brightness.
    
    Args:
        dimming: Brightness level (0-100). Only use values other than 100 if user specifically asks for different brightness like 'make it dimmer', 'less bright', 'brighter', etc.
    """
    if not 0 <= dimming <= 100:
        return "❌ Brightness value must be between 0 and 100"
    
    success = bulb_controller.set_daylight(dimming)
    
    if success:
        brightness_text = f"at {dimming}% brightness" if dimming != 100 else "at full brightness"
        return f"✅ Light set to daylight {brightness_text} (IP: {BULB_IP}:{BULB_PORT})"
    else:
        return f"❌ Failed to set light to daylight (IP: {BULB_IP}:{BULB_PORT})"

@app.tool()
def get_bulb_status() -> str:
    """Get the current status of the light/lamp/bulb. Use this to check if the light is on/off, current brightness, and color mode.
    This is useful when user asks about the current state of the light."""

@app.tool()
def adjust_brightness(brightness_percent: int) -> str:
    """Adjust the brightness of the light/lamp/bulb while maintaining the current color scene.
    Use this when user asks for brightness changes like 'make it dimmer', 'less bright', 'brighter', 'set to 50%', etc.
    
    This function automatically checks the current scene and maintains it while adjusting brightness.
    
    Args:
        brightness_percent: Brightness level (0-100). Use this value directly as requested by user.
    """
    if not 0 <= brightness_percent <= 100:
        return "❌ Brightness value must be between 0 and 100"
    
    # Always check current status first
    status = bulb_controller.get_status()
    if status and status.get('result'):
        result = status['result']
        current_scene = result.get('sceneId', 11)  # Default to warm white if unknown
        current_state = result.get('state', False)
        
        if not current_state:
            return "❌ Light is currently off. Please turn it on first."
        
        # Maintain current scene while adjusting brightness
        command = {
            "id": 1,
            "method": "setPilot",
            "params": {"sceneId": current_scene, "dimming": brightness_percent}
        }
        success = bulb_controller.send_command(command) is not None
        
        if success:
            scene_name = "Warm White" if current_scene == 11 else "Daylight" if current_scene == 12 else "Unknown"
            return f"✅ Light brightness adjusted to {brightness_percent}% while maintaining {scene_name} color (IP: {BULB_IP}:{BULB_PORT})"
        else:
            return f"❌ Failed to adjust brightness (IP: {BULB_IP}:{BULB_PORT})"
    else:
        return f"❌ Could not retrieve light status to adjust brightness (IP: {BULB_IP}:{BULB_PORT})"


@app.tool()
def get_bulb_info() -> str:
    """Get information about the configured light/lamp/bulb. Use this when user asks about the light setup or configuration."""
    return f"🔍 Light Configuration:\n- IP Address: {BULB_IP}\n- Port: {BULB_PORT}\n- Available commands: turn off, warm white, daylight, check status"

if __name__ == "__main__":
    print(f"🚀 Starting Wiz Light MCP Server")
    print(f"📡 Light IP: {BULB_IP}")
    print(f"🔌 Light Port: {BULB_PORT}")
    print(f"✨ Available tools: turn_off_bulb, turn_on_bulb, set_warm_white, set_daylight, adjust_brightness, get_bulb_status, get_bulb_info")
    print(f"🌍 Multi-language support: English, German, Russian, and more")
    print(f"💡 Smart brightness: adjust_brightness() maintains current scene")
    app.run() 