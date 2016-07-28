# timemachine_automount_unmount #

timemachine_automount_unmount is used to automount & unmount a USB Harddrive for timemachine backups.

### This Repo is for setting up timemachine_automount_unmount  ###

I have a USB backup drive connected through USB hub at work to my Macbook Pro and I often find myself wanting to quickly unplug and go without the consequences of the drive not being ejected properly. As well, I need the drive to be mounted so that Time Machine can do its automatic backups.

This is based on a [blog post](http://somethinginteractive.com/blog/2013/07/24/time-machine-auto-mountunmount-drive-os-x/) my coworker shared with me a few years ago.

**There is one caveat, in that when attempting to restore files from your Time Machine drive, you will need to disable the launch agents, as well you should re-activate Time Machine in the system preferences so that the system recognizes the drive for restore purposes.**


### How do I get set up? ###
* USB Harddrive
* Time Machine configured to use the USB hardrive as the backup Volume.
* Checkout this repo
* run the setup utility(setup_timemachine_bacups.py)

**NOTE: It is important that you all ready have timemachine configured to use your USB harddrive and that you know the name of the Volume of the drive.

```
#!/bin/bash


```

**EXAMPLE:**
```
setup_timemachine_bacups.py -b <NAME OF BACKUP VOL>
setup_timemachine_bacups.py --backup <NAME OF BACKUP VOL>
```

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact

