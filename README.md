# Video hacking with pyav

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Demo

Run demo to clip a video by milliseconds:

```bash
python test/run.py 
```

Example output:

```bash
$ python test/run.py

{'frames_processed': 1,
 'milliseconds_output': 33.333333333333336,
 'milliseconds_per_frame': 0.03333333333333333}

```

Verify the output file using `mediainfo` or `ffprobe`:

```bash
$ mediainfo out.mp4 | grep Duration

Duration                                 : 33 ms
```

```bash
$ ffprobe out.mp4 | grep Duration

Duration: 00:00:00.03, start: 0.066667, bitrate: 22199 kb/s
```

# Usage

```python
from Processor import Processor

processor = Processor()

frames_processed = processor.process(input_path="data/15-seconds.mp4",
                                     output_path="out.mp4",
                                     start=192,
                                     end=200)

pprint(frames_processed)
```
