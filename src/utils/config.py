"""Configuration loading and management utilities."""

import json
import os
from typing import Dict, Optional


def load_config(config_path: str = "config/settings.json") -> Dict:
    """
    Load configuration from JSON file.

    Args:
        config_path: Path to settings.json file

    Returns:
        Configuration dictionary
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in {config_path}: {e}")


def save_config(config: Dict, config_path: str = "config/settings.json") -> bool:
    """
    Save configuration to JSON file.

    Args:
        config: Configuration dictionary
        config_path: Path where to save settings.json

    Returns:
        True if successful
    """
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving config: {e}")
        return False


def get_threshold_value(
    config: Dict, threshold_name: str
) -> Optional[float]:
    """
    Get a specific threshold value from config.

    Args:
        config: Configuration dictionary
        threshold_name: Name of the threshold (e.g., 'green_to_yellow')

    Returns:
        Threshold value or None
    """
    thresholds = config.get("status_thresholds", {})
    return thresholds.get(threshold_name)
