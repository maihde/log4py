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
"""
This module intends to provide a log4j/log4cxx compatibility wrapper
for python.  The primary goal is to provide the ability to configure
the built-in python "logging" module using log4j/log4cxx configuration
file.

At this time, there is no intention to fully replicate the log4j/log4cxx
API in python nor provide a wrapper of the log4cxx libraries.
"""
__version__ = "0.1"
