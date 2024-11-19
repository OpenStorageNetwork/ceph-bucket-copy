# ceph-bucket-copy

Add `osnadmin` user's access key and secret key to the `creds.yaml` file.

```yaml
host1.domain.edu:
  access_key: abc123
  secret_key: def456
host2.domain.edu:
  access_key: ghi789
  secret_key: jkl012
```

Add source and destination bucket names to the `buckets.yaml` file. The source and destination bucket names must be in the `creds.yaml` file.

```yaml
bucket01:
  source: host1.domain.edu
  destination: host2.domain.edu
bucket02:
  source: host1.domain.edu
  destination: host3.domain.edu
```

Run the script to create the users and buckets.

```bash
    pip install -r requirements.txt

    python ./ceph-bucket-copy.py --credentials creds.yaml --buckets buckets.yaml
```

`config_commands.sh` has the commands needed to add the credentials to rclone. `copy_commands.sh` has the commands needed to copy the buckets.

```bash
    bash ./config_commands.sh
    bash ./copy_commands.sh
```