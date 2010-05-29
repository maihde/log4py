#!/usr/bin/env python
# vim: sw=2: et:
#
# Copyright (c) 2010 by Michael Ihde <mike.ihde@randomwalking.com>
#
#                All Rights Reserved
#
# Permission to use, copy, modify, and distribute this software
# and its documentation for any purpose and without fee is hereby
# granted, provided that the above copyright notice appear in all
# copies and that both that copyright notice and this permission
# notice appear in supporting documentation, and that the name of
# Michael Ihde  not be used in advertising or publicity
# pertaining to distribution of the software without specific, written
# prior permission.
#
# Michael Ihde DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS
# SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS, IN NO EVENT SHALL Michael Ihde BE LIABLE FOR
# ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#
import logging, logging.handlers
import codecs
import sys
import os
import string
from appenders import *
from layouts import *

# Map log4j levels to python logging levels
_LEVEL_TRANS = {"ALL": logging.NOTSET,
                "DEBUG": logging.DEBUG,
                "INFO": logging.INFO,
                "WARN": logging.WARNING,
                "ERROR": logging.ERROR,
                "FATAL": logging.FATAL,
                "OFF": logging.FATAL + 1
               }

def _parsePropertiesFile(f):
  """Parse a Java Properties file into a python dictionary.

  NOTE: CURRENTLY THIS DOES NOT SUPPORT ESCAPE CHARACTERS
  NOR LINE CONTINUATIONS.
  """
  if isinstance(f, str):
    f = open(f)
 
  result = {}
  # The stream is assumed to be using the ISO 8859-1 character encoding
  for line in codecs.iterdecode(f, "iso-8859-1"):
    line = line.lstrip()
    # A natural line that contains only white space characters is considered
    # blank and is ignored. A comment line has an ASCII '#' or '!' as its first
    # non-white space character; comment lines are also ignored
    if len(line) == 0 or line[0] in ('#', '!'):
      continue

    key = None
    value = None
    for i, char in enumerate(line):
      if char in ('\\'):
        # TODO properly deal with escape characters and line continuations
        continue

      # The key contains all of the characters in the line starting with the
      # first non-white space character and up to, but not including, the first
      # unescaped '=', ':', or white space character other than a line
      # terminator.
      if char in ('=', ':', ' ', '\t', '\f'):
        key = line[0:i]
        value = line[i+1:].lstrip()
        result[key] = value
        break
  return result

def _import_handler(name):
  if name.startswith("org.apache.log4j."):
    name = name[len("org.apache.log4j."):]
  return eval(name) # SECURITY HOLE, ARBITRARY PYTHON CODE CAN BE PLACED IN THE CONFIG FILE

def _import_layout(name):
  if name.startswith("org.apache.log4j."):
    name = name[len("org.apache.log4j."):]
  return eval(name) # SECURITY HOLE, ARBITRARY PYTHON CODE CAN BE PLACED IN THE CONFIG FILE

def fileConfig(f):
  props = _parsePropertiesFile(f)
  try:
    repoWideThresh = props["log4j.threshold"].strip()
    logging.getLogger().setLevel(_LEVEL_TRANS[repoWideThresh.strip().upper()])
  except KeyError:
    logging.getLogger().setLevel(logging.NOTSET)

  # First load up all loggers and set their levels
  loggers = {}
  rootLoggerCfg = props["log4j.rootLogger"].split(",")
  if rootLoggerCfg[0].strip().upper() in _LEVEL_TRANS.keys():
    logging.getLogger().setLevel(_LEVEL_TRANS[rootLoggerCfg[0].strip().upper()])
    del rootLoggerCfg[0]
  else:
    logging.getLogger().setLevel(logging.NOTSET)

  loggers[logging.getLogger()] = [x.strip() for x in rootLoggerCfg]

  configuredLoggers = filter(lambda x: x.startswith("log4j.logger."), props.keys())
  configuredLoggers = [x[len("log4j.logger."):] for x in configuredLoggers]
  for logger in configuredLoggers:
    loggerCfg = props[logger].split(",")
    if loggerCfg[0].strip() in _LEVEL_TRANS.keys():
      logging.getLogger(logger).setLevel(_LEVEL_TRANS[loggerCfg[0]])
      del rootLoggerCfg[0]
    else:
      logging.getLogger(logger).setLevel(logging.NOTSET)
    loggers[loggin.getLogger(logger)] = [x.strip() for x in loggerCfg]

  # Now deal with appenders
  for logger, appenders in loggers.items():
    for appender in appenders:
      layout = None
      appenderKey = "log4j.appender."+appender
      appenderClass = props[appenderKey]
      klass = _import_handler(appenderClass)
      handler = klass()
      # Deal with appender options
      appenderOptions = filter(lambda x: x.startswith(appenderKey+"."), props.keys())
      for appenderOption in appenderOptions:
        opt = appenderOption[len(appenderKey+"."):]
        value = props[appenderOption].strip()
        if opt.endswith("layout"):
          layoutClass = value
          klass = _import_layout(layoutClass)
          layout = klass()
          layoutOptions = filter(lambda x: x.startswith(appenderKey+".layout."), props.keys())
          for layoutOption in layoutOptions:
            opt = layoutOption[len(appenderKey+".layout."):]
            value = props[layoutOption].strip()
            setattr(layout, opt, value)
        elif opt.endswith("filter"):
          pass
        elif opt.endswith("errorhandler"):
          pass
        else:
          setattr(handler, opt, value)
      handler.activateOptions()
      logger.addHandler(handler)
      if layout:
        handler.setFormatter(layout)
