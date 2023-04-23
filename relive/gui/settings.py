import json

settings_json = json.dumps(
    [
        {
            "type": "title",
            "title": "Appearance"
        },
        {
            "type": "bool",
            "title": "Fullscreen",
            "desc": "Test",
            "section": "appearance",
            "key": "fullscreen"
        },
        {
            "type": "title",
            "title": "Network"
        },
        {
            "type": "string",
            "title": "Server IP address",
            "desc": "Enter here the IP of your device: e.g. 192.168.0.1",
            "section": "network",
            "key": "serverIP"
        },
        {
            "type": "title",
            "title": "MIDI"
        },
        {
            "type": "numeric",
            "title": "Looper base note",
            "desc": "Enter base note for loop control pads",
            "section": "MIDI",
            "key": "looperBaseNote"
        },
        {
            "type": "bool",
            "title": "Switch",
            "desc": "Test",
            "section": "MIDI",
            "key": "switch"
        },
        {
            "type": "title",
            "title": "Storage"
        },
        {
            "type": "options",
            "title": "Project directory",
            "desc": "Choose between application folder or user directory",
            "section": "storage",
            "options": ["application", "user"],
            "key": "userDir"
        },
        {
            "type": "path",
            "title": "Custom directory",
            "desc": "Select your own folder to manage documents",
            "section": "storage",
            "key": "CustomDir"
        }
    ]
)
