import calendar

from flask_appbuilder import ModelView
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface

from . import appbuilder, db
from .models import Contact, ContactGroup, Gender, vyrobek, Sklad

def fill_gender():
    try:
        db.session.add(Gender(name="Male"))
        db.session.add(Gender(name="Female"))
        db.session.commit()
    except Exception:
        db.session.rollback()


class VyrobekModelView(ModelView):
    datamodel = SQLAInterface(vyrobek)
    list_columns = ["nazev", "serial_number"]

class SkladModelView(ModelView):
    datamodel = SQLAInterface(Sklad)
    list_columns = ["nazev", "datum", "ks", "stav"]

appbuilder.add_view(
    VyrobekModelView, "Product Catalog", icon="fa-cube", category="Inventory"
)

appbuilder.add_view(
    SkladModelView, "Warehouse Management", icon="fa-warehouse", category="Inventory"
)    

class ContactModelView(ModelView):
    datamodel = SQLAInterface(Contact)

    list_columns = ["name", "personal_celphone", "birthday", "contact_group.name"]

    base_order = ("name", "asc")
    show_fieldsets = [
        ("Basic Information", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Contact Details",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                ],
                "expanded": True,
            },
        ),
    ]

    add_fieldsets = [
        ("Basic Information", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Contact Details",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                ],
                "expanded": True,
            },
        ),
    ]

    edit_fieldsets = [
        ("Basic Information", {"fields": ["name", "gender", "contact_group"]}),
        (
            "Contact Details",
            {
                "fields": [
                    "address",
                    "birthday",
                    "personal_phone",
                    "personal_celphone",
                ],
                "expanded": True,
            },
        ),
    ]


class GroupModelView(ModelView):
    datamodel = SQLAInterface(ContactGroup)
    related_views = [ContactModelView]


def pretty_month_year(value):
    return calendar.month_name[value.month] + " " + str(value.year)


def pretty_year(value):
    return str(value.year)


class ContactTimeChartView(GroupByChartView):
    datamodel = SQLAInterface(Contact)

    chart_title = "Birthday Analytics Dashboard"
    chart_type = "ColumnChart"
    label_columns = ContactModelView.label_columns
    definitions = [
        {
            "group": "month_year",
            "formatter": pretty_month_year,
            "series": [(aggregate_count, "group")],
        },
        {
            "group": "year",
            "formatter": pretty_year,
            "series": [(aggregate_count, "group")],
        },
    ]


db.create_all()
fill_gender()
appbuilder.add_view(
    GroupModelView,
    "Manage Groups",
    icon="fa-users",
    category="People Management",
    category_icon="fa-address-book",
)
appbuilder.add_view(
    ContactModelView, "Directory", icon="fa-user", category="People Management"
)
appbuilder.add_separator("People Management")
appbuilder.add_view(
    ContactTimeChartView,
    "Analytics Dashboard",
    icon="fa-chart-bar",
    category="People Management",
)
