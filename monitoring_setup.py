import boto3
import json

cloudwatch = boto3.client("cloudwatch", region_name="ca-central-1")

def create_alarm():
    cloudwatch.put_metric_alarm(
        AlarmName="VideoProcessing-HighFailureRate",
        ComparisonOperator="GreaterThanThreshold",
        EvaluationPeriods=1,
        MetricName="JobsFailed",
        Namespace="Netflix/VideoProcessing",
        Period=300,
        Statistic="Sum",
        Threshold=2.0,
        ActionsEnabled=False,
        AlarmDescription="More than 2 video jobs failed in 5 minutes",
        TreatMissingData="notBreaching"
    )
    print("Alarm created: VideoProcessing-HighFailureRate")

if __name__ == "__main__":
    create_alarm()
    print("Setup complete")
    print("Next: run python3 video_processor.py to send metrics")
    print("Then view in AWS Console > CloudWatch > Metrics > Netflix/VideoProcessing")
