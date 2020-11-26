import subprocess


cmd = """
awslocal kinesis create-stream \
    --stream-name bexh-outgoing-events \
    --shard-count 1
"""
try:
    print(cmd)
    print(subprocess.getoutput(cmd))
except Exception as e:
    print("topic already exists", e)

cmd = """
awslocal kinesis create-stream \
    --stream-name bexh-outgoing-bets \
    --shard-count 1
"""
try:
    print(cmd)
    print(subprocess.getoutput(cmd))
except Exception as e:
    print("topic already exists", e)

cmd = """
awslocal kinesis create-stream \
    --stream-name bexh-incoming-aggregated-bets \
    --shard-count 1
"""
try:
    print(cmd)
    print(subprocess.getoutput(cmd))
except Exception as e:
    print("topic already exists", e)

cmd = """
awslocal sns create-topic \
    --name bet-status-change-email
"""
try:
    print(cmd)
    print(subprocess.getoutput(cmd))
except Exception as e:
    print("topic already exists", e)

cmd = """
awslocal sns create-topic \
    --name verification-email
"""
try:
    print(cmd)
    print(subprocess.getoutput(cmd))
except Exception as e:
    print("topic already exists", e)

cmd = """
awslocal dynamodb create-table \
    --table-name bexh-outgoing-events-manager \
    --attribute-definitions AttributeName=shard,AttributeType=S \
    --key-schema AttributeName=shard,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
"""
try:
    print(cmd)
    print(subprocess.getoutput(cmd))
except Exception as e:
    print("table already exists", e)

cmd = """
awslocal dynamodb create-table \
    --table-name bexh-outgoing-bets-manager \
    --attribute-definitions AttributeName=shard,AttributeType=S \
    --key-schema AttributeName=shard,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
"""
try:
    print(cmd)
    print(subprocess.getoutput(cmd))
except Exception as e:
    print("table already exists", e)

cmd = """
awslocal dynamodb create-table \
    --table-name bexh-incoming-aggregated-bets-manager \
    --attribute-definitions AttributeName=shard,AttributeType=S \
    --key-schema AttributeName=shard,KeyType=HASH \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1
"""
try:
    print(cmd)
    print(subprocess.getoutput(cmd))
except Exception as e:
    print("table already exists", e)


cmd = "mysql -u user -ppassword -h 127.0.0.1 < scripts/file.sql"
print(cmd)
print(subprocess.getoutput(cmd))
