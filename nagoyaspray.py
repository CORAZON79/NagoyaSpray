#!/usr/bin/env python3

import argparse
from datetime import datetime

# ASCII Art Banner
BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ███╗   ██╗ █████╗  ██████╗  ██████╗ ██╗   ██╗ █████╗        ║
║   ████╗  ██║██╔══██╗██╔════╝ ██╔═══██╗╚██╗ ██╔╝██╔══██╗       ║
║   ██╔██╗ ██║███████║██║  ███╗██║   ██║ ╚████╔╝ ███████║       ║
║   ██║╚██╗██║██╔══██║██║   ██║██║   ██║  ╚██╔╝  ██╔══██║       ║
║   ██║ ╚████║██║  ██║╚██████╔╝╚██████╔╝   ██║   ██║  ██║       ║
║   ╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚═╝  ╚═╝       ║
║                                                               ║
║              ███████╗██████╗ ██████╗  █████╗ ██╗   ██╗        ║
║              ██╔════╝██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝        ║
║              ███████╗██████╔╝██████╔╝███████║ ╚████╔╝         ║
║              ╚════██║██╔═══╝ ██╔══██╗██╔══██║  ╚██╔╝          ║
║              ███████║██║     ██║  ██║██║  ██║   ██║           ║
║              ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝           ║
║                                                               ║
║                Developed by Strikoder | v1.0                  ║
║          Lightweight Wordlist Generator for Pentesting        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""

# Base word lists
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

SEASONS = ["Winter", "Spring", "Summer", "Autumn", "Fall"]

DAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday", 
    "Friday", "Saturday", "Sunday"
]

COMMON = ["Welcome", "Password", "Company", "Access"]


def capitalize_first_only(word):
    return word[0].upper() + word[1:].lower() if word else word


def capitalize_last_only(word):
    return word[:-1].lower() + word[-1].upper() if word else word


def generate_passwords(word_lists, years, attributes, position, cap_mode):
    passwords = set()
    
    # Combine all selected word lists
    all_words = []
    for word_list in word_lists:
        all_words.extend(word_list)
    
    year_start, year_end = years
    
    for word in all_words:
        for year in range(year_start, year_end + 1):
            # Full year
            year_str = str(year)
            # Short year (last 2 digits)
            year_short = str(year)[-2:]
            
            for y in [year_str, year_short]:
                # Base combination: word + year
                base = f"{word}{y}"
                
                # Apply capitalization
                if cap_mode == 'first':
                    base = capitalize_first_only(base)
                elif cap_mode == 'last':
                    base = capitalize_last_only(base)
                elif cap_mode == 'normal':
                    base = base.capitalize()
                elif cap_mode == 'all':
                    # Add multiple variations
                    passwords.add(base.lower())
                    passwords.add(base.upper())
                    passwords.add(base.capitalize())
                    passwords.add(capitalize_first_only(base))
                    continue
                
                # Add with attributes based on position
                for attr in attributes:
                    if attr == '':
                        # No attribute, just add base
                        passwords.add(base)
                    elif position == 'p':  # prefix (start)
                        passwords.add(f"{attr}{base}")
                    elif position == 's':  # suffix (end)
                        passwords.add(f"{base}{attr}")
                    elif position == 'b':  # both
                        passwords.add(f"{attr}{base}{attr}")
    
    return sorted(passwords)


def main():
    parser = argparse.ArgumentParser(
        description='Simple Password Spray List Generator',
        epilog='\nExample: python3 spray.py --seasons --months --start 2020 --end 2025 -p "!" -o passwords.txt'
    )
    
    # Word list selection
    parser.add_argument('--months', action='store_true', help='Include months')
    parser.add_argument('--seasons', action='store_true', help='Include seasons')
    parser.add_argument('--days', action='store_true', help='Include days of week')
    parser.add_argument('--common', action='store_true', help='Include common words')
    parser.add_argument('--all', action='store_true', help='Include all word types')
    parser.add_argument('-w', '--words', type=str, help='Custom comma-separated words')
    
    # Year range
    parser.add_argument('--start', type=int, help='Start year (default: current year)')
    parser.add_argument('--end', type=int, help='End year (default: current year)')
    
    # Attributes
    parser.add_argument('-p', '--prefix', type=str, default='', 
                       help='Comma-separated prefixes to add at START (e.g., "!,@,#")')
    parser.add_argument('-s', '--suffix', type=str, default='',
                       help='Comma-separated suffixes to add at END (e.g., "!,123")')
    parser.add_argument('-b', '--both-attr', type=str, default='',
                       help='Comma-separated attributes to add at BOTH start and end (e.g., "!")')
    
    # Position (hidden, determined by which flag is used)
    
    # Capitalization
    parser.add_argument('--cap', choices=['first', 'last', 'normal', 'all'], 
                       default='normal',
                       help='Capitalization mode (default: normal)')
    
    # Output
    parser.add_argument('-o', '--output', type=str, help='Output file (required unless --print is used)')
    parser.add_argument('--print', action='store_true', help='Print to stdout instead of file')
    
    args = parser.parse_args()
    
    # Print banner
    print(BANNER)
    
    # Validate output requirement
    if not args.print and not args.output:
        print("[!] Error: Output file required (-o) unless --print is specified")
        print("\nExample: python3 spray.py --seasons --months --start 2020 --end 2025 -s \"!\" -o passwords.txt")
        return
    
    # Set default years
    current_year = datetime.now().year
    year_start = args.start if args.start else current_year
    year_end = args.end if args.end else current_year
    
    # Select word lists
    word_lists = []
    if args.all:
        word_lists = [MONTHS, SEASONS, DAYS, COMMON]
    else:
        if args.months:
            word_lists.append(MONTHS)
        if args.seasons:
            word_lists.append(SEASONS)
        if args.days:
            word_lists.append(DAYS)
        if args.common:
            word_lists.append(COMMON)
    
    # Add custom words
    if args.words:
        custom_words = [w.strip() for w in args.words.split(',')]
        word_lists.append(custom_words)
    
    if not word_lists:
        print("[!] Error: No word lists selected. Use --months, --seasons, --days, --common, or --all")
        return
    
    # Determine which attribute flag was used
    attributes = []
    position = None
    
    if args.prefix:
        attributes = [s.strip() for s in args.prefix.split(',')]
        position = 'p'
    elif args.suffix:
        attributes = [s.strip() for s in args.suffix.split(',')]
        position = 's'
    elif args.both_attr:
        attributes = [s.strip() for s in args.both_attr.split(',')]
        position = 'b'
    else:
        attributes = ['']
        position = 's'
    
    print(f"[*] Generating passwords...")
    print(f"[*] Year range: {year_start}-{year_end}")
    print(f"[*] Attributes: {attributes if attributes != [''] else 'None'}")
    print(f"[*] Position: {'PREFIX (start)' if position == 'p' else 'SUFFIX (end)' if position == 's' else 'BOTH'}")
    print(f"[*] Capitalization: {args.cap}")
    
    # Generate passwords
    passwords = generate_passwords(
        word_lists=word_lists,
        years=(year_start, year_end),
        attributes=attributes,
        position=position,
        cap_mode=args.cap
    )
    
    print(f"[+] Generated {len(passwords)} unique passwords")
    
    # Output
    if args.output:
        with open(args.output, 'w') as f:
            for pwd in passwords:
                f.write(pwd + '\n')
        print(f"[+] Saved to {args.output}")
    
    if args.print:
        for pwd in passwords:
            print(pwd)


if __name__ == '__main__':
    main()
