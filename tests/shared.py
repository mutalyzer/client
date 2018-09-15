import md5
import StringIO


def md5_check(data, md5sum):
    return md5.md5(data).hexdigest() == md5sum
