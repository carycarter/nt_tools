# -*- encoding=utf-8 -*-
# author: Cary

import os
import time
from datetime import datetime

COMMAND = "ps ax -o %cpu,vsz,rss,command | grep gamemanager"
INTERVAL = 10
FILE_NAME = None


class Info(object):

	PROC_TYPES = ["gamemanager", "dbmanager", "game", "gate"]

	def __init__(self, line):
		super(Info, self).__init__()
		self.line = line
		self.process = None
		self.cpu = None
		self.vsz = None
		self.rss = None

	def parse(self):
		info = self.line.split()
		process_type = info[-2][2:]
		if process_type not in self.PROC_TYPES:
			return False
		self.process = info[-1]
		self.cpu = info[0]
		self.vsz = int(int(info[1]) * 100 / 1024.0 + 0.5) / 100.0
		self.rss = int(int(info[2]) * 100 / 1024.0 + 0.5) / 100.0
		return True

	def __cmp__(self, other):
		if not isinstance(other, self.__class__):
			return NotImplemented
		return cmp(self.process, other.process)

	def __str__(self):
		assert self.process is not None
		return "%s/%s" % (self.cpu, self.rss)


class Helper(object):

	@staticmethod
	def process():
		global FILE_NAME

		snap = []
		with os.popen(COMMAND) as proc:
			for line in proc.readlines():
				info = Info(line)
				if not info.parse():
					continue
				snap.append(info)
		snap.sort()

		def write(line):
			assert isinstance(line, str)
			with open(FILE_NAME, 'a') as fd:
				fd.write(line)
			print line

		if not FILE_NAME:
			FILE_NAME = "snap_" + datetime.now().strftime('%b_%d_%y_%H_%M_%S') + ".txt"
			write(", ".join([str(proc.process) for proc in snap]) + "\n")
		write(", ".join([str(proc) for proc in snap]) + "\n")


def main():

	while True:
		Helper.process()
		time.sleep(INTERVAL)


if __name__ == "__main__":
	main()
