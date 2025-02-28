[  !["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/notenough)

If you find this tool helpful, consider supporting the development by buying me a coffee! ☕

# Game Automation

An automation tool for managing game tasks efficiently, including secretary management, alliance donations, and scheduled events.

## Prerequisites

Before setting up, ensure you have:


1. A device with USB debugging enabled
2. ADB (Android Debug Bridge) installed on your computer
3. Python 3.8 or higher installed

## Quick Start


1. Clone this repository
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Connect your device via USB and enable USB debugging
4. Run the automation:

   ```bash
   python cli.py auto  # For full automation
   # OR
   python cli.py routine <routine_name>  # For specific routine
   ```

## Features

* Automated secretary management with alliance tag filtering
* Resource collection - Upcoming (VIP12 exclusive)
* Alliance donation handling
* Automatic help button detection
* Smart delay system with configurable multiplier
* Robust error handling and recovery
* Automatic cleanup of temporary files
* Log rotation with size limits
* Alliance whitelist filtering
* Scheduled event automation
* Map exchange automation
* Dig checking system

## Setup


1. Install Python 3.8 or higher
2. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```
3. Install Tesseract OCR:
   * **Windows**:

     
     1. Download and install [Tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki)
     2. Add Tesseract to your PATH (default: `C:\Program Files\Tesseract-OCR`)
     3. Download additional language data files:
        * [Chinese (Simplified)](https://github.com/tesseract-ocr/tessdata/raw/main/chi_sim.traineddata)
        * [Korean](https://github.com/tesseract-ocr/tessdata/raw/main/kor.traineddata)
        * [Japanese](https://github.com/tesseract-ocr/tessdata/raw/main/jpn.traineddata)
        * [Russian](https://github.com/tesseract-ocr/tessdata/raw/main/rus.traineddata)
        * [Arabic](https://github.com/tesseract-ocr/tessdata/raw/main/ara.traineddata)
        * [Thai](https://github.com/tesseract-ocr/tessdata/raw/main/tha.traineddata)
     4. Place downloaded .traineddata files in `C:\Program Files\Tesseract-OCR\tessdata`
   * **Linux**:

     ```bash
     sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim tesseract-ocr-kor tesseract-ocr-jpn tesseract-ocr-rus tesseract-ocr-ara tesseract-ocr-tha
     ```
4. Connect your device via ADB
5. Configure your settings in `config/game_config.json` and `config/automation.json`
6. Create a `.env` file in the root directory with your Discord webhook:

   ```
   DISCORD_WEBHOOK_URL=your_webhook_url_here
   ```

## Configuration

### Game Config (`config/game_config.json`)

```json
{
  "package_name": "com.example.game",
  "sleep_multiplier": 1.0,        // Global multiplier for all delays
  "debug_mode": false,            // Enable/disable debug logging
  "max_retries": 3,              // Maximum retry attempts for actions
  "retry_delay": 1.0,            // Delay between retries
  "collect_resources_interval": 300,  // Seconds between resource collections
  "donate_alliance_interval": null,   // Seconds between alliance donations (null to disable)
  "screenshot_quality": 100,      // Quality of captured screenshots
  "match_threshold": 0.8,         // Confidence threshold for template matching
  "alliance_whitelist": ["TAG1", "TAG2"],  // Alliance tags to whitelist (case-sensitive)
  "timings": {
    "menu_animation": 1.5         // Delay for menu animations
  },
  "discord": {
    "dig_notification": {
      "content": "🏴‍☠️ **Dig Notification!**\nA new dig location has been discovered on the map.",
      "embed_color": "0xFF0000",
      "embed_title": "Action Required",
      "embed_value": "Check the map for new dig locations!"
    }
  }
}
```

> **Important Note About Alliance Tags**: Due to OCR limitations, similar-looking characters in alliance tags (like 'S' vs 's', 'O' vs '0') may be misinterpreted. To avoid issues:
>
> * Only include one case version of similar-looking characters (e.g., use "STAG" instead of both "STAG" and "stag")
> * Test your whitelist with the debug mode enabled to ensure proper tag recognition
> * Consider using distinctive characters when possible

### Additional Configuration Tips


1. **Performance Tuning**:
   * Adjust `sleep_multiplier` based on your device's performance
   * Lower values speed up automation but may cause instability
   * Higher values increase reliability but slow down operations
2. **Resource Management**:
   * Set `collect_resources_interval` based on your resource generation speed
   * Use `donate_alliance_interval: null` to disable alliance donations
   * Configure `screenshot_quality` based on your storage constraints (lower = smaller files)
3. **Error Recovery**:
   * Increase `max_retries` for less stable connections
   * Adjust `retry_delay` for slower devices
   * Set `match_threshold` lower for more lenient image matching
4. **Discord Integration**:
   * Customize notification messages in the discord section
   * Use markdown formatting in notification content
   * Add multiple webhook URLs for different notification types

### Automation Config (`config/automation.json`)

This file controls all automation routines and their scheduling. Each routine can be configured with:

* `handler`: The Python class that implements the routine
* `interval`: Time in seconds between routine executions (for time-based checks)
* `schedule`: Specific schedule for routines that run at fixed times (for scheduled events)

Example:

```json
{
  "time_checks": {
    "routine_name": {
      "handler": "src.automation.routines.RoutineClass",
      "interval": 300
    }
  },
  "scheduled_events": {
    "event_name": {
      "handler": "src.automation.routines.EventClass",
      "schedule": {
        "day": "sunday",
        "time": "01:50"
      }
    }
  }
}
```

## Available Routines

The following routines are available for automation:


1. **Secretary Management** (`secretary`)
   * Handles secretary-related tasks
   * Interval: 30 seconds
   * Filters alliance tags and manages resources
2. **Alliance Donations** (`donate`)
   * Manages alliance donations
   * Interval: 25000 seconds
   * Automatically handles resource distribution
3. **Help Detection** (`help`)
   * Monitors and clicks help buttons
   * Interval: 10 seconds
   * Provides alliance support
4. **Map Exchange** (`mapExchange`)
   * Handles map exchange activities
   * Interval: 300 seconds
   * Manages map-related resources
5. **Dig Checking** (`dig`)
   * Monitors for dig opportunities
   * Interval: 10 seconds
   * Automates dig-related activities
6. **Cleanup** (`cleanup`)
   * Manages temporary files and resources
   * Interval: 3600 seconds (1 hour)
   * Prevents disk space issues
7. **Reset** (`reset`)
   * Handles game reset procedures
   * Interval: 2700 seconds
   * Maintains game state
8. **Weekly Reset** (`weekly_reset`)
   * Scheduled event for weekly resets
   * Runs every Sunday at 01:50
   * Handles weekly maintenance tasks
9. **Weekly Recording** (`weekly_recording`)
   * Scheduled event for weekly video recording
   * Runs every Saturday at 9:55 PM Eastern Time
   * Records game activity for 5 minutes

### Time Zone Configuration

All scheduled events in `automation.json` use UTC time internally. Here's how to convert common time zones:

* Eastern Time (ET) to UTC: Add 4 hours during EDT (March-November) or 5 hours during EST (November-March)
* Pacific Time (PT) to UTC: Add 7 hours during PDT or 8 hours during PST
* Central European Time (CET) to UTC: Subtract 1 hour during winter or 2 hours during summer

Examples:
* 9:55 PM ET = 01:55 UTC (next day)
* 8:00 AM PT = 15:00 UTC
* 2:00 PM CET = 13:00 UTC (winter) or 12:00 UTC (summer)

When configuring scheduled events in `automation.json`, always use UTC time format.

### Managing Routines

To enable or disable routines:


1. Open `config/automation.json`
2. To disable a routine:
   * Remove its entry from the configuration
   * Or set its interval to `null`
3. To enable a routine:
   * Add its configuration under `time_checks` or `scheduled_events`
   * Specify the handler path and desired interval/schedule

### Positions Config (`config/positions.json`)

Contains all screen coordinates for UI elements. Coordinates are specified as `[x, y]` pairs.

### Templates

Place template images in `config/templates/` directory:

* `help.png`: Template for help button detection
* Other game-specific templates

## Usage

Run the automation:

```bash
python cli.py
```

## Directory Structure

```
├── config/
│   ├── game_config.json     # Main configuration
│   ├── automation.json      # Routine configuration
│   ├── positions.json       # Screen coordinates
│   └── templates/           # Template images
├── src/
│   ├── core/               # Core functionality
│   ├── game/               # Game-specific logic
│   ├── automation/         # Automation routines
│   │   └── routines/      # Individual routine implementations
│   └── utils/             # Utility functions
├── logs/                   # Log files (rotated, max 10MB each)
└── tmp/                    # Temporary files (auto-cleaned)
```

## Logging

Logs are stored in the `logs/` directory with automatic rotation:

* Maximum file size: 10MB
* Keeps last 5 backup files
* Automatically rotates when size limit is reached
* Includes detailed routine execution information

## Cleanup

The automation includes automatic cleanup features:

* Temporary files older than 24 hours are removed
* Device screenshots are cleaned up periodically
* Cleanup runs every hour during automation
* Log files are automatically rotated when size limits are reached

## Error Handling

The automation includes robust error handling:

* Automatic recovery from disconnections
* Smart retries for failed actions
* Comprehensive logging for debugging
* Routine-specific error recovery mechanisms

## Troubleshooting

### Common Issues


1. **Device Not Detected**
   * Ensure USB debugging is enabled in developer options
   * Try a different USB cable or port
   * Run `adb devices` to verify device connection
   * Restart ADB server with:

     ```bash
     adb kill-server
     adb start-server
     ```
2. **OCR Recognition Issues**
   * Verify Tesseract is properly installed and in PATH
   * Check language data files are in correct directory
   * Try adjusting game's text size/resolution
   * Enable debug mode to see OCR results in logs
3. **Automation Stops Unexpectedly**
   * Check logs for error messages
   * Verify device screen timeout is disabled
   * Ensure stable internet connection
   * Check if game has been updated
   * Verify template images match current game version
4. **Performance Issues**
   * Lower screenshot quality in config
   * Increase sleep multiplier
   * Close background apps on device
   * Clear game and device cache
   * Check device temperature

### Debug Mode

To enable detailed logging:


1. Set `debug_mode: true` in `game_config.json`
2. Run with `python cli.py auto --debug`
3. Check `logs/app.log` for detailed information

### Support

If you encounter issues:


1. Check the troubleshooting guide above
2. Enable debug mode and check logs
3. Open an issue with:
   * Full error message
   * Debug logs
   * Device information
   * Configuration files (without sensitive data)

## Contributing


1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

This project is licensed under the MIT License.

### Alliance Whitelist Configuration

The automation system uses OCR (Optical Character Recognition) to read alliance tags. Due to OCR limitations, configure your whitelist carefully:


1. Edit `config/config.json` control list section:

   ```json
   "control_list": {
     "whitelist": {
       "alliance": [
         "TAG1",
         "TAG2"
       ]
     }
   }
   ```
2. Important whitelist guidelines:
   * Case-sensitive: "TAG" and "tag" are different
   * Avoid similar-looking characters (e.g., 'O' vs '0', 'I' vs 'l')
   * Test your whitelist with debug mode enabled
   * Use consistent casing within your alliance

### Automation Configuration

Configure routines in `config/automation.json`:


1. Time-based checks: - UPCOMING

   ```json
   "time_checks": {
     "secretary": {
       "handler": "src.automation.routines.secretary.SecretaryRoutine",
       "interval": 40
     }
   }
   ```
2. To disable a routine:
   * Remove its entry completely, or
   * Set interval to null:

   ```json
   "collect_resources": {
     "handler": "src.automation.routines.collectResources.CollectResourcesRoutine",
     "interval": null  // Disabled routine
   }
   ```
3. Default Intervals:
   * secretary: 40 seconds
   * help: 5 seconds
   * dig: 5 seconds
   * mapExchange: 300 seconds
   * alliance_gifts: 5000 seconds
   * collect_resources: 10000 seconds (VIP12 only)
   * cleanup: 3600 seconds
4. Scheduled events:

   ```json
   "scheduled_events": {
     "weekly_reset": {
       "handler": "src.automation.routines.weeklyReset.WeeklyResetRoutine",
       "schedule": {
         "day": "monday",
         "time": "01:50"
       }
     }
   }
   ```

> **Note**: Setting an interval to `null` is the recommended way to disable routines while maintaining their configuration for future use.


