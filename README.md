# Wiz Smart Light MCP Server

A FastMCP server for controlling Wiz smart lights/bulbs via UDP commands with multi-language support and intelligent brightness control.

## Features

- Turn off the light/lamp/bulb
- Set warm white color with intelligent brightness control
- Set daylight color with intelligent brightness control
- Check current light status and settings
- Multi-language support (English, German, Russian, and more)
- Smart brightness defaults (100% unless specifically requested otherwise)
- Configurable IP and port via environment variables

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables (optional):
```bash
export WIZ_BULB_IP="192.168.0.148"
export WIZ_BULB_PORT="38899"
```

If not set, defaults to:
- IP: `192.168.0.148`
- Port: `38899`

## Usage

### Run the MCP Server

```bash
python wiz_bulb_mcp.py
```

### Available Tools

The server provides the following MCP tools:

1. **turn_on_bulb()** - Turn on the light with warm white color at full brightness
2. **turn_off_bulb()** - Turn off the light/lamp/bulb
3. **set_warm_white(dimming: int = 100)** - Set warm white color (always sets warm white)
4. **set_daylight(dimming: int = 100)** - Set daylight color (always sets daylight)
5. **adjust_brightness(brightness_percent: int)** - Adjust brightness while maintaining current color scene
6. **get_bulb_status()** - Check current light status (on/off, brightness, color mode)
7. **get_bulb_info()** - Get light configuration information

### Smart Features

- **Multi-language support**: Works with requests in English, German, Russian, and other languages
- **Intelligent brightness**: Defaults to 100% brightness unless user specifically asks for different levels
- **Clear function separation**: Color functions always set the requested color, brightness function maintains current scene
- **Natural language**: Understands various terms like "light", "lamp", "bulb", "make it brighter", "dim the lights", etc.

### Example Commands

The server translates these commands to UDP messages:

**Turn off:**
```json
{"id":1,"method":"setState","params":{"state":false}}
```

**Warm White:**
```json
{"id":1,"method":"setPilot","params":{"sceneId":11,"dimming":100}}
```

**Daylight:**
```json
{"id":1,"method":"setPilot","params":{"sceneId":12,"dimming":100}}
```

**Get Status:**
```json
{"method":"getPilot","params":{}}
```

### Example User Requests

The server understands various natural language requests:

- "Turn on the light" / "Schalte das Licht ein" / "Включи свет"
- "Turn off the light" / "Schalte das Licht aus" / "Выключи свет"
- "Make it warm white" / "Mach es warmweiß" / "Сделай теплый белый"
- "Set to daylight" / "Stelle auf Tageslicht ein" / "Поставь дневной свет"
- "Make it brighter" / "Mach es heller" / "Сделай ярче"
- "Dim the lights" / "Dimm das Licht" / "Приглуши свет"
- "Set brightness to 50%" / "Stelle Helligkeit auf 50%" / "Поставь яркость на 50%"
- "What's the current status?" / "Wie ist der aktuelle Status?" / "Какой текущий статус?"

### Smart Workflow

**For turning on/off:**
- "Turn on the light" → `turn_on_bulb()`
- "Turn off the light" → `turn_off_bulb()`

**For color changes:**
- "Make it warm white" → `set_warm_white(100)`
- "Set to daylight" → `set_daylight(100)`
- "Warm white at 30%" → `set_warm_white(30)`

**For brightness changes (maintaining current color):**
- "Make it brighter" → `get_bulb_status()` then `adjust_brightness(75)`
- "Dim the lights" → `get_bulb_status()` then `adjust_brightness(25)`
- "Set to 50%" → `get_bulb_status()` then `adjust_brightness(50)`

## Integration

This MCP server can be integrated with any MCP-compatible client or AI assistant that supports the Model Context Protocol.

## Troubleshooting

- Make sure your Wiz bulb is on the same network
- Verify the IP address is correct (you can find it in your router's admin panel)
- Check that port 38899 is not blocked by your firewall
- Ensure the bulb is powered on and connected to WiFi 