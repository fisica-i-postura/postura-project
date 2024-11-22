from globals.bulk_processor import bulk_process_videos

if __name__ == '__main__':
    bulk_process_videos()

# if __name__ == '__main__':
#     for video in get_videos_paths():
#         cap = cv2.VideoCapture(video)
#         df = pd.read_csv(PathHelper(Path(video)).get_csv_path())
#         metadata = VideoMetadata((1920, 1080), 1/0.0019805559026734917)
#         analysis = VideoAnalysis(metadata, df)
#         display(video, analysis, None)