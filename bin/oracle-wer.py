#!/usr/bin/env python3

# Copyright 2012-2018 Ben Lambert

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import gzip
import asr_tools.evaluation_util
# import matplotlib.pyplot as plt

from asr_tools.io import open_file_stream
from asr_tools.kaldi import read_nbest_file
from asr_tools.kaldi import read_transcript_table
from asr_tools.nbest_util import evaluate_nbests
from asr_tools.nbest_util import evaluate_nbests_oracle
from asr_tools.nbest_util import evals_by_depth

def main():
    """Main method for computing Oracle WER."""
    parser = argparse.ArgumentParser()
    parser.add_argument("nbest_file", type=open_file_stream, help='A file containing n-best lists.  Read as a gzip file if filename ends with .gz')
    parser.add_argument("ref_file", type=argparse.FileType('r'))
    # parser.add_argument('--plot', '-p', default=False, action='store_true')

    args = parser.parse_args()

    print('Reading n-best lists...')    
    nbests = list(read_nbest_file(args.nbest_file))
    print('# of nbests: {}'.format(len(nbests)))
    print('Reading transcripts...')
    refs = read_transcript_table(args.ref_file)
    asr_tools.evaluation_util.REFERENCES = refs

    # This is the slow part.
    print('Running evaluation...')
    overall_eval = evaluate_nbests(nbests)
    print('Overall eval:')
    print(overall_eval)
    print()
    print('Computing oracle eval...')
    print('Oracle eval:')
    print(evaluate_nbests_oracle(nbests))

    evals = evals_by_depth(nbests)
    wers = list(map(lambda x: x.wer(), evals))

    # if args.plot:
    #     plt.plot(wers)
    #     plt.ylim(ymin=0)
    #     plt.show()

    args.nbest_file.close()

if __name__ == "__main__":
    main()
