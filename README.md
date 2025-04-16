# Dwarf Fortress Steam Workshop Mod Fixer Script

This script automates the fix described in [this Steam guide](https://steamcommunity.com/sharedfiles/filedetails/?id=2908486502) for resolving the issue with Steam Workshop mods not deployed correctly.

Steam Workshop mods are not being deployed in the installed_mods directory of Dwarf Fortress.

This script:

- Takes a **source** directory (usually your Steam Workshop content directory),
- Takes a **destination** directory (usually the mod directory your game reads from),
- Copies and reorganizes mod files to ensure compatibility with the game.

This replicates the manual fix described in the linked Steam guide.

## How to Use

### Prerequisites

- Python 3.x
- OS: Windows(untested), macOS(untested), Linux

### Use

Clone this repository or download the script file directly and run fixer.py like this:

```bash
python fixer.py "/home/guy/.steam/steam/steamapps/workshop/content/975370" "/home/guy/.steam/steam/steamapps/common/Dwarf Fortress/data/installed_mods"
```
