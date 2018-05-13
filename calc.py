import diff_calc
import requests
import pp_calc
import sys
import argparse
import b_info
import configparser
from beatmap import Beatmap
parser = argparse.ArgumentParser()
feature = False
mod_s = ""
c100 = 0
c50 = 0
misses = 0
sv = 1
acc = 0
combo = 0
parser.add_argument('file', help='File or url. If url provided use -l flag')
parser.add_argument('-l', help='Flag if url provided', action='store_true')
parser.add_argument('-acc', help='Accuracy', metavar="acc%", default=0)
parser.add_argument('-c100', help='Number of 100s', metavar="100s", default=0)
parser.add_argument('-c50', help='Number of 50s', metavar="50s", default=0)
parser.add_argument('-m', help='Number of misses', metavar="miss", default=0, dest='misses')
parser.add_argument('-c', help='Max combo', metavar="combo", default=0, dest='combo')
parser.add_argument('-sv', help='Score version 1 or 2', metavar="sv", default=1)
parser.add_argument('-mods', help='Mod string eg. HDDT', metavar="mods", default="")
args = parser.parse_args()
c100 = int(args.c100)
c50 = int(args.c50)
misses = int(args.misses)
combo = int(args.combo)
acc = float(args.acc)
sv = int(args.sv)
mod_s = args.mods
feature = args.l
file_name = ""

try:
    f = open('keys.cfg');
    config = configparser.ConfigParser()
    config.readfp(f)
    key = config._sections["osu"]['api_key']
except:
    raise Exception("Invalid config")
try:
	file_name = args.file
	if feature:
		if key == "":
			print("Please enter an API key to use this feature.")
			raise()
		file = requests.get(b_info.main(file_name, key)).text.splitlines()
	else:
		file = open(file_name)
except:
	print("ERROR: "+file_name + " not a valid beatmap or API key is incorrect")
	sys.exit(1)
map = Beatmap(file)
if combo == 0 or combo > map.max_combo:
	combo = map.max_combo


def mod_str(mod):
	string = ""
	if mod.nf:
		string += "NF"
	if mod.ez:
		string += "EZ"
	if mod.hd:
		string += "HD"
	if mod.hr:
		string += "HR"
	if mod.dt:
		string += "DT"
	if mod.ht:
		string += "HT"
	if mod.nc:
		string += "NC"
	if mod.fl:
		string += "FL"
	if mod.so:
		string += "SO"
	return string

class mods:
	def __init__(self):
		self.nomod = 0,
		self.nf = 0
		self.ez = 0
		self.hd = 0
		self.hr = 0
		self.dt = 0
		self.ht = 0
		self.nc = 0
		self.fl = 0
		self.so = 0
		self.speed_changing = self.dt | self.ht | self.nc
		self.map_changing = self.hr | self.ez | self.speed_changing
	def update(self):
		self.speed_changing = self.dt | self.ht | self.nc
		self.map_changing = self.hr | self.ez | self.speed_changing
mod = mods()

def set_mods(mod, m):
		if m == "NF":
			mod.nf = 1
		if m == "EZ":
			mod.ez = 1
		if m == "HD":
			mod.hd = 1
		if m == "HR":
			mod.hr = 1
		if m == "DT":
			mod.dt = 1
		if m == "HT":
			mod.ht = 1
		if m == "NC":
			mod.nc = 1
		if m == "FL":
			mod.fl = 1
		if m == "SO":
			mod.so = 1

if mod_s != "":
	mod_s = [mod_s[i:i+2] for i in range(0, len(mod_s), 2)]
	for m in mod_s:
		set_mods(mod, m)
		mod.update()

mod_string = mod_str(mod)
map.apply_mods(mod)
diff = diff_calc.main(map)
if acc == 0:
	pp = pp_calc.pp_calc(diff[0], diff[1], diff[3], misses, c100, c50, mod, combo,sv)
else:
	pp = pp_calc.pp_calc_acc(diff[0], diff[1], diff[3], acc, mod, combo, misses,sv)
title = map.artist + " - "+map.title + "["+map.version+"]" 
if mod_string != "":
	title += "+" + mod_string
title += " (" + map.creator + ")"
print("Map: " + title)
print("AR: " + str(round(map.ar, 2)) + " CS: " + str(round(map.cs,2)) + " OD: " + str(round(map.od,2)))
print("Stars: "+str(round(diff[2], 2)))
print("Acc: "+str(round(pp.acc_percent, 2)) + "%")
comb_s = "Combo: "+str(int(combo)) + "/" + str(int(map.max_combo))
if misses != 0:
	comb_s += " with " + str(misses) + " misses"
print(comb_s)
print("Performance: "+str(round(pp.pp, 2)) + "PP")