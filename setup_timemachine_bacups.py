#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
###

### Set up logging
import logging
from util import color_stream

handler = color_stream.ColorizingStreamHandler()
handler.setFormatter(logging.Formatter(\
"%(asctime)s [%(levelname)5s] %(name)s - %(message)s"))
root = logging.getLogger()
root.addHandler(handler)
root.setLevel(logging.WARN)
logger = logging.getLogger(__name__)
## will apply to all child modules of this package, as well
logger.setLevel(logging.DEBUG)
###

import ConfigParser
import os, re, sys, optparse, random, string, time, shutil, commands
from optparse import OptionParser


### Dudes command line Option Parser
parser = optparse.OptionParser(version='%prog version 1')
parser.add_option(
  '-b',
  '--backup',
  help='The name of the USB Volume to use.',
  dest='vol_name',
  action='store')
parser.add_option(
  '-d',
  '--disable',
  help='Disable the unmounter for when needed to restore files from Time Machine.',
  dest='disable_agents',
  action='store')

(opts, args) = parser.parse_args()
mandatory = [
  'vol_name'
  ]
for m in mandatory:
  if not opts.__dict__[m]:
    print "Mandatory options missing:"
    #dudes_logger.error('Oops! Badness happened, Mandatory options missing...')
    parser.print_help()
    sys.exit(1)

### Copy from here the there
def move_files(
    src_path,
    src,
    dst):
  """Copy source files to destination directory"""
  assert [src_path, src, dst] is not None, 'either one of src_path, src & dst or all is not set'
  for script_name in src:
    full_name = os.path.join(src_path, script_name)
    if (os.path.isfile(full_name)):
      logger.info("Copying %s templates into place: %s%s", full_name, dst, script_name)
      shutil.copy(full_name, dst)
    else:
      logger.critical("ERROR: Could not copy %s templates into place: %s%s", full_name, dst, script_name)

### Create links and shit...
def link_this(
    path,
    files,
    sym):
  """Create Symbolic links of the scripts & configs."""
  assert [path, files, sym] is not None, 'Either the path, files, and sym vars or one of were not set'
  cwd = os.getcwd()
  for file_name in files:
    full_name = os.path.join(path, file_name)
    abs_full_name = os.path.join(cwd, full_name)
    if (os.path.isfile(full_name)):
      logger.info("Creating Symbolic link for %s -> %s%s", full_name, sym, file_name)
      #logger.info("%s", abs_full_name)
      os.symlink(abs_full_name, os.path.join(sym, file_name))
    else:
      logger.critical("Could not find %s to create symbolic link", full_name)

###
# Find and replace pattern. This is less that good...
# it loads the entire file word by word into
# Memeory and then writes it back out. this is fine
# on these small scripts but not a good pattern to use on larger files.
def search_and_destroy(
    script,
    old_patt,
    new_patt):
  """Load the file into memmory word by word searching for \
  the pattern to be replaced. then writes the file back out again."""
  assert script is not None, 'The script file was empty'
  if (os.path.isfile(script)):
    logger.info("Opening %s to replace %s placeholder with %s", script, old_patt, new_patt)
    f1 = open(script,'r').read()
    f2 = open(script,'w')
    logger.info("Searching for %s and replacing it with %s", old_patt, new_patt)
    m = f1.replace(old_patt,new_patt)
    f2.write(m)
    logger.info("Closing %s script and writing out back to file.", script)
  else:
    logger.critical("ERROR: Could not stat %s", script)

#
### Vars
home_path             = os.environ.get('HOME')
src_scripts_path      = "src/scripts/"
src_configs_path      = "src/configs/"
src_scripts           = os.listdir(src_scripts_path)
src_configs           = os.listdir(src_configs_path)
dst_scripts           = "scripts/"
dst_configs           = "configs/"
dst_scripts_sym_path  = "/usr/local/bin/"
dst_configs_sym_path  = os.path.join(home_path, 'Library/LaunchAgents/')
old_pattern           = "%BNAME%"
new_pattern           = opts.vol_name

###
# Make the config and script directories:
the_directories = [
  "configs/",
  "scripts/"
]
for d in the_directories:
  logger.info("Checking if %s exists", d)
  if not os.path.exists(d):
    logger.info("making directory: %s", d)
    os.makedirs(d)

#
### Move the scripts and configs into place:
move_files(src_scripts_path, src_scripts, dst_scripts)
move_files(src_configs_path, src_configs, dst_configs)
###
#

###
# create the symlinks for the scripts and configs
link_this(dst_scripts, os.listdir(dst_scripts), dst_scripts_sym_path)
link_this(dst_configs, os.listdir(dst_configs), dst_configs_sym_path)

###
# modify the scripts to use the backup Volume passed in with the "-b" flag
for tm_script in os.listdir(dst_scripts):
  script_cwd = os.getcwd()
  s_path = os.path.join(dst_scripts, tm_script)
  full_scripts_path = os.path.join(script_cwd, s_path)
  if (os.path.isfile(full_scripts_path)):
    logger.info("the %s is being updated", full_scripts_path)
    search_and_destroy(full_scripts_path, old_pattern, new_pattern)
  else:
    logger.critical("ERROR: could not load the %s file", full_scripts_path)

###
# Lastly run these commands to load TimeMachine plist files 
#commands.getstatusoutput(
#  "/usr/bin/sudo /bin/launchctl unload -w \
#  /System/Library/LaunchDaemons/com.apple.backupd-auto.plist")
for conf in src_configs:
  full_conf_path = os.path.join(dst_configs_sym_path, conf)
  logger.info("adding the Launch config %s", full_conf_path)
  commands.getstatusoutput("/bin/launchctl load "+full_conf_path)



###
#   Lastly run these commands:
#   sudo launchctl unload -w /System/Library/LaunchDaemons/com.apple.backupd-auto.plist
#   launchctl load ~/Library/LaunchAgents/com.apple.TimeMachine_OnMount.plist
#   launchctl load ~/Library/LaunchAgents/com.apple.TimeMachine_OnLoadSchedule.plist
#
## Also:
# make sure to add a function that can turn off the auto unmounting for when you need to restore files from Time Machine.
#
###
