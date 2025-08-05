# Wiz Smart Bulb MCP Server

An MCP server for controlling Wiz smart lights/bulbs via UDP commands.

## Features

- Turn on the light
- Turn off the light
- Set warm white color
- Set daylight color
- Change brightness
- Check current light status

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables (optional):
```bash
export WIZ_BULB_IP="192.168.1.XX"
export WIZ_BULB_PORT="38899"
```

## Usage

### Run the MCP Server

```bash
python wiz_bulb_mcp.py
```

### Available Tools

The server provides the following MCP tools:

1. **turn_on_bulb()** - Turn on the light
2. **turn_off_bulb()** - Turn off the light
3. **set_warm_white(dimming: int = 100)** - Set warm white color (always sets warm white)
4. **set_daylight(dimming: int = 100)** - Set daylight color (always sets daylight)
5. **adjust_brightness(brightness_percent: int)** - Adjust brightness while maintaining current color scene
6. **get_bulb_status()** - Check current light status (on/off, brightness, color mode)
7. **get_bulb_info()** - Get light configuration information


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