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

##############################################################################
# Map standard log4j layouts to logging formatters
##############################################################################
_FORMATTER_TRANS = {"c": ("%(name)", "s"),            # Name of the logger (logging channel)
                    "p": ("%(levelname)", "s"),       # Text logging level for the message ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
                    "F": ("%(filename)", "s"),        # Filename portion of pathname
                    "L": ("%(lineno)", "d"),          # Source line number where the logging call was issued (if available)
                    "M": ("%(funcName)", "s"),        # Function name
                    "r": ("%(relativeCreated)", "d"), # Time in milliseconds when the LogRecord was created, relative to start
                    "t": ("%(thread)", "d"),          # Thread ID (if available)
                    "t": ("%(threadName)", "s"),      # Thread name (if available)
                    "m": ("%(message)", "s"),         # The result of record.getMessage(), computed just as the record is emitted
                    "C": ("", ""),
                    "d": ("%(asctime)", "s"),
                    "l": ("", ""),
                    "n": ("", ""),
                    "x": ("", ""), 
                    "X": ("", ""),
                   }


class PatternLayout(logging.Formatter,object):
  def setConversionPattern(self, pattern):
    self.pattern = pattern
    fmt = []
    # Translate the pattern to python logging formats
    i = 0
    while i < len(pattern):
      if pattern[i] != "%":
        fmt.append(pattern[i])
        i += 1
      else:
        i += 1
        if pattern[i] == "%":
          fmt.append("%%")
        else:
          modifier = []
          while pattern[i] in ("-", ".", '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            modifier.append(pattern[i])
            i += 1
          modifier = "".join(modifier)

          char = pattern[i]
          i += 1
          
          # If it's a date spec, see if there is a custom date format
          if char == "d" and pattern[i] == "{":
            datefmt = []
            i += 1
            while pattern[i] != "}":
              datefmt.append(pattern[i])
              i += 1
            i += 1
            datefmt = "".join(datefmt)
            # TODO : don't ingore the datefmt

          fmt.append(_FORMATTER_TRANS[char][0])
          fmt.append(modifier)
          fmt.append(_FORMATTER_TRANS[char][1])
    self._fmt = "".join(fmt)

  def getConversionPattern(self):
    return pattern
  ConversionPattern = property(fget=getConversionPattern, fset=setConversionPattern)
