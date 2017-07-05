import os
import fnmatch


class dotdict(dict):
	"""dot.notation access to dictionary attributes"""
	__getattr__ = dict.get
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__

	def __dir__(self):
		return self.keys()


def getfoldersize(folder, recurse=False):
	if recurse:
		total_size = 0
		for dirpath, dirnames, filenames in os.walk(folder):
			for f in filenames:
				total_size += os.path.getsize(os.path.join(dirpath, f))
		return total_size
	else:
		return sum(os.path.getsize(os.path.join(folder, f))
				for f in os.listdir(folder))


def format_size(size):
	"""Return file size as string from byte size."""
	for unit in ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB'):
		if size < 2048:
			return "%.f %s" % (size, unit)
		size /= 1024.0


def which(program):
	"""Check if program is exectuable.  Return path to bin if so"""
	def is_exe(fpath):
		return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
	fpath, fname = os.path.split(program)
	if fpath:
		if is_exe(program):
			return program
	else:
		for path in os.environ["PATH"].split(os.pathsep):
			path = path.strip('"')
			exe_file = os.path.join(path, program)
			if is_exe(exe_file):
				return exe_file
	return None


def isexecutable(fpath):
	if os.path.isfile(fpath) and os.access(fpath, os.X_OK):
		return 1
	else:
		return 0


def get_subfolders_containing_filepattern(
	dirname, filepattern='*Settings.txt', exclude=['Corrected']):
	"""retrieve a list of subdirectories of the input directory that contain a
	filepattern... useful for getting raw data directories for batch processing
	"""
	matches = []
	for root, dirnames, filenames in os.walk(dirname):
		for filename in fnmatch.filter(filenames, filepattern):
			if not any([e in root for e in exclude]):
				matches.append(root)
	return matches
