# Web Scraper v1.0
# Capture mod IDs from the Steam collection webpage so that the server is
# always downloading the same mods as the clients

import os
import shutil
import subprocess
import urllib2
import re
from bs4 import BeautifulSoup 

import logging
logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s ", level=logging.DEBUG)

def move_mods():
	target_dir = "~/starbound/mods/"
	directories = os.listdir( target_dir )
	pattern = re.compile( "[0-9]+" )
	for containing_folder in directories:
		if os.path.isdir( target_dir + containing_folder ) and pattern.match( containing_folder ):
			for file in os.listdir( target_dir + containing_folder + "/" ):
				shutil.copyfile( target_dir + containing_folder + "/" +  file, target_dir + containing_folder + file )

def main():
	# Get home dir
	HOME = os.environ.get("HOME", "/home/default/")

	# Location of mod list
	mod_list = HOME + "/starbound_modlist"

	# Location of starbound mod directory
	mod_dir = HOME + "/starbound/mods/"

	# Location of starbound_update.sh
	update_script_path = HOME + "/Steam/starbound_update_helper.sh"

	# URL of our server mod collection
	url = "http://steamcommunity.com/sharedfiles/filedetails/?id=1234649677"

	# Set of mod IDs
	new_mod_ids = set()

	# Set of existing mods
	old_mod_ids = set()


	# Grab the HTML of the collection page, then parse it using BeutifulSoup
	collection_page = BeautifulSoup(urllib2.urlopen(url), 'html.parser')

	# Regular expression to capture the mod ID inside of the script tag on the collection page
	pattern = re.compile(r'SharedFileBindMouseHover\( "sharedfile_([0-9]+).*"', re.MULTILINE | re.DOTALL)

	workshop_id = collection_page.find_all('script', text=pattern)

	# Iterate through each match and store the ID
	for row in workshop_id:
		match = pattern.search(row.text)
		if match:
			new_mod_ids.add(match.group(1).strip())


	# Compare the new mod list with the old one
	# Read in current mod list
	current_mods=open(mod_list, 'a+')
	current_mods.seek(0)


	for line in current_mods.readlines():
		logging.debug("Loading mod ID: " + line)
		old_mod_ids.add(line.strip())
	current_mods.seek(0)
	logging.debug("Loaded %d existing mods." % len(current_mods.readlines()))


	# The difference of the old set and the new set = mods in the old set that aren't in the new = mods to remove
	to_remove = old_mod_ids - new_mod_ids
	if len(to_remove) > 0:
		logging.debug("Found %d local mods not in the collection, deleting..."  % len(to_remove))
		for mod in to_remove:
			if not os.path.isdir(mod_dir + mod):
				logging.warning("Mod ID " + " does not exist but was removed from mod list, ignoring...")
			else:
				shutil.rmtree(mod_dir + mod)


	# The opposite is also important: mods in the new and not in the old need to be added
	to_add = new_mod_ids - old_mod_ids
	if len(to_add) > 0:
		print "Found %d new mods, adding..." % len(to_add)
		for mod_id in to_add:
			logging.debug("Adding new mod " + mod_id)
			current_mods.write(mod_id + '\n')
	else:
		print "There are no new mods to add."
		current_mods.close()
		exit()

	current_mods.close()


	# Run the script to update the server
	logging.debug("Running update script...")
	subprocess.call(update_script_path, shell=True)
	move_mods()
	logging.debug("Update finished, exiting...")

if __name__ == "__main__":
	main()