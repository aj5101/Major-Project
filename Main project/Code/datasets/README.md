# ASL Video Datasets

This directory is for storing ASL video datasets used by the platform.

## Supported Datasets

### WLASL (Word-Level American Sign Language)
- **Source**: [WLASL Dataset](https://github.com/dxli94/WLASL)
- **Format**: Videos organized by gloss
- **Preprocessing**: Use `process_asl_videos.py` to import

### ASL Lexicon
- **Source**: Various ASL lexicon resources
- **Format**: Videos with gloss annotations
- **Preprocessing**: Use `process_asl_videos.py` to import

## Dataset Structure

```
datasets/
├── wlasl/
│   ├── gloss1/
│   │   ├── video1.mp4
│   │   └── video2.mp4
│   └── gloss2/
│       └── video1.mp4
└── custom/
    └── ...
```

## Importing Datasets

1. Download dataset to this directory
2. Run preprocessing script:

```bash
python dataset_preprocessing/process_asl_videos.py \
    --dataset_path datasets/wlasl \
    --gloss_file datasets/wlasl/gloss_mapping.json
```

## Gloss Mapping File Format

### JSON Format
```json
{
    "video1.mp4": "hello",
    "video2.mp4": "world"
}
```

### CSV Format
```csv
filename,gloss
video1.mp4,hello
video2.mp4,world
```

## Notes

- Videos are automatically validated during import
- Embeddings are generated for similarity search
- Duplicate glosses are handled (keeps first occurrence)
- Invalid videos are skipped with warnings

