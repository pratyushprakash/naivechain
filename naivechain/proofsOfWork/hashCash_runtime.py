import hashlib
import re
import argparse
from time import time


def check_runtime(input_str, difficulty, digit):
    i_cntr = 0
    time_start = time()
    re_str_compiled = re.compile('^{}'.format(digit) + '{' + '{}'.format(difficulty) + '}.*')
    hash = hashlib.sha256(input_str.encode('ascii'))
    hash_digest = hash.hexdigest()
    while not bool(re.search(re_str_compiled, hash_digest)):
        input_str += str((i_cntr) % 10)
        i_cntr = i_cntr + 1
        hash = hashlib.sha256(input_str.encode('ascii'))
        hash_digest = hash.hexdigest()
    time_end = time()
    print('Number of digits that were appended to the base string to get the desired hash: {}'.format(i_cntr))
    print('Hash that matched the expected preceding condition: {}'.format(hash_digest))
    print('Time(in seconds) taken to find the hash is: {}'.format(time_end - time_start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-df', '--difficulty', type=int,
                        help='The number of repetitions of the digit in the beginning of the hash.', default=3)
    parser.add_argument('-dg', '--digit', type=int, help='The digit that is to be repeated at the start of the hash.',
                        default=0)
    parser.add_argument('-str', '--stringToHash', type=str,
                        help='The string that is it to be used to hash and whose hash has to fulfill the conditions '
                             'specified as arguments.', default='hello world')
    args_list = parser.parse_args()
    # use the below code to enable for the logging in later instance
    # try:
    #     if not bool(args_list.difficulty):
    #         raise Exception
    #     difficulty = args_list.difficulty
    # except Exception:
    #     difficulty = 3
    # try:
    #     if not bool(args_list.digit):
    #         raise Exception
    #     digit = args_list.digit
    # except Exception:
    #     digit = 0
    # try:
    #     if not bool(args_list.stringToHash):
    #         raise Exception
    #     input_str = args_list.stringToHash
    # except Exception:
    #     input_str = 'hello world'
    # check_runtime(input_str, difficulty, digit)
    check_runtime(args_list.stringToHash, args_list.difficulty, args_list.digit)
