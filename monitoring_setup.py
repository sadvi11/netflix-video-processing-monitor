import boto3
import os
from dotenv import load_dotenv

load_dotenv()

cloudwatch = boto3.client('cloudwatch', region_name='ca-central-1')
sns = boto3.client('sns', region_name='ca-central-1')

def create_dashboard():
    dashboard_body = {
        "widgets": [
            {
                "type": "metric",
                "properties": {
                    "title": "Jobs Started vs Completed vs Failed",
                    "metrics": [
                        ["Netflix/VideoProcessing", "JobsStarted"],
                        ["Netflix/VideoProcessing", "JobsCompleted"],
                        ["Netflix/VideoProcessing", "JobsFailed"]
                    ],
                    "period": 60,
                    "stat": "Sum",
                    "view": "timeSeries"
                }
            },
            {
                "type": "metric",
                "properties": {
                    "title": "Average Quality Score",
                    "metrics": [
                        ["Netflix/VideoProcessing", "QualityScore"]
                    ],
                    "period": 60,
                    "stat": "Average"
                }
            },
            {
                "type": "metric",
                "properties": {
                    "title": "Transcoding Duration",
                    "metrics": [
                        ["Netflix/VideoProcessing", "TranscodingDuration"]
                    ],
                    "period": 60,
                    "stat": "Average"
                }
            }
        ]
    }

    import json
    cloudwatch.put_dashboard(
        DashboardName='Netflix-Video-Processing',
        DashboardBody=json.dumps(dashboard_body)
    )
    print("Dashboard created: Netflix-Video-Processing")

def create_alarm():
    cloudwatch.put_metric_alarm(
        AlarmName='VideoProcessing-HighFailureRate',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=1,
        MetricName='JobsFailed',
        Namespace='Netflix/VideoProcessing',
        Period=300,
        Statistic='Sum',
        Threshold=2.0,
        ActionsEnabled=True,
        AlarmDescription='More than 2 video jobs failed in 5 minutes',
        TreatMissingData='notBreaching'
    )
    print("Alarm created: VideoProcessing-HighFailureRate")

if __name__ == "__main__":
    create_dashboard()
    create_alarm()
    print("\nMonitoring setup complete")
    print("View dashboard at: AWS Console > CloudWatch > Dashboards > Netflix-Video-Processing")
