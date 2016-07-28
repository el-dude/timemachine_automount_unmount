#!/bin/bash
#
###
#
# Set the drive name that we mount for our backups
VOLMOUNT="%BNAME%"

# Conditional argument: if mounted entry has the volume name in the variable string
#if mount | grep "${VOLMOUNT}" ; then
mount | grep "${VOLMOUNT}";
if [[ $? == "0" ]]; then
  # Drive is mounted, so: backup and then eject after
  tmutil startbackup -b &&
  #diskutil eject "${VOLMOUNT}"
  diskutil unmount "${VOLMOUNT}"
fi
