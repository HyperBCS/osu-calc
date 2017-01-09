# osu-calc
osu! calc is a performance point(PP) calculator for the game osu! This program only works on standard beatmaps. If provided an API key you will be able to use a link to easily calculate PP without downloading the beatmap. Use keys.cfg to add the API key. Most of this code is based on the C++ version located [here](https://github.com/Francesco149/oppai).

# Usage

This program is written in python and requires version 2.7. There are several supported arguments.

* -l <link> (If API key available)
* -acc <% acc>
* -c100 <# of 100s>
* -c50 <# of 50s>
* -m <# of misses>
* -sv <score version 1 or 2>
* -mods <string of mods>

Example
```python
python calc.py map.osu
python calc.py map.osu -mods HDDTHR
python calc.py -l https://osu.ppy.sh/b/994495
```
