import logging

from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from ...models import INSPIRE_EU_DEFAULT_SRID, CodeListValue, UnitOfMeasure
from ...models.abstract import DataLifeCycleInfo, Identifier

log = logging.getLogger(__name__)


class AbstractCadastralZoning(Identifier, DataLifeCycleInfo):
    """CadastralZoning

    Definition
        Intermediary areas used in order to divide national territory into cadastral parcels.

    Description

        Cadastral zonings are the intermediary areas (such as municipalities, sections, blocks, …) used in
        order to divide national territory into cadastral parcels. In the INSPIRE context, cadastral zonings are
        to be used to carry metadata information and to facilitate portrayal and search of data.
        Cadastral zonings have the following additional attributes:

            * a geometry
            * a national cadastral zoning reference
            * a name, if any
            * a level in the national cadastral hierarchy and the name of this level
            * portrayal attributes: reference point and label
            * metadata attributes: original map scale denominator and estimated accuracy

        If cadastral zonings are provided, cadastral parcels shall belong to one cadastral zoning of lowest
        level. When several levels of zonings exist in a Member State, it must be ensured that the higher level
        units are composed of that of lower level.

    References:
        * `UML <https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:1:3:1:7204>`_
    """

    estimated_accuracy = models.FloatField(
        blank=True,
        help_text=_(
            "The estimated absolute positional accuracy of cadastral parcels within the cadastral zoning in the "
            "used INSPIRE coordinate reference system. Absolute positional accuracy is the mean value of the "
            "positional uncertainties for a set of positions, where the positional uncertainties are the "
            "distance between a measured position and what is considered as the corresponding true position.",
        ),
    )

    estimated_accuracy_uom = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_estimated_accuracy_uom",
        related_query_name="%(app_label)s_%(class)s_estimated_accuracy_uoms",
        limit_choices_to={"measure_type": UnitOfMeasure.MEASURE_TYPE_AREA},
        help_text=_("Value of estimatedAccuracy shall be given in meters"),
    )

    geometry = models.MultiPolygonField(
        srid=INSPIRE_EU_DEFAULT_SRID,
        blank=True,
        null=True,
        help_text=_(
            _("Geometry of the cadastral zoning."),
        ),
    )

    label = models.CharField(
        max_length=32,
        blank=True,
        help_text=_(
            "Text commonly used to display the cadastral zoning identification.",
        ),
    )

    level = models.ForeignKey(
        CodeListValue,
        blank=True,
        null=True,
        limit_choices_to={"code_list__code": "LevelValue"},
        related_name="%(app_label)s_%(class)s_level",
        related_query_name="%(app_label)s_%(class)s_levels",
        on_delete=models.PROTECT,
        help_text=_(
            "Level of the cadastral zoning in the national cadastral hierarchy.",
        ),
    )

    name = models.CharField(
        max_length=24,
        blank=True,
        help_text=_("Name of the cadastral zoning."),
    )

    national_cadastal_zoning_reference = models.CharField(
        max_length=32,
        blank=True,
        help_text=_(
            "Text commonly used to display the cadastral zoning identification.",
        ),
    )

    area_value = models.IntegerField(
        blank=True,
        null=True,
        help_text=_(
            "Registered area value giving quantification of the area projected on the horizontal plane of "
            "the cadastral parcel.",
        ),
    )
    area_value_uom = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        limit_choices_to={"measure_type": UnitOfMeasure.MEASURE_TYPE_AREA},
        related_name="%(app_label)s_%(class)s_area_value_uom",
        related_query_name="%(app_label)s_%(class)s_area_value_uoms",
    )

    original_map_scale_denominator = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text=_(
            "The denominator in the scale of the original paper map (if any) to whose extent the cadastral "
            "zoning corresponds.",
        ),
    )

    valid_from = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_(
            "Official date and time the cadastral zoning was/will be legally established.",
        ),
    )

    valid_to = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_(
            "Date and time at which the cadastral zoning legally ceased/will cease to be used.",
        ),
    )

    reference_point = models.PointField(
        srid=INSPIRE_EU_DEFAULT_SRID,
        blank=True,
        null=True,
        help_text=_(
            "A point within the cadastral zoning. EXAMPLE The centroid of the cadastral zoneing geometry.",
        ),
    )

    upper_level_unit = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text=_(
            "Level of the cadastral zoning in the national cadastral hierarchy.",
        ),
    )

    class Meta:
        abstract = True


class AbstractCadastralParcel(
    Identifier,
    DataLifeCycleInfo,
    models.Model,
):
    """Cadastral Parcels

    Definition
        Areas defined by cadastral registers or equivalent

    Description
        The INSPIRE Directive focuses on the geographical part of cadastral data In the INSPIRE context cadastral
        parcels will be mainly used as locators for geo information in general including environmental data. As
        much as possible in the INSPIRE context cadastral parcels should be forming a partition of national territory
        Cadastral parcel should be considered as a single area of Earth surface under homogeneous real property
        rights and unique ownership adapted from UN ECE 2004 and WG CPI 2006 Remark By unique ownership is meant
        that the ownership is held by one or several owners for the whole parcel By homogeneous property rights
        is meant that rights of ownership leases and mortgages affect the whole parcel This does not apply to
        specific rights as servitudes which may only affect part of the parcel

        In the definition given by the INSPIRE directive or equivalent refers to all public agencies and institutions
        other than the main traditional nominal cadastre or land registry that register parts of the Earth s surface
        such as special domains urban cadastres public lands which spatially complement the registrations by the main
        cadastre or land registry.

        Cadastral parcels are considered in the INSPIRE scope if they are available as vector data
        Rights and owners are out of the INSPIRE scope
        Buildings land use addresses are considered in other INSPIRE themes

    """

    label = models.CharField(
        max_length=32,
        blank=True,
        help_text=_(
            "Text commonly used to display the cadastral parcel identification.",
        ),
    )

    national_cadastral_reference = models.CharField(
        max_length=32,
        db_index=True,
        help_text=_(
            "Thematic identifier at national level, generally the full national code of the cadastral "
            "parcel. Must ensure the link to the national cadastral register or equivalent.",
        ),
    )

    area_value = models.IntegerField(
        blank=True,
        null=True,
        help_text=_(
            "Registered area value giving quantification of the area projected on the horizontal plane of "
            "the cadastral parcel.",
        ),
    )

    area_value_uom = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        limit_choices_to={"measure_type": UnitOfMeasure.MEASURE_TYPE_AREA},
        related_name="%(app_label)s_%(class)s_area_value_uom",
        related_query_name="%(app_label)s_%(class)s_area_value_uoms",
    )

    valid_from = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_(
            "Official date and time the cadastral parcel was/will be legally established.",
        ),
    )

    valid_to = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_(
            "Date and time at which the cadastral parcel legally ceased/will cease to be used.",
        ),
    )

    geometry = models.MultiPolygonField(
        srid=INSPIRE_EU_DEFAULT_SRID,
        blank=True,
        null=True,
        help_text=_(_("Geometry of the cadastral parcel.")),
    )

    reference_point = models.PointField(
        srid=INSPIRE_EU_DEFAULT_SRID,
        blank=True,
        null=True,
        help_text=_(
            "A point within the cadastral parcel. EXAMPLE The centroid of the cadastral parcel geometry.",
        ),
    )

    class Meta:
        abstract = True
