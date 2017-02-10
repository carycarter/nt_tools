# -*- encoding=utf-8 -*-
import os
import codecs


class StateMachine(object):

	_STATE_INIT = 0
	_STATE_RECORD = 1
	_STATE_ESCAPE = 2
	_STATE_END = 3
	_STATE_COMMENT = 4

	_VALID_QUOTE = ('\'', '\"', "'''", '"""')
	_COMMENT_IN = "#"
	_COMMENT_OUT = "\n"

	def __init__(self):
		super(StateMachine, self).__init__()
		self.__string = ""
		self.__state = self._STATE_INIT
		self.__last_state = None
		self.__current_quote = None

	def append_string(self, s):
		self.__string += s

	def input(self, s):

		if self.__state == self._STATE_INIT:
			if s in self._VALID_QUOTE:
				self.__current_quote = s
				self.__state = self._STATE_RECORD
			elif s == self._COMMENT_IN:
				self.__state = self._STATE_COMMENT
		elif self.__state == self._STATE_RECORD:
			if s == self.__current_quote:
				self.__state = self._STATE_END
			elif s == "\\":
				self.__state = self._STATE_ESCAPE
				self.append_string(s)
			else:
				self.append_string(s)
		elif self.__state == self._STATE_ESCAPE:
			self.__state = self._STATE_RECORD
			self.append_string(s)
		elif self.__state == self._STATE_COMMENT:
			if s == self._COMMENT_OUT:
				self.__state = self._STATE_INIT

	def reset(self):
		self.__string = ""
		self.__state = self._STATE_INIT
		self.__current_quote = None

	def is_end(self):
		return self.__state == self._STATE_END

	def get_string(self):
		return self.__string


def extract_string_from_file(f, ret):
	assert os.path.exists(f)
	assert isinstance(ret, dict)

	st = StateMachine()

	file_string = codecs.open(f, 'r', 'utf-8').read()
	len_string = len(file_string)
	index = 0
	while index < len_string:
		s = file_string[index]

		if s == '\'':
			if index + 2 < len_string and file_string[index: index + 3] == "'''":
				index += 2
				s = "'''"
		elif s == "\"":
			if index + 2 < len_string and file_string[index: index + 3] == '"""':
				index += 2
				s = '"""'
		index += 1

		st.input(s)
		if st.is_end():
			string = st.get_string()
			ret.setdefault(string, set())
			ret[string].add(f)
			st.reset()


def is_number(s):
	try:
		int(s)
	except:
		return False
	return True


def process_string(s):
	processed = s.replace("\t", "").replace('\n', "").replace('\r', "")
	return processed.strip()


if __name__ == "__main__":

	root_dir = r""  # this is root dir
	total_token = dict()

	for parent, dir_names, file_names in os.walk(root_dir):
		for filename in file_names:
			if not filename.endswith(".py"):
				continue

			file_path = os.path.join(parent, filename)
			try:
				extract_string_from_file(file_path, total_token)
			except Exception as ex:
				print "exception file: ", file_path, ex

	with open("server.txt", "w+") as fd:
		for string, source in total_token.iteritems():
			processed = process_string(string)

			if not processed:
				continue

			if is_number(processed):
				continue

			try:
				processed = processed.encode("gb18030")
			except Exception as ex:
				try:
					print "fuck", processed, ex
				except:
					print ex
			finally:
				fd.flush()

			fd.write(processed + "\n")
