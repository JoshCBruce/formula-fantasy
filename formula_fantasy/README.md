# Formula Fantasy Python Library 🏎️

A simple and powerful Python library for fetching F1 Fantasy data. Get driver and constructor points, detailed breakdowns, and statistics with just one line of code.

## ✨ Features

- **Simple API**: Single command to get points data
- **Comprehensive Data**: Access all driver and constructor fantasy points
- **Detailed Breakdowns**: Get specific point categories (overtakes, DotD, fastest lap, etc.)
- **Latest Data**: Always up-to-date with the most recent race weekend
- **Historical Data**: Access data from any previous race round
- **CLI Interface**: Command-line tools for quick queries
- **Live GitHub Data**: Fetches real-time data from the official F1 Fantasy scraper

## 🚀 Quick Start

### Installation

```bash
pip install formula-fantasy
```

### Basic Usage

```python
from formula_fantasy import get_driver_points, get_constructor_points

# Get driver points for latest race
points = get_driver_points("VER")  # Max Verstappen latest race
print(f"VER latest points: {points}")

# Get constructor points for a specific round
points = get_constructor_points("RBR", "14")  # Red Bull Racing round 14
print(f"RBR round 14: {points} points")

# Get detailed breakdown
from formula_fantasy import get_driver_breakdown

breakdown = get_driver_breakdown("VER", "14", "race")
print(f"VER overtakes: {breakdown['overtakeBonus']}")

# Get specific point type
overtakes = get_driver_breakdown("VER", "14", "race", "overtakeBonus")
print(f"VER overtake bonus: {overtakes}")
```

## 📖 API Reference

### Core Functions

#### `get_driver_points(abbreviation, round="latest")`
Get total fantasy points for a driver in a specific round.

**Parameters:**
- `abbreviation` (str): Driver abbreviation ("VER", "HAM", "NOR", etc.)
- `round` (str/int): Round number or "latest" (default: "latest")

**Returns:** int - Total fantasy points

**Examples:**
```python
get_driver_points("VER", "14")     # Verstappen round 14
get_driver_points("NOR", "latest") # Norris latest round
get_driver_points("HAM", 12)       # Hamilton round 12
```

#### `get_constructor_points(abbreviation, round="latest")`
Get total fantasy points for a constructor in a specific round.

**Parameters:**
- `abbreviation` (str): Constructor abbreviation ("RBR", "MCL", "FER", etc.)
- `round` (str/int): Round number or "latest" (default: "latest")

**Returns:** int - Total fantasy points

**Examples:**
```python
get_constructor_points("RBR", "14")   # Red Bull Racing round 14
get_constructor_points("MCL", "latest") # McLaren latest round
```

#### `get_driver_breakdown(abbreviation, round="latest", session="race", points_type=None)`
Get detailed points breakdown for a driver.

**Parameters:**
- `abbreviation` (str): Driver abbreviation
- `round` (str/int): Round number or "latest" (default: "latest")
- `session` (str): "race", "sprint", or "qualifying" (default: "race")
- `points_type` (str, optional): Specific point type to get

**Returns:** 
- If `points_type` specified: int (specific point value)
- Otherwise: dict (complete breakdown)

**Available point types:**
- `"dotd"` - Driver of the Day (10 points)
- `"position"` - Position points
- `"qualifyingPosition"` - Qualifying position points
- `"fastestLap"` - Fastest lap bonus
- `"overtakeBonus"` - Overtaking points
- `"positionsGained"` - Positions gained
- `"positionsLost"` - Positions lost
- `"disqualificationPenalty"` - Penalty points

**Examples:**
```python
# Get full breakdown
breakdown = get_driver_breakdown("VER", "14", "race")
# Returns: {"dotd": 0, "position": 10, "overtakeBonus": 7, ...}

# Get specific point type
dotd_points = get_driver_breakdown("VER", "14", "race", "dotd")
# Returns: 0

# Get sprint breakdown
sprint_breakdown = get_driver_breakdown("VER", "14", "sprint")
```

#### `get_constructor_breakdown(abbreviation, round="latest", session="race", points_type=None)`
Get detailed points breakdown for a constructor.

**Parameters:** Same as `get_driver_breakdown`

**Constructor point types:**
- `"position"` - Position points
- `"overtakes"` - Total overtakes
- `"fastestPitStop"` - Fastest pit stop bonus
- `"pitStopBonus"` - Pit stop bonus
- `"worldRecordBonus"` - World record bonus
- `"positionsGained"` - Positions gained
- `"positionsLost"` - Positions lost

#### `get_driver_info(abbreviation)` / `get_constructor_info(abbreviation)`
Get complete information including season totals, value, team, etc.

**Returns:** dict - Complete data structure

**Examples:**
```python
info = get_driver_info("VER")
print(info["team"])              # "Red Bull Racing"
print(info["seasonTotalPoints"])  # 335
print(info["value"])             # "28.2M"
print(info["percentagePicked"])  # 16

constructor_info = get_constructor_info("RBR")
print(constructor_info["seasonTotalPoints"])  # 568
```

#### Utility Functions

```python
from formula_fantasy import list_drivers, list_constructors, get_latest_round

drivers = list_drivers()
# Returns: ["ALB", "ALO", "ANT", "BEA", "BOR", ...]

constructors = list_constructors() 
# Returns: ["ALP", "AMR", "FER", "HAS", "MCL", ...]

latest = get_latest_round()
# Returns: "15"
```

## 🖥️ Command Line Interface

The library includes a powerful CLI for quick data access:

### Basic Commands

```bash
# Driver points
python -m formula_fantasy.cli VER 14          # VER round 14: 11 points
python -m formula_fantasy.cli NOR latest      # NOR latest round: 0 points

# Constructor points  
python -m formula_fantasy.cli RBR 14          # RBR round 14: 39 points

# Specific breakdowns
python -m formula_fantasy.cli VER 14 race overtakeBonus  # VER overtakeBonus: 7
python -m formula_fantasy.cli RBR 14 race overtakes      # RBR overtakes: 7
```

### Advanced CLI Options

```bash
# Get full breakdown
python -m formula_fantasy.cli VER 14 --breakdown
# Shows: VER race breakdown for round 14: {dotd: 0, position: 10, ...}

# Get driver/constructor info
python -m formula_fantasy.cli VER --info
# Shows: Driver: Max Verstappen, Team: Red Bull Racing, Season: 335 points

# List available options
python -m formula_fantasy.cli --drivers        # List all drivers
python -m formula_fantasy.cli --constructors   # List all constructors
```

## 🏎️ Available Drivers & Constructors

### Drivers
```
ALB - Alexander Albon    ANT - Antonelli         BEA - Bearman
ALO - Fernando Alonso    BOR - Valtteri Bottas    COL - Colapinto  
DOO - Doohan             GAS - Pierre Gasly       HAD - Hadjar
HAM - Lewis Hamilton     HUL - Nico Hulkenberg    LAW - Liam Lawson
LEC - Charles Leclerc    NOR - Lando Norris       OCO - Esteban Ocon
PIA - Oscar Piastri      RUS - George Russell     SAI - Carlos Sainz Jr
STR - Lance Stroll       TSU - Yuki Tsunoda       VER - Max Verstappen
```

### Constructors
```
ALP - Alpine       AMR - Aston Martin    FER - Ferrari      HAS - Haas
MCL - McLaren      MER - Mercedes        RB - Racing Bulls  RBR - Red Bull Racing
SAU - Sauber       WIL - Williams
```

## 🔍 Data Structure

### Driver Data Structure
```python
{
  "driverId": "maxverstappendriver",
  "name": "maxverstappendriver", 
  "displayName": "maxverstappen",
  "abbreviation": "VER",
  "team": "Red Bull Racing",
  "position": 3,
  "value": "28.2M",
  "seasonTotalPoints": 335,
  "percentagePicked": 16,
  "isInactive": false,
  "races": [
    {
      "round": "14",
      "raceName": "Hungary",
      "totalPoints": 11,
      "race": {
        "dotd": 0,
        "position": 10,
        "qualifyingPosition": 0,
        "fastestLap": 0,
        "overtakeBonus": 7,
        "positionsGained": 0,
        "positionsLost": -1,
        "disqualificationPenalty": 0
      },
      "qualifying": {
        "position": 3,
        "disqualificationPenalty": 0
      }
    }
  ],
  "extractedAt": "2025-08-10T20:17:09.831Z"
}
```

## 🎯 Usage Examples

### Fantasy Team Analysis
```python
from formula_fantasy import *

# Analyze your fantasy team performance
my_team = {
    "drivers": ["NOR", "PIA", "VER", "RUS", "HAM"],
    "constructors": ["MCL", "RBR"]
}

print("=== My Fantasy Team Performance ===")
total_points = 0

for driver in my_team["drivers"]:
    points = get_driver_points(driver, "14")
    info = get_driver_info(driver)
    total_points += points
    print(f"{driver}: {points} pts (${info['value']}, {info['percentagePicked']}% picked)")

for constructor in my_team["constructors"]:
    points = get_constructor_points(constructor, "14") 
    info = get_constructor_info(constructor)
    total_points += points
    print(f"{constructor}: {points} pts (${info['value']}, {info['percentagePicked']}% picked)")

print(f"Total team points: {total_points}")
```

### Driver Performance Analysis
```python
# Compare drivers over multiple rounds
drivers = ["VER", "NOR", "HAM", "RUS"]
rounds = ["12", "13", "14"]

print("Driver Performance Comparison:")
print("Driver\\tRound 12\\tRound 13\\tRound 14\\tAvg")

for driver in drivers:
    points = []
    for round_num in rounds:
        pts = get_driver_points(driver, round_num)
        points.append(pts)
    
    avg = sum(points) / len(points)
    print(f"{driver}\\t{points[0]}\\t{points[1]}\\t{points[2]}\\t{avg:.1f}")
```

### Overtaking Kings Analysis
```python
# Find the best overtakers
drivers = list_drivers()
round_num = "14"

print(f"Top Overtakers - Round {round_num}:")
overtake_data = []

for driver in drivers:
    try:
        overtakes = get_driver_breakdown(driver, round_num, "race", "overtakeBonus")
        if overtakes > 0:
            info = get_driver_info(driver)
            overtake_data.append((driver, info['team'], overtakes))
    except:
        continue

# Sort by overtake points
overtake_data.sort(key=lambda x: x[2], reverse=True)

for i, (driver, team, points) in enumerate(overtake_data[:10], 1):
    print(f"{i:2d}. {driver} ({team}): +{points} overtake points")
```

## 🔄 Data Updates

The library fetches data from GitHub in real-time, so you always get:
- ✅ Latest race results
- ✅ Most current driver/constructor standings  
- ✅ Updated fantasy point calculations
- ✅ Recent team changes and driver swaps

Data is automatically updated after each race weekend.

## ⚠️ Error Handling

```python
from formula_fantasy import F1FantasyError

try:
    points = get_driver_points("INVALID", "14")
except F1FantasyError as e:
    print(f"Error: {e}")
    # Handle the error appropriately
```

Common error scenarios:
- Invalid driver/constructor abbreviation
- Round data not available
- Network connectivity issues
- GitHub API rate limiting

## 🛠️ Advanced Usage

### Custom Round Names
```python
# The library also supports race names (when available)
points = get_driver_points("VER", "Hungary")    # If supported
points = get_driver_points("VER", "14")         # Recommended approach
```

### Session-Specific Analysis
```python
# Compare qualifying vs race performance
driver = "NOR"
round_num = "14"

qualifying = get_driver_breakdown(driver, round_num, "qualifying")
race = get_driver_breakdown(driver, round_num, "race")  
sprint = get_driver_breakdown(driver, round_num, "sprint")

print(f"{driver} Round {round_num}:")
print(f"Qualifying: {qualifying.get('position', 0)} pts")
print(f"Race: {race.get('position', 0)} pts") 
print(f"Sprint: {sprint.get('position', 0)} pts")
```

## 🌟 Pro Tips

1. **Use abbreviations consistently** - Always use 3-letter codes (VER, HAM, NOR)
2. **Cache expensive calls** - Store driver/constructor info if calling repeatedly
3. **Handle missing data gracefully** - Not all rounds have sprint sessions
4. **Check latest round** - Use `get_latest_round()` to know what data is available
5. **Batch CLI operations** - Use shell scripts for multiple queries

## 📊 Data Source

This library fetches data from the official F1 Fantasy scraper repository:
- **GitHub Repository**: [JoshCBruce/fantasy-data](https://github.com/JoshCBruce/fantasy-data)
- **Data Updates**: After each race weekend  
- **Coverage**: Complete 2025 F1 season
- **Accuracy**: Official F1 Fantasy point calculations

## 🤝 Contributing

Found a bug or want to contribute? 
1. Check the [issues page](https://github.com/yourusername/formula-fantasy/issues)
2. Fork the repository
3. Make your changes
4. Submit a pull request

## 📜 License

MIT License - feel free to use in your own projects!

---

**Happy F1 Fantasy analysis! 🏎️📊**