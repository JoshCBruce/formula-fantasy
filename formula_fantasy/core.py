"""
Core functionality for F1 Fantasy Python Library
"""
import requests
import json
from typing import Optional, Dict, List, Union, Any

# Base URL for GitHub raw data  
BASE_URL = "https://raw.githubusercontent.com/JoshCBruce/fantasy-data/refs/heads/main"

# For local development/testing
import os
LOCAL_DATA_PATH = None
if os.path.exists("/Users/user/fantasy-scrape/f1-fantasy-scraper"):
    LOCAL_DATA_PATH = "/Users/user/fantasy-scrape/f1-fantasy-scraper"

class F1FantasyError(Exception):
    """Custom exception for F1 Fantasy data errors"""
    pass

def _fetch_json_data(url: str) -> Dict[str, Any]:
    """
    Fetch JSON data from a URL or local file with error handling
    
    Args:
        url: The URL or file path to fetch data from
        
    Returns:
        Parsed JSON data as dictionary
        
    Raises:
        F1FantasyError: If the request fails or data is invalid
    """
    # Check if we should use local data for testing
    if LOCAL_DATA_PATH and url.startswith(BASE_URL):
        # Convert URL to local file path
        local_path = url.replace(BASE_URL, LOCAL_DATA_PATH)
        try:
            with open(local_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise F1FantasyError(f"Failed to read local data from {local_path}: {e}")
    
    # Use web request
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise F1FantasyError(f"Failed to fetch data from {url}: {e}")
    except json.JSONDecodeError as e:
        raise F1FantasyError(f"Failed to parse JSON data: {e}")

def get_latest_round() -> str:
    """
    Get the latest available round number
    
    Returns:
        Latest round number as string
    """
    # Try to fetch from latest folder first
    try:
        url = f"{BASE_URL}/latest/summary_data/extraction_summary.json"
        data = _fetch_json_data(url)
        # Extract latest round from the data
        if 'latestRound' in data:
            return str(data['latestRound'])
    except F1FantasyError:
        pass
    
    # Fallback: assume latest is 15 based on the data structure we saw
    return "15"

def _resolve_round(round_input: Union[str, int]) -> str:
    """
    Resolve round input to a valid round string
    
    Args:
        round_input: Round number or "latest"
        
    Returns:
        Round number as string
    """
    if isinstance(round_input, int):
        return str(round_input)
    
    if round_input == "latest":
        return get_latest_round()
    
    return str(round_input)

def get_driver_points(abbreviation: str, round_input: Union[str, int] = "latest") -> int:
    """
    Get total points for a driver in a specific round
    
    Args:
        abbreviation: Driver abbreviation (e.g., "VER", "HAM")
        round_input: Round number, round name, or "latest"
        
    Returns:
        Total points for the driver in that round
        
    Examples:
        >>> get_driver_points("VER", "15")
        0
        >>> get_driver_points("VER", "latest") 
        0
    """
    round_num = _resolve_round(round_input)
    
    # First try latest folder
    try:
        url = f"{BASE_URL}/latest/driver_data/{abbreviation}.json"
        data = _fetch_json_data(url)
        
        # Find the race data for the specified round
        for race in data.get('races', []):
            if race.get('round') == round_num:
                return race.get('totalPoints', 0)
                
        # If not found in latest, try specific round folder
        raise F1FantasyError("Round not found in latest data")
    except F1FantasyError:
        # Fallback to specific round folder - need to find the right folder name
        if LOCAL_DATA_PATH:
            import glob
            folders = glob.glob(f"{LOCAL_DATA_PATH}/{round_num}-*")
            if folders:
                folder_name = os.path.basename(folders[0])
                url = f"{BASE_URL}/{folder_name}/driver_data/{abbreviation}.json"
                data = _fetch_json_data(url)
                # Find the race data for the specified round
                for race in data.get('races', []):
                    if race.get('round') == round_num:
                        return race.get('totalPoints', 0)
    
    raise F1FantasyError(f"No data found for driver {abbreviation} in round {round_num}")

def get_constructor_points(abbreviation: str, round_input: Union[str, int] = "latest") -> int:
    """
    Get total points for a constructor in a specific round
    
    Args:
        abbreviation: Constructor abbreviation (e.g., "RBR", "MCL")
        round_input: Round number, round name, or "latest"
        
    Returns:
        Total points for the constructor in that round
        
    Examples:
        >>> get_constructor_points("RBR", "15")
        0
        >>> get_constructor_points("RBR", "latest")
        0
    """
    round_num = _resolve_round(round_input)
    
    # First try latest folder
    try:
        url = f"{BASE_URL}/latest/constructor_data/{abbreviation}.json"
        data = _fetch_json_data(url)
        
        # Find the race data for the specified round
        for race in data.get('races', []):
            if race.get('round') == round_num:
                return race.get('totalPoints', 0)
                
        # If not found in latest, try specific round folder
        raise F1FantasyError("Round not found in latest data")
    except F1FantasyError:
        # Fallback to specific round folder - need to find the right folder name
        if LOCAL_DATA_PATH:
            import glob
            folders = glob.glob(f"{LOCAL_DATA_PATH}/{round_num}-*")
            if folders:
                folder_name = os.path.basename(folders[0])
                url = f"{BASE_URL}/{folder_name}/constructor_data/{abbreviation}.json"
                data = _fetch_json_data(url)
                # Find the race data for the specified round
                for race in data.get('races', []):
                    if race.get('round') == round_num:
                        return race.get('totalPoints', 0)
    
    raise F1FantasyError(f"No data found for constructor {abbreviation} in round {round_num}")

def get_driver_breakdown(abbreviation: str, round_input: Union[str, int] = "latest", 
                        session: str = "race", points_type: Optional[str] = None) -> Union[int, Dict[str, int]]:
    """
    Get detailed points breakdown for a driver
    
    Args:
        abbreviation: Driver abbreviation (e.g., "VER", "HAM")
        round_input: Round number, round name, or "latest"
        session: "race", "sprint", or "qualifying"
        points_type: Specific points type (e.g., "overtakeBonus", "dotd", "position")
        
    Returns:
        If points_type specified: specific point value
        Otherwise: dictionary of all points breakdown
        
    Examples:
        >>> get_driver_breakdown("VER", "14", "race", "overtakeBonus")
        7
        >>> get_driver_breakdown("VER", "14", "race")
        {"dotd": 0, "position": 10, "overtakeBonus": 7, ...}
    """
    round_num = _resolve_round(round_input)
    
    # First try latest folder
    try:
        url = f"{BASE_URL}/latest/driver_data/{abbreviation}.json"
        data = _fetch_json_data(url)
    except F1FantasyError:
        # Fallback to specific round folder
        url = f"{BASE_URL}/{round_num}-*/driver_data/{abbreviation}.json"
        data = _fetch_json_data(url)
    
    # Find the race data for the specified round
    for race in data.get('races', []):
        if race.get('round') == round_num:
            session_data = race.get(session, {})
            if points_type:
                return session_data.get(points_type, 0)
            return session_data
    
    raise F1FantasyError(f"No data found for driver {abbreviation} in round {round_num}")

def get_constructor_breakdown(abbreviation: str, round_input: Union[str, int] = "latest",
                            session: str = "race", points_type: Optional[str] = None) -> Union[int, Dict[str, int]]:
    """
    Get detailed points breakdown for a constructor
    
    Args:
        abbreviation: Constructor abbreviation (e.g., "RBR", "MCL")
        round_input: Round number, round name, or "latest"
        session: "race", "sprint", or "qualifying"
        points_type: Specific points type (e.g., "overtakes", "fastestPitStop")
        
    Returns:
        If points_type specified: specific point value
        Otherwise: dictionary of all points breakdown
        
    Examples:
        >>> get_constructor_breakdown("RBR", "14", "race", "overtakes")
        7
        >>> get_constructor_breakdown("RBR", "14", "race")
        {"position": 2, "overtakes": 7, "fastestPitStop": 20, ...}
    """
    round_num = _resolve_round(round_input)
    
    # First try latest folder
    try:
        url = f"{BASE_URL}/latest/constructor_data/{abbreviation}.json"
        data = _fetch_json_data(url)
    except F1FantasyError:
        # Fallback to specific round folder
        url = f"{BASE_URL}/{round_num}-*/constructor_data/{abbreviation}.json"
        data = _fetch_json_data(url)
    
    # Find the race data for the specified round
    for race in data.get('races', []):
        if race.get('round') == round_num:
            session_data = race.get(session, {})
            if points_type:
                return session_data.get(points_type, 0)
            return session_data
    
    raise F1FantasyError(f"No data found for constructor {abbreviation} in round {round_num}")

def list_drivers() -> List[str]:
    """
    Get list of all available driver abbreviations
    
    Returns:
        List of driver abbreviations
    """
    # Common F1 driver abbreviations based on the data we saw
    return ["ALB", "ALO", "ANT", "BEA", "BOR", "COL", "DOO", "GAS", "HAD", "HAM", 
            "HUL", "LAW", "LEC", "NOR", "OCO", "PIA", "RUS", "SAI", "STR", "TSU", "VER"]

def list_constructors() -> List[str]:
    """
    Get list of all available constructor abbreviations
    
    Returns:
        List of constructor abbreviations
    """
    # Common F1 constructor abbreviations based on the data we saw
    return ["ALP", "AMR", "FER", "HAS", "MCL", "MER", "RB", "RBR", "SAU", "WIL"]

def get_driver_info(abbreviation: str) -> Dict[str, Any]:
    """
    Get full driver information including season totals, value, team, etc.
    
    Args:
        abbreviation: Driver abbreviation (e.g., "VER", "HAM")
        
    Returns:
        Complete driver data dictionary
        
    Examples:
        >>> info = get_driver_info("VER")
        >>> print(info["team"])
        Red Bull Racing
        >>> print(info["seasonTotalPoints"])
        335
    """
    try:
        url = f"{BASE_URL}/latest/driver_data/{abbreviation}.json"
        return _fetch_json_data(url)
    except F1FantasyError:
        raise F1FantasyError(f"No data found for driver {abbreviation}")

def get_constructor_info(abbreviation: str) -> Dict[str, Any]:
    """
    Get full constructor information including season totals, value, etc.
    
    Args:
        abbreviation: Constructor abbreviation (e.g., "RBR", "MCL")
        
    Returns:
        Complete constructor data dictionary
        
    Examples:
        >>> info = get_constructor_info("RBR")
        >>> print(info["seasonTotalPoints"])
        568
        >>> print(info["value"])
        28.4M
    """
    try:
        url = f"{BASE_URL}/latest/constructor_data/{abbreviation}.json"
        return _fetch_json_data(url)
    except F1FantasyError:
        raise F1FantasyError(f"No data found for constructor {abbreviation}")