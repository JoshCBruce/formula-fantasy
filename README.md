# Formula Fantasy 🏎️

[![PyPI version](https://img.shields.io/badge/PyPI-v1.0.3-blue)](https://pypi.org/project/formula-fantasy/)
[![Python versions](https://img.shields.io/pypi/pyversions/formula-fantasy.svg)](https://pypi.org/project/formula-fantasy/)
[![License](https://img.shields.io/github/license/JoshCBruce/formula-fantasy.svg)](https://github.com/JoshCBruce/formula-fantasy/blob/main/LICENSE)

A comprehensive Python library for accessing and analyzing Formula 1 Fantasy data with powerful visualization capabilities.

## 🌟 Features

- **Complete F1 Fantasy Data Access**: Driver and constructor points, breakdowns, team information
- **Real-time Data**: Always up-to-date with latest race results  
- **Powerful Visualizations**: Professional charts and dashboards with matplotlib integration
- **Fantasy Strategy Tools**: Value analysis, popularity trends, pick recommendations
- **Command Line Interface**: Quick data access via CLI commands
- **Easy Integration**: Simple Python API for custom analysis

## 🚀 Quick Start

### Installation

```bash
pip install formula-fantasy
```

### Basic Usage

```python
from formula_fantasy import get_driver_points, get_constructor_points

# Get driver points for latest race
points = get_driver_points("VER")  # Max Verstappen
print(f"VER latest points: {points}")

# Get constructor points for specific round
points = get_constructor_points("MCL", "14")  # McLaren round 14
print(f"MCL round 14: {points} points")
```

### CLI Usage

```bash
# Driver points for specific round
formula-fantasy VER 14

# Constructor points for latest round  
formula-fantasy MCL latest

# List all available drivers
formula-fantasy --drivers
```

## 📊 Data Visualization

Create stunning visualizations with the included examples:

```python
# Run the comprehensive visualization demo
python examples/example_visualization.py

# Generate sample plots as image files
python examples/create_sample_plots.py
```

### Example Visualizations

![Driver Performance Comparison](images/driver_comparison.png)
*Driver performance comparison showing recent rounds and season totals*

![Value Analysis Dashboard](images/value_analysis.png)
*Comprehensive value analysis with bubble charts and strategy recommendations*

![Constructor Analysis](images/constructor_analysis.png)
*Constructor championship standings and team analysis*

**Features:**
- **Driver Performance Comparisons**: Track multiple drivers across recent rounds
- **Value Analysis Dashboards**: Find the best fantasy picks based on points per cost
- **Constructor Championships**: Season standings and team comparisons  
- **Strategy Analysis**: Popular vs contrarian picks, recent form trends

## 📁 Project Structure

```
formula-fantasy/
├── formula_fantasy/          # Main package
│   ├── __init__.py           # Package initialization  
│   ├── core.py               # Core data access functions
│   ├── cli.py                # Command line interface
│   └── README.md             # Package documentation
├── examples/                 # Example programs
│   ├── example_visualization.py    # Comprehensive demo
│   └── create_sample_plots.py      # Generate plot images
├── docs/                     # Documentation
│   ├── VISUALIZATION_EXAMPLE.md   # Visualization guide
│   ├── UPLOAD_INSTRUCTIONS.md     # PyPI upload guide
│   └── dataformat.md              # Data format reference
├── images/                   # Generated visualization samples
│   ├── driver_comparison.png
│   ├── value_analysis.png
│   └── constructor_analysis.png
├── dist/                     # Distribution packages
├── setup.py                  # Package setup
├── pyproject.toml           # Modern package config
└── requirements-viz.txt     # Visualization dependencies
```

## 🔧 API Reference

### Core Functions

```python
from formula_fantasy import *

# Driver data
get_driver_points(abbreviation, round="latest")
get_driver_breakdown(abbreviation, round="latest", session="race", points_type=None) 
get_driver_info(abbreviation)

# Constructor data  
get_constructor_points(abbreviation, round="latest")
get_constructor_breakdown(abbreviation, round="latest", session="race", points_type=None)
get_constructor_info(abbreviation)

# Utility functions
list_drivers()                # Get all available drivers
list_constructors()          # Get all available constructors  
get_latest_round()           # Get current round number
```

### Available Drivers
```
VER, NOR, RUS, PIA, HAM, LEC, SAI, ALO, OCO, GAS, 
ALB, HUL, STR, BOR, TSU, LAW, ANT, BEA, COL, DOO, HAD
```

### Available Constructors  
```
MCL, FER, RBR, MER, AMR, ALP, HAS, RB, WIL, SAU
```

## 🎯 Fantasy Strategy Examples

### Find Value Picks
```python
from formula_fantasy import get_driver_info, list_drivers

# Find best points per cost ratio
for driver in list_drivers():
    info = get_driver_info(driver)
    value = float(info['value'].replace('M', ''))
    points = info['seasonTotalPoints']
    ratio = points / value if value > 0 else 0
    print(f"{driver}: {ratio:.1f} pts/M")
```

### Track Performance Trends
```python
from formula_fantasy import get_driver_points

driver = "NOR"
recent_rounds = ["13", "14", "15"]

print(f"{driver} recent performance:")
for round_num in recent_rounds:
    points = get_driver_points(driver, round_num)
    print(f"  Round {round_num}: {points} points")
```

## 📈 Visualization Requirements

For visualization features, install additional dependencies:

```bash
pip install -r requirements-viz.txt
```

Or manually:
```bash
pip install matplotlib pandas seaborn numpy
```

## 🛠️ Development

### Building the Package

```bash
# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build distribution packages
python -m build

# Upload to PyPI (with proper credentials)
python -m twine upload dist/*
```

**PyPI Package**: https://pypi.org/project/formula-fantasy/

### Testing

```bash
# Test basic functionality
python -c "from formula_fantasy import get_driver_points; print(get_driver_points('VER', '14'))"

# Test CLI
formula-fantasy VER 14

# Run visualization examples  
python examples/example_visualization.py
```

## 🔗 Links

- **📦 PyPI Package**: https://pypi.org/project/formula-fantasy/
- **🐙 GitHub Repository**: https://github.com/JoshCBruce/formula-fantasy
- **📊 Data Source**: https://github.com/JoshCBruce/fantasy-data

## 📊 Data Source

Data is sourced from the official Formula 1 Fantasy platform via the [fantasy-data repository](https://github.com/JoshCBruce/fantasy-data), providing:

- **Real-time race results** and fantasy points
- **Historical performance** data for all drivers/constructors  
- **Team information** including values and popularity metrics
- **Detailed breakdowns** by point category (position, overtakes, etc.)

## 🤝 Contributing

Contributions welcome! Please ensure any changes maintain compatibility with the existing API.

## 📜 License

MIT License - see LICENSE file for details.

## 🏁 Example Results

Recent data shows:
- **McLaren leading constructors** with 1215+ season points
- **Best value drivers**: HUL (16.1 pts/M), BEA (11.3 pts/M), ANT (7.7 pts/M)
- **Most popular constructor**: Williams (25% ownership)
- **Consistent performers**: NOR averaging 35+ points in recent rounds

---

**Happy Formula Fantasy analysis! 🏎️📊**