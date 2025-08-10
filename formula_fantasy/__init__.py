"""
F1 Fantasy Python Library

A simple Python library for fetching F1 fantasy data including driver and constructor
points, breakdowns, and statistics from race weekends.

Usage:
    from formula_fantasy import get_driver_points, get_constructor_points
    
    # Get total points for a driver in a specific round
    points = get_driver_points("VER", "15")
    
    # Get constructor points
    points = get_constructor_points("RBR", "15")
"""

__version__ = "1.0.0"
__author__ = "F1 Fantasy Data Team"

from .core import (
    get_driver_points,
    get_constructor_points,
    get_driver_breakdown,
    get_constructor_breakdown,
    get_latest_round,
    list_drivers,
    list_constructors,
    get_driver_info,
    get_constructor_info
)

__all__ = [
    "get_driver_points",
    "get_constructor_points", 
    "get_driver_breakdown",
    "get_constructor_breakdown",
    "get_latest_round",
    "list_drivers",
    "list_constructors",
    "get_driver_info",
    "get_constructor_info"
]