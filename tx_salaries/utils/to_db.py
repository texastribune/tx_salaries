from tx_people import models as tx_people

from .. import models


def save(source_department, data):
    # TODO: Save source data
    identifier, id_created = tx_people.Identifier.objects.get_or_create(
            **data['tx_people.Identifier'])

    if id_created:
        person = tx_people.Person.objects.create(**data['tx_people.Person'])
        person.identifiers.add(identifier)
    else:
        person = tx_people.Person.objects.get(identifiers__in=[identifier, ])

    department, _ = tx_people.Organization.objects.get_or_create(
            parent=source_department, **data['tx_people.Organization'])

    post, _ = tx_people.Post.objects.get_or_create(organization=department,
            **data['tx_people.Post'])

    membership, _ = tx_people.Membership.objects.get_or_create(
            person=person, organization=department, post=post,
            **data['tx_people.Membership'])

    compensation_type, _ = models.CompensationType.objects.get_or_create(
            **data['tx_salaries.CompensationType'])

    compensation, _ = models.Employee.objects.get_or_create(
            position=membership, compensation_type=compensation_type,
            **data['tx_salaries.Employee'])
