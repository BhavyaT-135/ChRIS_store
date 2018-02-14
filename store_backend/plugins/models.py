
from django.db import models
import django_filters

from rest_framework.filters import FilterSet

from django.conf import settings
import swiftclient


# API types
TYPE_CHOICES = [("string", "String values"), ("float", "Float values"),
                ("boolean", "Boolean values"), ("integer", "Integer values"),
                ("path", "Path values")]

# table of equivalence between front-end types and back-end types
TYPES = {'string': 'str', 'integer': 'int', 'float': 'float', 'boolean': 'bool',
         'path': 'path'}

PLUGIN_TYPE_CHOICES = [("ds", "Data plugin"), ("fs", "Filesystem plugin")]


class Plugin(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True)
    dock_image = models.CharField(max_length=500)
    type = models.CharField(choices=PLUGIN_TYPE_CHOICES, default='ds', max_length=4)
    authors = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=400, blank=True)
    category = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=800, blank=True)
    documentation = models.CharField(max_length=800, blank=True)
    license = models.CharField(max_length=50, blank=True)
    version = models.CharField(max_length=10, blank=True)

    class Meta:
        ordering = ('type',)

    def __str__(self):
        return self.name

    def get_plugin_parameter_names(self):
        """
        Custom method to get the list of plugin parameter names.
        """
        params = self.parameters.all()
        return [param.name for param in params]
    

class PluginFilter(FilterSet):
    min_creation_date = django_filters.DateFilter(name="creation_date", lookup_expr='gte')
    max_creation_date = django_filters.DateFilter(name="creation_date", lookup_expr='lte')
    
    class Meta:
        model = Plugin
        fields = ['name', 'dock_image', 'type', 'category', 'authors',
                  'min_creation_date', 'max_creation_date', ]


class PluginParameter(models.Model):
    name = models.CharField(max_length=100)
    optional = models.BooleanField(default=True)
    default = models.CharField(max_length=200, blank=True)
    type = models.CharField(choices=TYPE_CHOICES, default='string', max_length=10)
    help = models.TextField(blank=True)
    plugin = models.ForeignKey(Plugin, on_delete=models.CASCADE,
                               related_name='parameters')
    
    class Meta:
        ordering = ('plugin',)

    def __str__(self):
        return self.name
    
