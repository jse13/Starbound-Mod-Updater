#!/bin/bash

# App ID of Starbound
starbound_id=211820

# Get password for account
while read -r u p
do
	user=$u
	pass=$p
done <$GDS_CREDS

# Scraped list of mods
mod_list=$HOME/starbound_modlist

# Full path to SteamCMD script
steamcmd_path=$HOME/Steam/steamcmd.sh

# Temporary location for steamCMD script
temp_file=$HOME/Steam/temp


# Clean up the existing mod directory
mkdir -p $HOME/starbound/mods_BAK
rm -rf $HOME/starbound/mods_BAK/*
mv $HOME/starbound/mods/* $HOME/starbound/mods_BAK/

# Beginning of script
echo "Prepping SteamCMD script..."

printf "@ShutdownOnFailedCommand 1\n@NoPromptForPassword 1\nlogin %s %s\nforce_install_dir /home/julsebeng/starbound\napp_update %s validate\nforce_install_dir /home/julsebeng/starbound/mods\n" "$user" "$pass" "$starbound_id" > $temp_file

# Iterate through each mod ID in the specified file
echo "Adding workshop mods to install to the script..."
while read p; do
	printf "workshop_download_item %s %s\n" "$starbound_id" "$p" >> $temp_file
	printf "Added workshop ID %s to script...\n" "$p"
done < $mod_list

printf "quit\n" >> $temp_file


echo "Running script..."
$steamcmd_path +runscript $temp_file


#Cleanup
echo "Removing temp script file..."
rm $temp_file
echo "Moving mods to the proper directory..."
mv -v /home/julsebeng/starbound/mods/steamapps/workshop/content/211820/* /home/julsebeng/starbound/mods
rm -rf /home/julsebeng/starbound/mods/steamapps/
