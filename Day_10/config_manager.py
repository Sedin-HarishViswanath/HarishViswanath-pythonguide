"""JSON Config File Manager.

A small persistent key/value config store backed by a JSON file on disk —
the same pattern VS Code, Chrome, and Django use for settings files.
"""

import json
from pathlib import Path

DEFAULTS = {
    "theme": "light",
    "language": "en",
    "font_size": 14,
    "auto_save": True,
}


class ConfigManager:
    """Read/write a JSON config file with get/set/delete/reset operations.

    Args:
        path (str): Path to the JSON config file. Auto-created with
            DEFAULTS if it does not already exist.

    Example:
        >>> import tempfile, os
        >>> tmp = tempfile.mktemp(suffix=".json")
        >>> cm = ConfigManager(tmp)
        >>> cm.get("theme")
        'light'
        >>> cm.set("theme", "dark")
        >>> cm.get("theme")
        'dark'
        >>> cm.delete("theme")
        True
        >>> cm.delete("theme")
        False
        >>> cm.reset()
        >>> cm.get("theme")
        'light'
        >>> os.remove(tmp)
    """

    def __init__(self, path="config.json"):
        self.path = Path(path)
        self.config = self._load()

    def _load(self):
        """Load config from disk, creating it with DEFAULTS if missing.

        Returns:
            dict: The loaded (or newly created) config dictionary.
        """
        if not self.path.exists():
            self._save(DEFAULTS)
            return DEFAULTS.copy()
        with open(self.path) as f:
            return json.load(f)

    def _save(self, data):
        """Persist `data` to the config file as pretty-printed JSON.

        Args:
            data (dict): The full config dict to write out.
        """
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def get(self, key, default=None):
        """Get a config value.

        Args:
            key (str): Config key to look up.
            default: Value to return if `key` is absent. Defaults to None.

        Returns:
            The stored value, or `default` if `key` is not set.
        """
        return self.config.get(key, default)

    def set(self, key, value):
        """Set a config value and persist immediately.

        Args:
            key (str): Config key to set.
            value: Value to store under that key.
        """
        self.config[key] = value
        self._save(self.config)

    def delete(self, key) -> bool:
        """Delete a config key if it exists, persisting the change.

        Args:
            key (str): Config key to remove.

        Returns:
            bool: True if the key existed and was removed, False otherwise.
        """
        if key in self.config:
            del self.config[key]
            self._save(self.config)
            return True
        return False

    def reset(self) -> None:
        """Replace the entire config file's contents with DEFAULTS."""
        self.config = DEFAULTS.copy()
        self._save(self.config)


if __name__ == "__main__":
    cm = ConfigManager("config.json")
    print("Loaded:", cm.config)
    cm.set("font_size", 16)
    print("After set font_size=16:", cm.get("font_size"))
    print("Delete 'auto_save':", cm.delete("auto_save"))
    print("Delete 'auto_save' again:", cm.delete("auto_save"))
    cm.reset()
    print("After reset:", cm.config)