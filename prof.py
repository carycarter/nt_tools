# -*- encoding=utf-8 -*-
# author: Cary

import os
import time
from datetime import datetime
import psutil


class Info(object):

	def __init__(self, process):
		super(Info, self).__init__()
		self.process = process

	@property
	def process_name(self):
		return self.process.cmdline()[-1]

	@property
	def cpu(self):
		return self.process.cpu_percent()

	@property
	def rss(self):
		rss = self.process.memory_info().rss
		rss = int(rss * 100 / 2 ** 20 + 0.5) / 100.0
		return rss

	def __cmp__(self, other):
		if not isinstance(other, self.__class__):
			return NotImplemented
		return cmp(self.process_name, other.process_name)

	def __str__(self):
		assert self.process is not None
		return "%s/%s" % (self.cpu, self.rss)


class Prof(object):

	INTERVAL = 10

	def __init__(self):
		super(Prof, self).__init__()
		self.process_list = []
		self.file_name = None
		self.__init()

	def __init(self):
		for p in psutil.process_iter():
			cmdline = p.cmdline()
			if p.pid != os.getpid() and len(cmdline) >= 5 and cmdline[3] == "--gamemanager":
				self.process_list.append(Info(p))
				p.cpu_percent()  # first record cpu percentage
		self.process_list.sort()
		self.file_name = "snap_" + datetime.now().strftime('%b_%d_%y_%H_%M_%S') + ".txt"
		self.__write(", ".join([str(proc.process_name) for proc in self.process_list]) + "\n")

	def __write(self, line):
		assert isinstance(line, str)
		assert self.file_name is not None
		with open(self.file_name, 'a') as fd:
			fd.write(line)
		print line

	def __take_snap(self):
		self.__write(", ".join([str(proc) for proc in self.process_list]) + "\n")

	def process(self):
		while True:
			time.sleep(self.INTERVAL)
			self.__take_snap()


def main():
	prof = Prof()
	prof.process()

if __name__ == "__main__":
	main()
