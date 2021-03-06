from Poem.poem_super_admin.models import ProbeHistory, MetricTags
from django.contrib.auth.models import GroupManager, Permission
from django.db import models
from django.utils.translation import ugettext_lazy as _


class MetricTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class MetricType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)

    objects = MetricTypeManager()

    class Meta:
        app_label = 'poem'

    def __str__(self):
        return u'%s' % self.name

    def natural_key(self):
        return (self.name,)


class GroupOfMetrics(models.Model):
    name = models.CharField(_('name'), max_length=80, unique=True)
    permissions = models.ManyToManyField(Permission,
                                         verbose_name=_('permissions'),
                                         blank=True)
    objects = GroupManager()

    class Meta:
        verbose_name = _('Group of metrics')
        verbose_name_plural = _('Groups of metrics')
        app_label = 'poem'

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)


class Metric(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    mtype = models.ForeignKey(MetricType, on_delete=models.CASCADE)
    tags = models.ManyToManyField(MetricTags)
    probekey = models.ForeignKey(ProbeHistory, blank=True, null=True,
                                 on_delete=models.SET_NULL)
    description = models.TextField(default='')
    group = models.ForeignKey(GroupOfMetrics, null=True,
                              on_delete=models.SET_NULL)
    parent = models.CharField(max_length=128)
    probeexecutable = models.CharField(max_length=128)
    config = models.CharField(max_length=1024)
    attribute = models.CharField(max_length=1024)
    dependancy = models.CharField(max_length=1024)
    flags = models.CharField(max_length=1024)
    files = models.CharField(max_length=1024)
    parameter = models.CharField(max_length=1024)
    fileparameter = models.CharField(max_length=1024)

    class Meta:
        permissions = (('metricsown', 'Read/Write/Modify'),)
        app_label = 'poem'
        verbose_name = 'Metric'

    def __str__(self):
        return u'%s' % self.name
