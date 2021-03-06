from tx_people import models as tx_people

from .. import models

RACE_STORE = {}
TITLE_STORE = {}


def save(data):
    """
    Unpack and save each of the items in a structured record from a transformer

    Returns an object of the organizations and positions that it saved
    so they can be denormalized at the end of the import.
    """
    save_for_stats = {'organizations': set(), 'positions': set()}

    # TODO: Save source data
    identifier, id_created = tx_people.Identifier.objects.get_or_create(
        **data['tx_people.Identifier'])

    link, link_created = tx_people.Link.objects.get_or_create(
        **data['tx_people.Links'])

    if data['tx_people.Race']['name'] in RACE_STORE:
        race = RACE_STORE[data['tx_people.Race']['name']]
    else:
        race, _ = tx_people.Race.objects.get_or_create(
            **data['tx_people.Race'])
        RACE_STORE[race.name] = race

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
    source_department.links.add(link)
    save_for_stats['organizations'].add(source_department)
    for child in children:
        department, _ = tx_people.Organization.objects.get_or_create(
            parent=source_department, **child)
        save_for_stats['organizations'].add(department)

    # TODO: Remove post entirely
    post, _ = tx_people.Post.objects.get_or_create(
        organization=department, **data['tx_people.Post'])

    save_for_stats['positions'].add(post)

    membership, _ = tx_people.Membership.objects.get_or_create(
        person=person, organization=department, post=post,
        **data['tx_people.Membership'])

    for compensation in data['compensations']:
        compensation_type, _ = models.CompensationType.objects.get_or_create(
            **compensation['tx_salaries.CompensationType'])

        if compensation['tx_salaries.EmployeeTitle']['name'] in TITLE_STORE:
            title = TITLE_STORE[
                compensation['tx_salaries.EmployeeTitle']['name']]
        else:
            title, _ = models.EmployeeTitle.objects.get_or_create(
                **compensation['tx_salaries.EmployeeTitle'])
            TITLE_STORE[compensation[
                'tx_salaries.EmployeeTitle']['name']] = title

        emp, _ = models.Employee.objects.get_or_create(
            position=membership, compensation_type=compensation_type,
            title=title, **compensation['tx_salaries.Employee'])

    return save_for_stats


def denormalize(data):
    date_provided = data['date_provided']
    print "Denormalizing %s organizations" % (len(data['organizations']))
    for org in data['organizations']:
        models.OrganizationStats.objects.denormalize(org, date_provided)

    print "Denormalizing %s positions" % (len(data['positions']))
    for position in data['positions']:
        models.PositionStats.objects.denormalize(position, date_provided)
