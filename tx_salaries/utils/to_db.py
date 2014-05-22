from tx_people import models as tx_people

from .. import models


def save(data):
    save_for_stats = {'organizations': [], 'positions': []}
    # TODO: Save source data
    identifier, id_created = tx_people.Identifier.objects.get_or_create(
        **data['tx_people.Identifier'])

    race, _ = tx_people.Race.objects.get_or_create(**data['tx_people.Race'])

    if id_created:
        person = tx_people.Person.objects.create(**data['tx_people.Person'])
        person.identifiers.add(identifier)
        person.races.add(race)
    else:
        person = tx_people.Person.objects.get(identifiers__in=[identifier, ])

    # TODO: How should we deal with multiple children?  Right now they
    #       all have one child underneath their parent.
    #
    # TODO: How should we/can we deal with recursive children?
    children = data['tx_people.Organization'].pop('children', [])
    source_department, _ = tx_people.Organization.objects.get_or_create(
        **data['tx_people.Organization'])
    save_for_stats['organizations'].append(source_department)
    for child in children:
        department, _ = tx_people.Organization.objects.get_or_create(
            parent=source_department, **child)
        save_for_stats['organizations'].append(department)

    # TODO: Remove post entirely
    post, _ = tx_people.Post.objects.get_or_create(organization=department,
                                                   **data['tx_people.Post'])
    save_for_stats['positions'].append(post)

    membership, _ = tx_people.Membership.objects.get_or_create(
        person=person, organization=department, post=post,
        **data['tx_people.Membership'])

    for compensation in data['compensations']:
        compensation_type, _ = models.CompensationType.objects.get_or_create(
            **compensation['tx_salaries.CompensationType'])
        title, _ = models.EmployeeTitle.objects.get_or_create(
            **compensation['tx_salaries.EmployeeTitle'])
        models.Employee.objects.get_or_create(
            position=membership, compensation_type=compensation_type,
            title=title, **compensation['tx_salaries.Employee'])
    return save_for_stats


def denormalize(data):
    print "Denormalizing %s organizations" % (len(data['organizations']))
    for org in data['organizations']:
        models.OrganizationStats.objects.denormalize(org)

    print "Denormalizing %s positions" % (len(data['positions']))
    for position in data['positions']:
        models.PositionStats.objects.denormalize(position)
