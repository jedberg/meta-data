#!/usr/bin/python

#Copyright (c) 2009,2010,2011 Jeremy Edberg, jedberg@gmail.com
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import sys,urllib2

class _GetchUnix:
    def __init__(self):
        import tty

    def __call__(self):
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


getch = _GetchUnix()

base_url = "http://169.254.169.254/latest/"
url = base_url
factor = 0

while 1:
    try:
        data = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        url = url[0:url.rfind('/')]
        continue
    lines = data.split('\n')[factor:]
    length = len(lines) 
    d = dict(zip(range(1,length+1),lines[:(9+factor)]))

    sys.stdout.write(url.lstrip(base_url) + "\n\n")
    if url != base_url:
        sys.stdout.write("b: [Back]\n")
    for k,v in d.items():
        sys.stdout.write("%d: %s\n" % (k,v))
    if length > 9:
        sys.stdout.write("m: [More]\n")
    if factor > 9:
        sys.stdout.write("l: [Less]\n")
    sys.stdout.write("\n")

    c = getch()
    if c == 'q':
        sys.stdout.write("Come back again soon y'all!\n\n")
        exit(0)
    if c == 'b' and url != base_url:
        url = url[0:url.rfind('/')]
        continue
    if c == 'm' and length > 9:
        factor += 10
        continue
    if c == 'l' and factor > 9:
        factor -= 10
        continue
    try:
        c = int(c)
        try:
            url = url + "/" + d[int(c)]
            factor = 0
        except KeyError:
                sys.stderr.write('Invalid selection\n')        
    except ValueError:
        sys.stdout.write('Please select from above or press "q" to quit\n')

