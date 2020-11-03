import sys

import boto3
import yaml

client = boto3.client('route53')

TYPE = ['CNAME',
        'A']

ACTION = ['CREATE',
          'DELETE',
          'UPSERT']


def validate(type, action):
    type_val = type.upper() in TYPE
    action_val = action.upper() in ACTION
    return type_val and action_val


def add_cname_record(zone, name, value, action, type, ttl):
    if not validate(type, action):
        print("error in the type or in the action")
        raise sys.exit(2)
    try:
        response = client.change_resource_record_sets(
            HostedZoneId=zone,
            ChangeBatch={
                'Comment': 'add %s -> %s' % (name, value),
                'Changes': [
                    {
                        'Action': action.upper(),
                        'ResourceRecordSet': {
                            'Name': name,
                            'Type': type,
                            'TTL': ttl,
                            'ResourceRecords': [{'Value': value}]
                        }
                    }]
            })
    except Exception as e:
        print(e)


def main():
    with open(r'config.yml') as file:
        domains = yaml.load(file, Loader=yaml.FullLoader)
        for domain in domains:
            add_cname_record(domain.get('zone'), domain.get('domain'), domain.get('value'), domain.get('action'),
                             domain.get('type'), domain.get('ttl'))


if __name__ == "__main__":
    main()
