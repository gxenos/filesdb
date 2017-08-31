import math
import hashlib
import xxhash
import ssdeep as deep
import os


class FileMetadata:
    def __init__(self, root, file, quick=False):
        full_path = os.path.join(root, file)
        info = os.stat(full_path)

        self.name = file
        self.size = convert_size(info.st_size)
        self.path = os.path.relpath(root)
        if not quick:
            self.md5, self.sha1, self.xx32, self.xx64, self.ssdeep = get_hashes(full_path)
        if "." in file:
            self.basename = file.split(".")[0]
            self.extension = ".".join(file.split(".")[1:])
        else:
            self.basename = file
            self.extension = ""
        permissions = info.st_mode
        self.directory = os.path.split(root)[1]
        self.read = bool(permissions & 0o00400)
        self.write = bool(permissions & 0o00200)
        self.execute = bool(permissions & 0o00100)

    def get_tuple(self):
        return self.name, self.size, self.path, self.md5, self.sha1, self.xx32, self.xx64, self.ssdeep, self.basename, self.extension, self.directory,self.read, self.write, self.execute

    def get_quick_tuple(self):
        return self.name, self.size, self.path, self.basename, self.extension, self.directory, self.read, self.write, self.execute


def convert_size(size_bytes):
    if size_bytes == 0:
        return '0B'
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    size_name_pointer = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, size_name_pointer)
    round_size = round(size_bytes / p, 2)
    return '%s %s' % (round_size, size_name[size_name_pointer])


def get_hashes(file_path):
    with open(file_path, 'rb') as fh:
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        xx32 = xxhash.xxh32()
        xx64 = xxhash.xxh64()
        ssdeep = deep.Hash()
        while True:
            data = fh.read(8192)
            if not data:
                break
            md5.update(data)
            sha1.update(data)
            xx32.update(data)
            xx64.update(data)
            ssdeep.update(data)
    return md5.hexdigest(), sha1.hexdigest(), xx32.hexdigest(), xx64.hexdigest(), ssdeep.digest()
