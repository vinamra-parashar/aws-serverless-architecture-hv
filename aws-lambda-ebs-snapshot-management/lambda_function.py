import boto3
from datetime import datetime, timezone, timedelta

ec2 = boto3.client('ec2')

VOLUME_ID = "YOUR_VOLUME_ID"

def lambda_handler(event, context):

    created_snapshot = None
    deleted_snapshots = []

    # Create snapshot
    response = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description="Automated Lambda Snapshot"
    )

    created_snapshot = response['SnapshotId']

    # Tag snapshot
    ec2.create_tags(
        Resources=[created_snapshot],
        Tags=[
            {
                'Key': 'CreatedBy',
                'Value': 'LambdaBackup'
            }
        ]
    )

    print(f"Created Snapshot: {created_snapshot}")

    # Find Lambda-created snapshots
    snapshots = ec2.describe_snapshots(
        OwnerIds=['self'],
        Filters=[
            {
                'Name': 'tag:CreatedBy',
                'Values': ['LambdaBackup']
            }
        ]
    )

    threshold_date = (
        datetime.now(timezone.utc)
        - timedelta(days=30)
    )

    for snapshot in snapshots['Snapshots']:

        if snapshot['StartTime'] < threshold_date:

            snapshot_id = snapshot['SnapshotId']

            ec2.delete_snapshot(
                SnapshotId=snapshot_id
            )

            deleted_snapshots.append(snapshot_id)

            print(
                f"Deleted Snapshot: {snapshot_id}"
            )

    return {
        "statusCode": 200,
        "created_snapshot": created_snapshot,
        "deleted_snapshots": deleted_snapshots
    }
