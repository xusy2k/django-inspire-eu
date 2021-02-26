# Standard Library
import logging

import feedparser
import requests
from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
from slugify import slugify

from ...models import ApplicationSchema, CodeList, CodeListValue, Status, Theme

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load initial data"
    base_url = "https://inspire.ec.europa.eu"
    debug_console = None

    def add_arguments(self, parser):
        parser.add_argument(
            "-l",
            "--language",
            type=str,
            help=_("Language (default: en)"),
        )

    def populate_status(self, language):
        if self.debug_console:
            print("*********************")
            print("* Populating Status *")
            print("*********************")
        status_list = [
            {
                "link": "https://inspire.ec.europa.eu/registry/status/valid",
                "label": _("Valid"),
                "definition": _(
                    "The item has been accepted, is recommended for use, and has not been "
                    "superseded or retired.",
                ),
                "is_valid": True,
            },
            {
                "link": "https://inspire.ec.europa.eu/registry/status/invalid",
                "label": _("Invalid"),
                "definition": _(
                    "A decision has been made that a previously valid register item contains a substantial "
                    "error and is invalid, and will normally have been replaced by a corrected item.",
                ),
                "is_valid": False,
            },
            {
                "link": "https://inspire.ec.europa.eu/registry/status/retired",
                "label": _("Retired"),
                "definition": _(
                    "A decision has been made that the item is no longer recommended for use. "
                    "It has not been superseded by another item.",
                ),
                "is_valid": False,
            },
        ]
        for status_dict in status_list:
            update = False
            code = status_dict["link"].split("/")[-1]
            try:
                status = Status.objects.get(slug=slugify(code))
            except Status.DoesNotExist:
                status = Status(code=code)
                update = True

            for key, value in status_dict.items():
                # value = status_dict[key]
                if getattr(status, key) != value:
                    setattr(status, key, value)
                    update = True
            if update:
                status.save()
                if self.debug_console:
                    print(f"Updated status: '{status}'")

        print("End Populating Status")
        print("")

    def populate_themes(self, language):
        if self.debug_console:
            print("********************")
            print("* Populating Theme *")
            print("********************")
        response = requests.get(url=f"{self.base_url}/theme/theme.{language}.json")
        data = response.json()
        themes = data["register"]["containeditems"]
        for theme_dict in themes:
            theme_json = theme_dict["theme"]
            code = theme_json["id"].split("/")[-1]
            row = dict({"code": code, "link": theme_json["id"]})
            try:
                status = Status.objects.get(
                    slug=slugify(theme_json["status"]["id"].split("/")[-1]),
                )
            except Status.DoesNotExist:
                status_link = theme_json["status"]["id"]
                try:
                    status_label = theme_json["status"]["label"]["text"]
                except KeyError:
                    status_label = status_link
                status = Status(link=status_link, label=status_label)
                status.save()
            row["status"] = status
            try:
                row["version"] = int(theme_json["version"])
            except (TypeError, ValueError):
                msg = _(f"""{row["code"]} Version inválida: {theme_json["version"]}""")
                log.warning(msg)
                row["version"] = 0

            for f in ["label", "definition", "description"]:
                try:
                    row[f] = theme_json[f]["text"].strip()
                except KeyError:
                    row[f] = ""

            update = False
            try:
                theme = Theme.objects.get(code=code)
            except Theme.DoesNotExist:
                theme = Theme(code=code, status=status)
                update = True

            for f in ["link", "version", "label", "definition", "description"]:
                if getattr(theme, f) != row[f]:
                    setattr(theme, f, row[f])
                    update = True

            if update:
                theme.save()
                if self.debug_console:
                    print(f"Updated Theme '{theme}'")

        print("End Populating Theme")
        print("")

    def populate_schemas(self, language):
        if self.debug_console:
            print("*********************************")
            print("* Populating Application Schema *")
            print("*********************************")
        response = requests.get(
            url=f"{self.base_url}/applicationschema/applicationschema.{language}.json",
        )
        data = response.json()
        schemas = data["register"]["containeditems"]
        for schema_dict in schemas:
            schema_json = schema_dict["applicationschema"]
            code = schema_json["id"].split("/")[-1]
            row = dict({"code": code, "link": schema_json["id"]})
            try:
                status = Status.objects.get(
                    slug=slugify(schema_json["status"]["id"].split("/")[-1]),
                )
            except Status.DoesNotExist:
                status_link = schema_json["status"]["id"]
                try:
                    status_label = schema_json["status"]["label"]["text"].strip()
                except KeyError:
                    status_label = status_link
                status = Status(link=status_link, label=status_label)
                status.save()
            row["status"] = status
            try:
                row["version"] = int(schema_json["version"])
            except (TypeError, ValueError):
                msg = _(f"""{row["code"]} Version inválida: {schema_json["version"]}""")
                log.warning(msg)
                row["version"] = 0

            for f in ["label", "definition", "description"]:
                try:
                    row[f] = schema_json[f]["text"].strip()
                except KeyError:
                    row[f] = ""

            update = False
            try:
                schema = ApplicationSchema.objects.get(slug=slugify(code))
            except ApplicationSchema.DoesNotExist:
                schema = ApplicationSchema(code=code, status=status)
                update = True

            for f in ["link", "version", "label", "definition", "description"]:
                if getattr(schema, f) != row[f]:
                    setattr(schema, f, row[f])
                    update = True

            if update:
                schema.save()
                if self.debug_console:
                    print(f"Updated Application Schema: '{schema}'")

            try:
                for theme_json in schema_json["themes"]:
                    theme_dict = theme_json["theme"]
                    theme_code = theme_dict["id"].split("/")[-1]
                    try:
                        theme = Theme.objects.get(slug=slugify(theme_code))
                    except Theme.DoesNotExist:
                        theme_link = theme_dict["id"]
                        try:
                            theme_label = theme_dict["label"]["text"]
                        except KeyError:
                            theme_label = theme_link
                        theme = Theme(link=theme_link, label=theme_label, status=status)
                        theme.save()

                    if theme not in schema.themes.all():
                        schema.themes.add(theme)
            except KeyError:
                theme = None
        print("End Application Schema")
        print("")

    def populate_code_list(self, language):
        if self.debug_console:
            print("***********************")
            print("* Populating CodeList *")
            print("***********************")
        url = f"{self.base_url}/codelist/codelist.{language}.atom"

        if self.debug_console:
            print(f">>> Fetching {url}")
        response = requests.get(url=url)
        fp = feedparser.parse(response.text)
        status = Status.objects.get(slug="valid")
        for entry in fp.entries:
            code = entry["id"].split("/")[-1]
            row = dict({"code": code})
            row["link"] = entry["link"].strip()
            row["label"] = entry["title"].strip()
            row["definition"] = entry["summary"].strip()
            try:
                row["description"] = entry["content"][0]["value"]
            except KeyError:
                row["description"] = ""

            themes = []
            row["application_schema"] = None
            for entry_link in entry["links"]:
                if entry_link["rel"] == "self":
                    continue
                elif entry_link["rel"] == "up":
                    if entry_link["href"] == "http://inspire.ec.europa.eu/codelist":
                        continue
                    else:
                        raise Exception("Check!")
                elif entry_link["rel"] == "related":
                    if "theme" in entry_link["href"]:
                        theme_slug = slugify(entry_link["href"].split("/")[-1])
                        try:
                            themes.append(Theme.objects.get(slug=theme_slug))
                        except Theme.DoesNotExist:
                            pass
                    elif "applicationschema" in entry_link["href"]:
                        schema_slug = slugify(entry_link["href"].split("/")[-1])
                        try:
                            row["application_schema"] = ApplicationSchema.objects.get(
                                slug=schema_slug,
                            )
                        except ApplicationSchema.DoesNotExist:
                            pass

            update = False
            try:
                code_list = CodeList.objects.get(slug=slugify(code))
            except CodeList.DoesNotExist:
                code_list = CodeList(code=code, status=status)
                update = True

            for key, value in row.items():
                try:
                    if getattr(code_list, key) != value:
                        setattr(code_list, key, value)
                        update = True
                except AttributeError:
                    setattr(code_list, key, value)
                    update = True

            if update:
                code_list.save()
                if self.debug_console:
                    print(f"Updated CodeList: '{code_list}'")
                for theme in themes:
                    if theme not in code_list.themes.all():
                        code_list.themes.add(theme)

        print("End CodeList")
        print("")

    def populate_code_values(self, language):
        if self.debug_console:
            print("****************************")
            print("* Populating CodeListValue *")
            print("****************************")
        errors = dict({"key": [], "data": [], "multiple_parents": [], "no_data": []})
        qs = CodeList.objects.all()
        error_keys = [
            "SpecificAppurtenanceTypeValue",
            "ClassificationItemTypeValue",
            "PartyRoleValue",
            "PhenomenonTypeValue",
            "InputOutputValue",
            "ActivityCodeValue",
            "EconomicActivityValue",
            "ReferenceHabitatTypeCodeValue",
            "ReferenceSpeciesCodeValue",
            "RegionClassificationValue",
            "CountingUnitValue",
            "DesignationValue",
        ]
        error_keys = ["ClassificationItemTypeValue"]  # noqa
        # qs = qs.filter(code__in=error_keys)
        for code_list in qs:
            url = code_list.link
            url += f"/{code_list.code}.{language}.json"
            if self.debug_console:
                print(f">>> Fetching {url}")
            response = requests.get(url=url)
            if response.status_code == 404:
                continue
            data = response.json()
            try:
                item_dict_list = data["codelist"]["containeditems"]
            except KeyError:
                # No data # ToDo ¿?¿?
                if url not in errors["no_data"]:
                    errors["no_data"].append(url)
                continue
            for item_dict in item_dict_list:
                try:
                    item = item_dict["value"]
                except KeyError:
                    # item_code_list = item_dict["codelist"] # ToDo ¿?¿?
                    if url not in errors["key"]:
                        errors["key"].append(url)
                    continue

                row = dict()
                if "parents" in item:
                    parents = item["parents"]
                    if len(parents) > 1:
                        # https://inspire.ec.europa.eu/codelist/CommodityCodeValue/limestone
                        if url not in errors["multiple_parents"]:
                            errors["multiple_parents"].append(item["id"])

                    parent = parents[0]["parent"]
                    row["parent"] = CodeListValue.search(parent["id"])

                code = item["id"].split("/")[-1]
                status_link = item["status"]["id"]
                try:
                    status = Status.objects.get(
                        slug=slugify(status_link.split("/")[-1]),
                    )
                except Status.DoesNotExist:
                    try:
                        status_label = item["status"]["label"]["text"].strip()
                    except KeyError:
                        status_label = status_link
                    status = Status(link=status_link, label=status_label)
                    status.save()
                row["status"] = status
                row["link"] = item["id"]

                update = False
                try:
                    code_list_value = CodeListValue.objects.get(
                        code_list=code_list,
                        slug=slugify(code),
                    )
                except CodeListValue.DoesNotExist:
                    code_list_value = CodeListValue(code_list=code_list, code=code)
                    update = True

                for f in ["label", "definition", "description"]:
                    try:
                        row[f] = item[f]["text"].strip()
                    except KeyError:
                        row[f] = ""

                for key, value in row.items():
                    try:
                        if getattr(code_list_value, key) != value:
                            setattr(code_list_value, key, value)
                            update = True
                    except AttributeError:
                        setattr(code_list_value, key, value)
                        update = True

                if update:
                    try:
                        code_list_value.save()
                        if self.debug_console:
                            print(f"Updated CodeListValue: '{code_list_value}'")
                    except Exception as e:
                        errors["data"].append(f"{code}: {e}")
        # print("\n".join(errors["key"]))
        print("End CodeListValue")
        print("")

    def check_language(self, language):
        LANGUAGES_AVAILABLE = dict(
            {
                "bg": "български",
                "cs": "čeština",
                "da": "dansk",
                "de": "deutsch",
                "et": "eesti keel",
                "el": "ελληνικά",
                "en": "english",
                "es": "español",
                "fr": "français",
                "hr": "hrvatski",
                "it": "italiano",
                "lv": "latviešu valoda",
                "lt": "lietuvių kalba",
                "hu": "magyar",
                "mt": "malti",
                "nl": "nederlands",
                "pl": "polski",
                "pt": "português",
                "ro": "română",
                "sk": "slovenčina",
                "sl": "slovenščina",
                "fi": "suomi",
                "sv": "svenska",
            },
        )
        try:
            _lang = LANGUAGES_AVAILABLE[language]  # noqa
        except KeyError:
            print()
            print(f"ERROR: Language '{language}' is not availbale")
            print()
            print("These are current available languages:")
            print()
            for k, v in LANGUAGES_AVAILABLE.items():
                print(f"    {k}: {v}")
            print()
            print()
            language = None
        return language

    def handle(self, *args, **kwargs):
        if kwargs.get("verbosity") > 0:
            self.debug_console = True
        else:
            self.debug_console = False
        language = kwargs.get("language")
        if language:
            language = self.check_language(language)
            if not language:
                return
        else:
            language = "en"

        self.populate_status(language)
        self.populate_themes(language)
        self.populate_schemas(language)
        self.populate_code_list(language)
        self.populate_code_values(language)
