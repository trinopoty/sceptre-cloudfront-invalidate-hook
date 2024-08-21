import uuid
from typing import Optional

from botocore.exceptions import ClientError
from sceptre.hooks import Hook


class InvalidationHook(Hook):

    def __init__(self, *args, **kwargs):
        super(InvalidationHook, self).__init__(*args, **kwargs)

    def run(self):
        argument = self.argument.split(' ')
        argument = [x for x in argument if len(x) > 0]

        if len(argument) < 2:
            raise Exception("Required arguments are missing: distributionIdSpecifier paths...")

        distribution_id = self._find_distribution_id(argument[0])
        if not distribution_id or len(distribution_id) == 0:
            raise Exception("Unable to find CloudFront distribution id for specifier : {}".format(argument[0]))

        paths = argument[1:]

        try:
            tracking_id = str(uuid.uuid4())
            self.stack.connection_manager.call(
                service='cloudfront',
                region='us-east-1',
                command='create_invalidation',
                kwargs={
                    'DistributionId': distribution_id,
                    'InvalidationBatch': {
                        'CallerReference': tracking_id,
                        'Paths': {
                            'Quantity': len(paths),
                            'Items': paths,
                        },
                    },
                })
            print('Triggered invalidations for CloudFront distribution : {}'.format(distribution_id))
        except ClientError as ex:
            raise Exception('Unable to trigger invalidations for CloudFront distribution id : {}'.format(distribution_id), ex)

    def _find_distribution_id(self, distribution: str) -> Optional[str]:
        if distribution.startswith('Resources.'):
            return self._get_distribution_id_from_resources(distribution[len('Resources.'):])
        elif distribution.startswith('Outputs.'):
            return self._get_distribution_id_from_outputs(distribution[len('Outputs.'):])
        else:
            self.logger.info('Trying to interpret %s as distribution id', distribution)
            return distribution

    def _get_distribution_id_from_resources(self, resource_name: str) -> Optional[str]:
        try:
            response = self.stack.connection_manager.call(
                service='cloudformation',
                command='describe_stack_resources',
                kwargs={"StackName": self.stack.external_name}
            )
            resources = response['StackResources']
            for resource in resources:
                if (resource['ResourceType'] == 'AWS::CloudFront::Distribution' and
                        resource['LogicalResourceId'] == resource_name):
                    return resource['PhysicalResourceId']

            return None
        except ClientError as ex:
            self.logger.exception('Unable to get resources for stack: %s', self.stack.external_name)
            return None

    def _get_distribution_id_from_outputs(self, output_name: str) -> Optional[str]:
        try:
            response = self.stack.connection_manager.call(
                service='cloudformation',
                command='describe_stacks',
                kwargs={"StackName": self.stack.external_name}
            )
            outputs = response["Stacks"][0].get("Outputs", {})
            for output in outputs:
                if output['OutputKey'] == output_name:
                    return output['OutputValue']

            return None
        except ClientError as ex:
            self.logger.exception('Unable to get outputs for stack: %s', self.stack.external_name)
            return None
