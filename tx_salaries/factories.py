import factory
from tx_people.models import Organization, Membership, Person, Post
from tx_salaries.models import Employee, EmployeeTitle, CompensationType, OrganizationStats


# tx_people factories
class OrganizationFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Organization


class PersonFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Person


class PostFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Post
    organization = factory.SubFactory(OrganizationFactory)


class MembershipFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Membership
    person = factory.SubFactory(PersonFactory)
    organization = factory.SubFactory(OrganizationFactory)
    post = factory.SubFactory(PostFactory)


# tx_salaries factories
class CompensationTypeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = CompensationType


class EmployeeTitleFactory(factory.DjangoModelFactory):
    FACTORY_FOR = EmployeeTitle


class EmployeeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Employee
    position = factory.SubFactory(MembershipFactory)
    compensation_type = factory.SubFactory(CompensationTypeFactory)
    title = factory.SubFactory(EmployeeTitleFactory)
    compensation = 1337


class OrganizationStatsFactory(factory.DjangoModelFactory):
    FACTORY_FOR = OrganizationStats