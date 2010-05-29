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
import sys
import os

##############################################################################
# Map standard log4j appenders to logging handlers
##############################################################################
class ConsoleAppender(logging.StreamHandler,object):

  def __init__(self):
    self.stream = sys.stdout # in log4j stdout is default

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

  # Supported log4j Options
  Target = property(fget=getTarget, fset=setTarget)
  def activateOptions(self):
    logging.StreamHandler.__init__(self, strm=self.stream)

class FileAppender(logging.FileHandler,object):

  def __init__(self):
    pass

  def setFile(self, filename):
    self.filename = filename
    self.baseFilename = os.path.abspath(filename)

  def getFile(self):
    return self.filename

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

  # Supported log4j Options
  Append = property(fget=getAppend, fset=setAppend)
  File = property(fget=getFile, fset=setFile)

  def activateOptions(self):
    logging.FileHandler.__init__(self, self.filename)

class RollingFileAppender(logging.handlers.RotatingFileHandler, object):

  def __init__(self):
    pass

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
  
  def setMaxBackupIndex(self, value):
    self.backupCount = int(value)

  def getMaxBackupIndex(self):
    return str(self.backupCount)

  def setFile(self, filename):
    self.filename = filename
    self.baseFilename = os.path.abspath(filename)

  def getFile(self):
    return self.filename

  # Supported log4j Options
  MaxFileSize = property(fget=getMaxFileSize, fset=setMaxFileSize)
  MaxBackupIndex = property(fget=getMaxBackupIndex, fset=setMaxBackupIndex)
  File = property(fget=getFile, fset=setFile)
  
  def activateOptions(self):
    logging.handlers.RotatingFileHandler.__init__(self, self.filename)

class DailyRollingFileAppender(logging.handlers.TimedRotatingFileHandler, object):
  def __init__(self):
    pass

  def setDatePattern(self, pattern):
    self.pattern = pattern.strip()
    # TODO : support the log4j patterns more accurately and without hardcoding
    if self.pattern == ".yyyy-ww":
      self.when="W0"
    elif self.pattern == ".yyyy-MM-dd":
      self.when="midnight"
    elif self.pattern == ".yyyy-MM-dd-HH":
      self.when="H"
    elif self.pattern == ".yyyy-MM-dd-HH-mm":
      self.when="M"
    elif self.pattern == ".yyyy-MM-dd-HH-mm-ss":
      self.when="S"
    else:
      raise ValueError
 
  def getDatePattern(self):
    return self.pattern

  def setFile(self, filename):
    self.filename = filename
    self.baseFilename = os.path.abspath(filename)

  def getFile(self):
    return self.filename

  # Supported log4j Options
  File = property(fget=getFile, fset=setFile)
  DatePattern = property(fget=getDatePattern, fset=setDatePattern)
  def activateOptions(self):
    logging.handlers.TimedRotatingFileHandler.__init__(self, self.filename, self.when)

class SyslogAppender(logging.handlers.SysLogHandler, object):
  def __init__(self):
    pass

  def setFacility(self, facility):
    self.facility = self.facility_names[facility.lower()]

  def getFacility(self):
    return self.facility

  def setFacilityPrinting(self, facilityprint):
    self.facilityprint = bool(facilityprint)

  def getFacilityPrinting(self):
    return str(self.facilityprint)

  def setSyslogHost(self, sysloghost):
    addr = sysloghost.split(":", 1)
    if len(addr) == 1:
      addr.append(logging.handlers.SYSLOG_UDP_PORT)
    self.address = tuple(addr)
    
  def getSyslogHost(self):
    if len(self.adddress) == 2:
      return "%s:%s" % self.address
    else:
      return self.address[0]

  # Support log4j properites
  Facility = property(fget=getFacility, fset=setFacility)
  SyslogHost = property(fget=getSyslogHost, fset=setSyslogHost)
  def activateOptions(self):
    logging.handlers.SysLogHandler.__init__(self, self.address, self.facility)
