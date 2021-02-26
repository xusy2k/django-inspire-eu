import logging

from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from .core import CodeListValue, Namespace

log = logging.getLogger(__name__)


###############################################################################
#                    _    _         _                  _                      #
#                   / \  | |__  ___| |_ _ __ __ _  ___| |_                    #
#                  / _ \ | '_ \/ __| __| '__/ _` |/ __| __|                   #
#                 / ___ \| |_) \__ \ |_| | | (_| | (__| |_                    #
#                /_/   \_\_.__/|___/\__|_|  \__,_|\___|\__|                   #
#                                                                             #
###############################################################################


class Identifier(models.Model):
    """Identifier

    Definition
        External unique object identifier published by the responsible body, which may be used by external
        applications to reference the spatial object.

    Description

        NOTE 1 External object identifiers are distinct from thematic object identifiers.

        NOTE 2 The voidable version identifier attribute is not part of the unique identifier of a spatial object and
        may be used to distinguish two versions of the same spatial object.

    """

    namespace = models.ForeignKey(
        Namespace,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_namespace",
        related_query_name="%(app_label)s_%(class)s_namespaces",
    )
    local_id = models.CharField(
        max_length=32,
        help_text=_(
            "A local identifier, assigned by the data provider. The local identifier is unique within the "
            "namespace, that is no other spatial object carries the same unique identifier.<br />"
            "NOTE It is the responsibility of the data provider to guarantee uniqueness of the local "
            "identifier within the namespace.",
        ),
    )
    version_id = models.CharField(
        max_length=25,
        blank=True,
        help_text=_(
            "The identifier of the particular version of the spatial object, with a maximum length of 25 "
            "characters. If the specification of a spatial object type with an external object identifier "
            "includes life-cycle information, the version identifier is used to distinguish between the "
            "different versions of a spatial object. Within the set of all versions of a spatial object, "
            "the version identifier is unique.<br />"
            "NOTE The maximum length has been selected to allow for time stamps based on ISO 8601, "
            """for example, "2007-02-12T12:12:12+05:30" as the version identifier.<br />"""
            "NOTE 2 The property is void, if the spatial data set does not distinguish between different "
            "versions of the spatial object. It is missing, if the spatial object type does not support "
            "any life-cycle information.",
        ),
    )

    class Meta:
        abstract = True
        unique_together = ["namespace", "local_id", "version_id"]


class DataLifeCycleInfo(models.Model):
    """DataLifeCycleInfo

    Definition
        Begin and End datetime fields
    """

    begin_lifespan_version = models.DateTimeField(
        help_text=_(
            "Registered area value giving quantification of the area projected on the horizontal plane of "
            "the cadastral parcel.",
        ),
    )

    end_lifespan_version = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_(
            "Date and time at which this version of the spatial object was superseded or retired in the "
            "spatial data set.",
        ),
    )

    class Meta:
        abstract = True


class AbstractGeographicalName(models.Model):
    """Geographical Name

    Definition
        Proper noun applied to a real world entity.

    References
        `GeographicalName Class <https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:1:6:2:7246>`_
    """  # noqa

    language = models.CharField(
        max_length=64,
        blank=True,
        help_text=_(
            "Language of the name, given as a three letters code, in accordance with either "
            "ISO 639-3 or ISO 639-5.",
        ),
    )
    nativeness = models.ForeignKey(
        CodeListValue,
        limit_choices_to={"code_list__code": "NativenessValue"},
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        help_text=_(
            "Information enabling to acknowledge if the name is the one that is/was used in the area where "
            "the spatial object is situated at the instant when the name is/was in use.",
        ),
        related_name="%(app_label)s_%(class)s_nativeness",
        related_query_name="%(app_label)s_%(class)s_nativenesss",
    )
    name_status = models.ForeignKey(
        CodeListValue,
        limit_choices_to={"code_list__code": "NameStatusValue"},
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        help_text=_(
            "Qualitative information enabling to discern which credit should be given to the name "
            "with respect to its standardization and/or its topicality.",
        ),
        related_name="%(app_label)s_%(class)s_name_status",
        related_query_name="%(app_label)s_%(class)s_name_statuss",
    )
    source_of_name = models.CharField(
        max_length=64,
        blank=True,
        help_text=_(
            "Original data source from which the geographical name is taken from and integrated in the data set "
            "providing/publishing it. For some named spatial objects it might refer again to the publishing data "
            "set if no other information is available.",
        ),
    )
    pronunciation = models.CharField(
        max_length=64,
        blank=True,
        help_text=_(
            "Proper, correct or standard (standard within the linguistic community concerned) "
            "pronunciation of the geographical name.",
        ),
    )
    spelling = models.CharField(
        max_length=64,
        blank=True,
        help_text=_("A proper way of writing the geographical name."),
    )
    grammatical_gender = models.ForeignKey(
        CodeListValue,
        limit_choices_to={"code_list__code": "GrammaticalGenderValue"},
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        help_text=_("Class of nouns reflected in the behavior of associated words."),
        related_name="%(app_label)s_%(class)s_grammatical_gender",
        related_query_name="%(app_label)s_%(class)s_grammatical_genders",
    )
    grammatical_number = models.ForeignKey(
        CodeListValue,
        limit_choices_to={"code_list__code": "GrammaticalNumberValue"},
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        help_text=_("Grammatical category of nouns that expresses count distinctions."),
        related_name="%(app_label)s_%(class)s_grammatical_number",
        related_query_name="%(app_label)s_%(class)s_grammatical_numbers",
    )

    class Meta:
        abstract = True
