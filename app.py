from flask import Flask, jsonify
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
cloudwatch = boto3.client('cloudwatch', region_name='ca-central-1')

@app.route('/health')
def health():
    return jsonify({"service": "netflix-monitor", "status": "healthy"})

@app.route('/metrics')
def metrics():
    response = cloudwatch.get_metric_statistics(
        Namespace='Netflix/VideoProcessing',
        MetricName='JobsCompleted',
        Dimensions=[],
        StartTime='2026-01-01T00:00:00Z',
        EndTime='2026-12-31T23:59:59Z',
        Period=3600,
        Statistics=['Sum']
    )
    return jsonify({
        "jobs_completed": len(response['Datapoints']),
        "status": "success"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5003)
