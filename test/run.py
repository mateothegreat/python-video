import sys
from os.path import abspath, join, dirname
from pprint import pprint

sys.path.insert(0, abspath(join(dirname(__file__), '../src')))

from Processor import Processor

processor = Processor()

frames_processed = processor.process(input_path="data/15-seconds.mp4",
                                     output_path="out.mp4",
                                     start=0,
                                     end=5)

pprint(frames_processed)
