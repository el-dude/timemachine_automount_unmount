#!/bin/bash
#
###
#
# Set the drive name that we mount for our backups
VOLMOUNT="%BNAME%"

# Conditional argument: if mounted entry has the volume name in the variable string
mount | grep "${VOLMOUNT}"
if [[$? != "0" ]]; then
  # Drive isn't mounted, so: mount. A LaunchAgent will pick this OnMount action up and run the backup script
  diskutil mount "${VOLMOUNT}"
else
  # Drive is mounted, so: run the backup script
  timemachine_backup.sh
fi
