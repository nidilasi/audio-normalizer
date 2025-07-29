# audio-normalizer
Python script to normalize mp3/m4a files in a folder (recursively)

# Usage
```bash
python3 normalize.py /path/to/music/folder [--target-dbfs DBFS] 
```

# Installing dependencies
`audio-normalizer` depends on the python package [pydub](https://github.com/jiaaro/pydub?tab=readme-ov-file#installation) and [ffmpeg](https://github.com/jiaaro/pydub?tab=readme-ov-file#getting-ffmpeg-set-up)

# Known Issues
- Processed files might display the double track length.
