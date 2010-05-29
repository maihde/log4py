#!/usr/bin/env python
# vim: sw=2: et:
import logging, logging.handlers
import sys
import os

##############################################################################
# Map standard log4j appenders to logging handlers
##############################################################################
class ConsoleAppender(logging.StreamHandler,object):
  def __init__(self):
    logging.StreamHandler.__init__(self, strm=sys.stdout) # in log4j stdout is default

  def setTarget(self, target):
    if target == "System.out":
      self.stream = sys.stdout
    elif target == "System.err":
      self.stream = sys.stderr

  def getTarget(self):
    if self.stream == sys.stdout:
      return "System.out"
    elif self.stream == sys.stderr:
      return "System.err"
  Target = property(fget=getTarget, fset=setTarget)

  def activateOptions(self):
    pass

class FileAppender(logging.FileHandler,object):
  def __init__(self):
    logging.FileHandler.__init__(self, "", delay=True) # in log4j stdout is default

  def activateOptions(self):
    self._open()

  def setFile(self, filename):
    self.filename = filename
    self.baseFilename = os.path.abspath(filename)

  def getFile(self):
    return self.filename
  File = property(fget=getFile, fset=setFile)

  def setAppend(self, append):
    if bool(append):
      self.mode = "a"
    else:
      self.mode = "w"

  def getAppend(self):
    if self.mode == "a":
      return "true"
    else:
      return "false"
  Append = property(fget=getAppend, fset=setAppend)

class RollingFileAppender(logging.handlers.RotatingFileHandler, object):
  def __init__(self):
    logging.handlers.RotatingFileHandler.__init__(self, "", delay=True)

  def setMaxFileSize(self, value):
      # In configuration files, the MaxFileSize option takes an long integer in
      # the range 0 - 2^63. You can specify the value with the suffixes "KB",
      # "MB" or "GB" so that the integer is interpreted being expressed
      # respectively in kilobytes, megabytes or gigabytes. For example, the
      # value "10KB" will be interpreted as 10240.
      value = value.strip()
      suffix = value[-2:]
      multiplier = 1
      if suffix == "KB":
        multiplier = 1024
        value = int(value[:-2]) * multiplier
      elif suffix == "MB":
        multiplier = 1024 * 1024
        value = int(value[:-2]) * multiplier
      elif suffix == "GB":
        multiplier = 1024 * 1024 * 1024
        value = int(value[:-2]) * multiplier
      else:
        value = int(value)
      self.maxBytes = value


  def getMaxFileSize(self):
    return str(self.maxBytes)
  MaxFileSize = property(fget=getMaxFileSize, fset=setMaxFileSize)
  
  def setMaxBackupIndex(self, value):
    self.backupCount = int(value)
  def getMaxBackupIndex(self):
    return str(self.backupCount)
  MaxBackupIndex = property(fget=getMaxBackupIndex, fset=setMaxBackupIndex)
  
  def setFile(self, filename):
    self.filename = filename
    self.baseFilename = os.path.abspath(filename)

  def getFile(self):
    return self.filename
  File = property(fget=getFile, fset=setFile)
  
  def activateOptions(self):
    self._open()

class DailyRollingFileAppender(logging.handlers.RotatingFileHandler, object):
  def __init__(self):
    logging.handlers.RotatingFileHandler.__init__(self, "", delay=True)

  def setMaxFileSize(self, value):
      # In configuration files, the MaxFileSize option takes an long integer in
      # the range 0 - 2^63. You can specify the value with the suffixes "KB",
      # "MB" or "GB" so that the integer is interpreted being expressed
      # respectively in kilobytes, megabytes or gigabytes. For example, the
      # value "10KB" will be interpreted as 10240.
      value = value.strip()
      suffix = value[-2:]
      multiplier = 1
      if suffix == "KB":
        multiplier = 1024
        value = int(value[:-2]) * multiplier
      elif suffix == "MB":
        multiplier = 1024 * 1024
        value = int(value[:-2]) * multiplier
      elif suffix == "GB":
        multiplier = 1024 * 1024 * 1024
        value = int(value[:-2]) * multiplier
      else:
        value = int(value)
      self.maxBytes = value


  def getMaxFileSize(self):
    return str(self.maxBytes)
  MaxFileSize = property(fget=getMaxFileSize, fset=setMaxFileSize)
  
  def setMaxBackupIndex(self, value):
    self.backupCount = int(value)
  def getMaxBackupIndex(self):
    return str(self.backupCount)
  MaxBackupIndex = property(fget=getMaxBackupIndex, fset=setMaxBackupIndex)
  
  def setFile(self, filename):
    self.filename = filename
    self.baseFilename = os.path.abspath(filename)

  def getFile(self):
    return self.filename
  File = property(fget=getFile, fset=setFile)
  
  def activateOptions(self):
    self._open()
