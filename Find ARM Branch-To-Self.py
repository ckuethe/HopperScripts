# This script marks branch-to-self (0xe7fe) instructions. These are often
# used to wait for an event such as an interrupt.
# Based off of the "Create Procedures ARM" script by bradenthomas@me.com

import time

# main loop
doc = Document.getCurrentDocument()
start_time = time.clock()
nsegs = doc.getSegmentCount()
n = 0

for seg_id in range(0, nsegs):
	doc.log("scanning segment %d/%d" % (seg_id+1, nsegs))
	seg = doc.getSegment(seg_id)

	seg_start = seg.getStartingAddress()
	seg_len = seg.getLength()
	seg_stop = seg_start + seg_len

	# thumb instructions are 2-byte aligned
	if seg_start % 2 == 1:
		seg_start += 1
		seg_len -= 1

	for addr in range(seg_start, seg_stop):
		i = addr - seg_start
		if (i % 10000 == 0):
			doc.log("%.1f%% " % (i * 100.0 / seg_len) )

		x = seg.readByte(addr) & 0xff
		y = seg.readByte(addr+1) & 0xff
		if ((x == 0xe7) and (y ==0xfe)): # Branch to self
			seg.setNameAtAddress(addr, "loc_%x_bts" % addr)
			seg.markAsCode(addr)
			doc.log("loc_%x_bts" % addr)
			n += 1

		addr += 2

doc.refreshView()
elapsed = (time.clock() - start_time)
doc.log("found %d branch-to-self in %0.1f seconds" % (n, elapsed))
