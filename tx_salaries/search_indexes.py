from haystack import indexes
from tx_salaries.models import Employee


class EmployeeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='position__person__name')
    compensation = indexes.FloatField(model_attr='compensation', null=True)
    title = indexes.CharField(model_attr='position__post__label', faceted=True)
    title_slug = indexes.CharField(model_attr='position__post__stats__slug', faceted=True)
    department = indexes.CharField(model_attr='position__organization__name', faceted=True)
    department_slug = indexes.CharField(model_attr='position__organization__stats__slug')
    entity = indexes.CharField(model_attr='position__organization__parent__name', faceted=True)
    entity_slug = indexes.CharField(model_attr='position__organization__parent__stats__slug')

    def get_model(self):
        return Employee

    def get_updated_field(self):
        return 'updated'
