from tx_people import models as tx_people

from .. import models


def save(data):
    # TODO: Save source data
    identifier, id_created = tx_people.Identifier.objects.get_or_create(
            **data['tx_people.Identifier'])

    if id_created:
        person = tx_people.Person.objects.create(**data['tx_people.Person'])
        person.identifiers.add(identifier)
    else:
        person = tx_people.Person.objects.get(identifiers__in=[identifier, ])

    # TODO: How should we deal with multiple children?  Right now they
    #       all have one child underneath their parent.
    #
    # TODO: How should we/can we deal with recursive children?
    children = data['tx_people.Organization'].pop('children', [])
    source_department, _ = tx_people.Organization.objects.get_or_create(
            **data['tx_people.Organization'])
    for child in children:
        department, _ = tx_people.Organization.objects.get_or_create(
                parent=source_department, **child)

    # TODO: Remove post entirely
    post, _ = tx_people.Post.objects.get_or_create(organization=department,
            **data['tx_people.Post'])

    membership, _ = tx_people.Membership.objects.get_or_create(
            person=person, organization=department, post=post,
            **data['tx_people.Membership'])

    for compensation in data['compensations']:
        compensation_type, _ = models.CompensationType.objects.get_or_create(
                **compensation['tx_salaries.CompensationType'])
        models.Employee.objects.get_or_create(
            position=membership, compensation_type=compensation_type,
            **compensation['tx_salaries.Employee'])
