import boto3
import time
import random
import json
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

cloudwatch = boto3.client('cloudwatch', region_name='ca-central-1')

def publish_metric(metric_name, value, unit='Count', job_id=''):
    cloudwatch.put_metric_data(
        Namespace='Netflix/VideoProcessing',
        MetricData=[{
            'MetricName': metric_name,
            'Value': value,
            'Unit': unit,
            'Dimensions': [
                {'Name': 'JobId', 'Value': job_id},
                {'Name': 'Environment', 'Value': 'production'}
            ]
        }]
    )
    print(f"Published metric: {metric_name} = {value}")

def simulate_video_job(video_name):
    job_id = f"job-{int(time.time())}"
    print(f"\nStarting video processing job: {job_id}")
    print(f"Video: {video_name}")

    # Stage 1 — Upload received
    publish_metric('JobsStarted', 1, job_id=job_id)
    print("Stage 1: Upload received")
    time.sleep(1)

    # Stage 2 — Transcoding
    duration = random.uniform(10, 60)
    publish_metric('TranscodingDuration', duration, 'Seconds', job_id)
    print(f"Stage 2: Transcoding complete — {duration:.1f}s")
    time.sleep(1)

    # Stage 3 — Quality check
    quality_score = random.uniform(0.7, 1.0)
    publish_metric('QualityScore', quality_score, job_id=job_id)
    print(f"Stage 3: Quality score — {quality_score:.2f}")

    # Stage 4 — Success or failure
    if quality_score < 0.75:
        publish_metric('JobsFailed', 1, job_id=job_id)
        print(f"Stage 4: Job FAILED — quality below threshold")
        return False
    else:
        publish_metric('JobsCompleted', 1, job_id=job_id)
        print(f"Stage 4: Job COMPLETED successfully")
        return True

if __name__ == "__main__":
    videos = [
        "Stranger_Things_S5_E01.mp4",
        "The_Crown_S6_E03.mp4",
        "Squid_Game_S2_E01.mp4"
    ]
    for video in videos:
        simulate_video_job(video)
        time.sleep(2)
