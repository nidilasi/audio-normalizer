# audio-normalizer
Python script to normalize music files in a folder (recursively).
Set the [dBFS](https://en.wikipedia.org/wiki/DBFS) of all files in the given path.

## Supported file types
- mp3
- m4a

# Usage
```bash
pip3 install -r requirements.txt
python3 normalize.py /path/to/music/folder [--target-dbfs DBFS] 
```

# Dependencies
`audio-normalizer` depends on the python package [pydub](https://github.com/jiaaro/pydub?tab=readme-ov-file#installation) and [ffmpeg](https://github.com/jiaaro/pydub?tab=readme-ov-file#getting-ffmpeg-set-up)

# Known Issues
- Processed files might display the double track length (at least in iTunes)
