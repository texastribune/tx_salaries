from haystack import indexes
from tx_people.models import Organization
from tx_salaries.models import Employee


class EmployeeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='position__person__name')
    compensation = indexes.FloatField(model_attr='compensation', null=True)
    title = indexes.CharField(model_attr='title__name', faceted=True)
    department = indexes.CharField(model_attr='position__organization__name', faceted=True)
    entity = indexes.CharField(model_attr='position__organization__parent__name', faceted=True)

    def get_model(self):
        return Employee
