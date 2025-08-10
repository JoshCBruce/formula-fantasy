#!/usr/bin/env python3
"""
Command Line Interface for F1 Fantasy Library

Simple CLI for quick data access:
- formula-fantasy VER 15 -> get driver points
- formula-fantasy VER 15 race overtakeBonus -> get specific breakdown
- formula-fantasy RBR 15 -> get constructor points
"""

import sys
import argparse
from . import core

def main():
    parser = argparse.ArgumentParser(
        description="F1 Fantasy Data CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s VER 15                     # Driver points for round 15
  %(prog)s VER latest                 # Driver points for latest round
  %(prog)s VER 15 race overtakeBonus  # Specific point breakdown
  %(prog)s RBR 15                     # Constructor points for round 15
  %(prog)s VER --season               # Driver season total points
  %(prog)s MCL --season               # Constructor season total points
  %(prog)s --drivers                  # List all drivers
  %(prog)s --constructors             # List all constructors
        """
    )
    
    parser.add_argument("abbreviation", nargs="?", help="Driver/Constructor abbreviation")
    parser.add_argument("round", nargs="?", default="latest", help="Round number or 'latest'")
    parser.add_argument("session", nargs="?", default="race", help="Session: race, sprint, qualifying")
    parser.add_argument("points_type", nargs="?", help="Specific points type")
    
    parser.add_argument("--drivers", action="store_true", help="List all available drivers")
    parser.add_argument("--constructors", action="store_true", help="List all available constructors")
    parser.add_argument("--info", action="store_true", help="Get full info for abbreviation")
    parser.add_argument("--breakdown", action="store_true", help="Get points breakdown")
    parser.add_argument("--season", action="store_true", help="Get season total points")
    
    args = parser.parse_args()
    
    try:
        if args.drivers:
            drivers = core.list_drivers()
            print("Available drivers:", ", ".join(drivers))
            return
            
        if args.constructors:
            constructors = core.list_constructors()
            print("Available constructors:", ", ".join(constructors))
            return
            
        if not args.abbreviation:
            parser.print_help()
            return
            
        abbrev = args.abbreviation.upper()
        
        # Check if it's a driver or constructor
        is_driver = abbrev in core.list_drivers()
        is_constructor = abbrev in core.list_constructors()
        
        if not is_driver and not is_constructor:
            print(f"Error: '{abbrev}' is not a valid driver or constructor abbreviation")
            print("Use --drivers or --constructors to see available options")
            return
            
        if args.info:
            if is_driver:
                info = core.get_driver_info(abbrev)
                print(f"Driver: {info.get('displayName', abbrev)}")
                print(f"Team: {info.get('team', 'N/A')}")
                print(f"Season Total: {info.get('seasonTotalPoints', 0)} points")
                print(f"Value: {info.get('value', 'N/A')}")
                print(f"Picked by: {info.get('percentagePicked', 0)}%")
            else:
                info = core.get_constructor_info(abbrev)
                print(f"Constructor: {info.get('displayName', abbrev)}")
                print(f"Season Total: {info.get('seasonTotalPoints', 0)} points")
                print(f"Value: {info.get('value', 'N/A')}")
                print(f"Picked by: {info.get('percentagePicked', 0)}%")
            return

        if args.season:
            if is_driver:
                points = core.get_driver_season_points(abbrev)
                print(f"{abbrev} season total: {points} points")
            else:
                points = core.get_constructor_season_points(abbrev)
                print(f"{abbrev} season total: {points} points")
            return
            
        if args.breakdown or args.points_type:
            if is_driver:
                result = core.get_driver_breakdown(abbrev, args.round, args.session, args.points_type)
            else:
                result = core.get_constructor_breakdown(abbrev, args.round, args.session, args.points_type)
                
            if isinstance(result, dict):
                print(f"{abbrev} {args.session} breakdown for round {args.round}:")
                for key, value in result.items():
                    print(f"  {key}: {value}")
            else:
                print(f"{abbrev} {args.points_type} in {args.session} round {args.round}: {result}")
        else:
            # Simple points query
            if is_driver:
                points = core.get_driver_points(abbrev, args.round)
            else:
                points = core.get_constructor_points(abbrev, args.round)
            print(f"{abbrev} round {args.round}: {points} points")
            
    except core.F1FantasyError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()