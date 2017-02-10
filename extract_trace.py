# -*- encoding=utf-8 -*-

TRACE_LIST = [
	# here list trace pattern
]

IGNORE_TRACE_SET = {
	# here list ignore trace pattern
}

UNKNOWN_TRACE = "unknown"
DEFAULT_SPLITTER = "--\n"


def filter_trace_file(trace_file, splitter=DEFAULT_SPLITTER):
	trace_ret = {}
	map(lambda typed_trace: trace_ret.setdefault(typed_trace, []), TRACE_LIST)
	trace_ret.setdefault(UNKNOWN_TRACE, [])

	with open(trace_file) as fd:
		content = fd.read()
		trace_list = content.split(splitter)

		for trace in trace_list:
			if any((t in trace for t in IGNORE_TRACE_SET)):
				continue

			exist = False
			for typed_trace in TRACE_LIST:
				if typed_trace in trace:
					trace_ret[typed_trace].append(trace)
					exist = True

			if not exist:
				trace_ret[UNKNOWN_TRACE].append(trace)

	return trace_ret


def filter_trace_file_list(trace_file_list, splitter=DEFAULT_SPLITTER):

	trace_ret = {}
	for trace_file in trace_file_list:
		trace_ret.update(filter_trace_file(trace_file, splitter))
	return trace_ret


if __name__ == "__main__":

	trace_file_list = [
		# here list trace file
	]
	output_file = "trace.summary"

	trace_summary = filter_trace_file_list(trace_file_list)
	with open(output_file, "w") as fd:
		for trace, trace_list in trace_summary.iteritems():
			if trace == UNKNOWN_TRACE:
				continue
			if not trace_list:
				continue

			fd.write(trace_list[-1] + "\n--\n\nCount: %s\n\n" % len(trace_list))

		unknown_trace = trace_summary.get(UNKNOWN_TRACE, [])
		if unknown_trace:
			fd.write("unknown trace ==================================\n\n")
			for trace in unknown_trace:
				fd.write(trace + "\n--\n\n")
