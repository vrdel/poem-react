from configparser import ConfigParser

from Poem.poem import models as poem_models
from Poem.tenants.models import Tenant
from django.conf import settings
from django.core.management.base import BaseCommand
from tenant_schemas.utils import schema_context, get_public_schema_name


def create_groups_of_resources(tenant_name):
    schema = tenant_name.lower()
    group = tenant_name.upper()
    with schema_context(schema):
        poem_models.GroupOfAggregations.objects.create(name=group)
        poem_models.GroupOfMetrics.objects.create(name=group)
        poem_models.GroupOfMetricProfiles.objects.create(name=group)
        poem_models.GroupOfThresholdsProfiles.objects.create(name=group)


def create_tenant(name, hostname):
    # if tenant is created for the public schema, tenant name is 'all',
    # otherwise tenant name is the same as schema name
    if name == 'all':
        schema = 'public'
    else:
        schema = name.lower()
    tenant = Tenant(domain_url=hostname, schema_name=schema, name=name)
    tenant.save()

    if schema != get_public_schema_name():
        create_groups_of_resources(name)


def get_public_schema_hostname():
    config = ConfigParser()
    config.read(settings.CONFIG_FILE)

    hostname = config.get('GENERAL_ALL', 'publicpage')

    return hostname


class Command(BaseCommand):
    help = """Create a new tenant with given name"""

    def add_arguments(self, parser):
        parser.add_argument('--name', required=True, type=str)
        parser.add_argument('--hostname', nargs='?', type=str)

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        if kwargs['hostname']:
            hostname = kwargs['hostname']
        else:
            hostname = get_public_schema_hostname()
        create_tenant(name, hostname)
