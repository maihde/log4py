#!/usr/bin/env python
# vim: sw=2: et:
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
                    "m": ("%(message)", "s"),        # The result of record.getMessage(), computed just as the record is emitted
                    "C": ("", ""),
                    "d": ("", ""),
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
      char = pattern[i]
      if char == "%":
        i += 1
        char = pattern[i]
        if char == "%":
          fmt.append("%%")
        else:
          modifier = []
          while char in ("-", ".", '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
            modifier.append(char)
            i += 1
            char = pattern[i]
          i += 1
          modifier = "".join(modifier)
          fmt.append(_FORMATTER_TRANS[char][0])
          fmt.append(modifier)
          fmt.append(_FORMATTER_TRANS[char][1])
      else:
        i += 1
        fmt.append(char)
    self._fmt = "".join(fmt)
    print self._fmt 

  def getConversionPattern(self):
    return pattern
  ConversionPattern = property(fget=getConversionPattern, fset=setConversionPattern)
