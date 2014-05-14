from haystack import indexes
from tx_people.models import *
from tx_salaries.models import *


class EmployeeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='position__person__given_name')
    compensation = indexes.IntegerField(model_attr='compensation', null=True)
    title = indexes.CharField(model_attr='title__name', faceted=True)
    organization = indexes.CharField(model_attr='position__organization__name', faceted=True)
    parent = indexes.CharField(model_attr='position__organization__parent__name', faceted=True)

    def get_model(self):
        return Employee
