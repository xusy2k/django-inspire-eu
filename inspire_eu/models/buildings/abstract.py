import logging

from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from ...models import INSPIRE_EU_DEFAULT_SRID, CodeListValue, UnitOfMeasure
from ...models.abstract import DataLifeCycleInfo, Identifier

log = logging.getLogger(__name__)


##############################################
# Building Base
##############################################
class AbstractConstruction(Identifier, DataLifeCycleInfo, models.Model):
    """Abstract construction

    Definition:
        Abstract spatial object type grouping the semantic properties of  buildings, building parts and of
        some optional spatial object types that may be added in order to provide more information about the
        theme Buildings.

    Description:
        The optional spatial object types that may be added to core profiles are described in the extended profiles.
        The ones inheriting from the attributes of AbstractConstruction are Installation and OtherConstruction

    References
        https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:3:2:1:7895

    """

    condition_of_construction = models.ForeignKey(
        CodeListValue,
        on_delete=models.PROTECT,
        limit_choices_to={"code_list__code": "ConditionOfConstructionValue"},
        related_name="%(app_label)s_%(class)s_condition_of_construction",
        related_query_name="%(app_label)s_%(class)s_condition_of_constructions",
        help_text=_(
            "Status of the construction.<br />EXAMPLES: functional, projected, ruin",
        ),
    )

    date_of_construction_beginning = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("Beginning date of construction"),
    )
    date_of_construction_end = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("End of date of construction"),
    )
    date_of_construction_any_point = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("Any point of date of construction"),
    )

    date_of_demolition_beginning = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("Beginning date of demolition"),
    )
    date_of_demolition_end = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("End of date of demolition"),
    )
    date_of_demolition_any_point = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("Any point of date of demolition"),
    )

    date_of_renovation_beginning = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("Beginning date of last major renovation"),
    )
    date_of_renovation_end = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("End of date of last major renovation"),
    )
    date_of_renovation_any_point = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("Any point of date of last major renovation"),
    )

    class Meta:
        abstract = True


class AbstractBuilding(models.Model):
    """Abstract building

    Definition
        Abstract spatial object type grouping the common semantic properties of the spatial object types Building
        and BuildingPart.

    References
        https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:3:2:1:7900

    """

    number_of_dwellings = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text=_(
            "A dwelling is a residential unit which may consist of one or several rooms designed for the occupation "
            "of households.<br />"
            "NOTE: In the data sets including building units, a dwelling is a residential building unit or, only when "
            "that building has no building units, a residential building<br />"
            "EXAMPLES: a single building dwelling could be a detached or semi-detached house. A block of flats will "
            "contain multiple dwellings determined by the number of individual flats.",
        ),
    )
    number_of_building_units = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text=_(
            "Number of building units in the building. A BuildingUnit is a subdivision of Building with its own "
            "lockable access from the outside or from a common area (i.e. not from another BuildingUnit), which is "
            "atomic, functionally independent, and may be separately sold, rented out, inherited, etc.<br />"
            "Building units are spatial objects aimed at subdividing buildings and/or building parts into smaller "
            "parts that are treated as separate entities in daily life. A building unit is homogeneous, regarding "
            "management aspects.<br />"
            "EXAMPLES: It may be e.g. an apartment in a condominium, a terraced house, or a shop inside a "
            "shopping arcade.<br />"
            "NOTE 1: According to national regulations, a building unit may be a flat, a cellar, a garage or "
            "set of a flat, a cellar and a garage.<br />"
            "NOTE 2: According to national regulation, a building that is one entity for daily life (typically, "
            "a single family house) may be considered as a Building composed of one BuildingUnit or as a Building "
            "composed of zero BuildingUnit.",
        ),
    )
    number_of_floors_above_ground = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text=_("Number of floors above ground."),
    )

    class Meta:
        abstract = True


class AbstractBuildingGeometry2D(models.Model):
    """Building geometry 2D

    Definition
        This data types includes the geometry of the building and metadata information about which element of
        the building was captured and how.

    References
        https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:3:2:1:7904

    """

    geometry = models.MultiPolygonField(
        srid=INSPIRE_EU_DEFAULT_SRID,
        blank=True,
        null=True,
        help_text=_("2D or 2.5D geometric representation"),
    )
    reference_geometry = models.BooleanField(
        help_text=_(
            "The geometry to be taken into account by view services, for portrayal.<br />"
            "NOTE 1: In case of multiple representation by point and by surface, it is generally recommended to "
            "provide the surface as reference geometry.<br />"
            "NOTE 2: The geometric representation whose referenceGeometry is true may also be used preferably "
            "for spatial queries by download services (WFS) or by Geographical Information System (GIS).",
        ),
    )
    # HorizontalGeometryReferenceValue
    horizontal_geometry_reference = models.ForeignKey(
        CodeListValue,
        on_delete=models.PROTECT,
        limit_choices_to={"code_list__code": "HorizontalGeometryReferenceValue"},
        related_name="%(app_label)s_%(class)s_horizontal_geometry_reference",
        related_query_name="%(app_label)s_%(class)s_horizontal_geometry_references",
        help_text=_("Element of the building that was captured by (X,Y) coordinates."),
    )

    horizontal_geometry_estimated_accuracy = models.FloatField(
        blank=True,
        help_text=_(
            "The estimated absolute positional accuracy of the (X,Y) coordinates of the building geometry, "
            "in the INSPIRE official Coordinate Reference System. Absolute positional accuracy is defined "
            "as the mean value of the positional uncertainties for a set of positions where the positional "
            "uncertainties are defined as the distance between a measured position and what is considered as "
            "the corresponding true position.<br />"
            "NOTE: This mean value may come from quality measures on a homogeneous population of buildings or "
            "from an estimation based on the knowledge of the production processes and of their accuracy.",
        ),
    )
    horizontal_geometry_estimated_accuracy_uom = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_horizontal_geometry_estimated_accuracy_uom",
        related_query_name="%(app_label)s_%(class)s_horizontal_geometry_estimated_accuracy_uoms",
    )

    vertical_geometry_estimated_accuracy = models.CharField(
        max_length=1,
        blank=True,
        help_text=_("Value of estimatedAccuracy shall be given in meters"),
    )
    vertical_geometry_estimated_accuracy_uom = models.ForeignKey(
        UnitOfMeasure,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="%(app_label)s_%(class)s_vertical_geometry_estimated_accuracy_uom",
        related_query_name="%(app_label)s_%(class)s_vertical_geometry_estimated_accuracy_uoms",
    )
    # ElevationReferenceValue
    vertical_geometry_reference = models.ForeignKey(
        CodeListValue,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        limit_choices_to={"code_list__code": "ElevationReferenceValue"},
        related_name="%(app_label)s_%(class)s_vertical_geometry_reference",
        related_query_name="%(app_label)s_%(class)s_vertical_geometry_references",
        help_text=_(
            "Element of the building that was captured by vertical coordinates.",
        ),
    )

    class Meta:
        abstract = True


##############################################
# Building Extended
##############################################
class AbstractBuildingExtended2D(AbstractBuilding):
    """BuildingsExtended2D

    Definition
        The BuildingsExtended2D profile is a semantic extension of Buildings2D profile with
        additional thematic attributes (material of construction, official area or value, connection to
        utility networks...), classes (building units, installations, other constructions) and references to
        other data (like cadastral data and addresses).

    References
        https://inspire.ec.europa.eu/documents/Data_Specifications/INSPIRE_DataSpecification_BU_v3.0.pdf
    """

    # energy_performance = models.ForeignKey(EnergyPerformance, blank=True, null=True, on_delete=models.PROTECT)
    height_below_ground = models.FloatField(blank=True, null=True)
    height_below_ground_uom = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_height_below_ground_uom",
        related_query_name="%(app_label)s_%(class)s_height_below_ground_uoms",
    )
    number_of_floors_below_ground = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text=_("Number of floors below ground."),
    )

    class Meta:
        abstract = True


class AbstractOtherConstruction(AbstractConstruction):
    """Abstract other construction

    Definition
        Abstract spatial object type grouping the semantic properties of other
        constructions. An other construction is a self-standing construction that belongs
        to theme Buildings and that is not a Building

    Description

        NOTE 1: the main difference between a building and an other construction is the fact that an other construction
        does not need to be enclosed.

        NOTE 2: the other constructions to be considered under scope of theme Buildings are the constructions that are
        not present in another INSPIRE theme and that are necessary for environmental use cases, such as the ones
        considered in this data specification.

        EXAMPLES: bridge, acoustic fence, city wall.

    """

    # OtherConstructionNatureValue
    other_construction_nature = models.ForeignKey(
        CodeListValue,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        limit_choices_to={"code_list__code": "OtherConstructionNatureValue"},
        related_name="%(app_label)s_%(class)s_other_construction_nature",
        related_query_name="%(app_label)s_%(class)s_other_construction_natures",
        help_text=_(
            "Characteristic of the building that makes it generally of interest for mappings applications. "
            "The characteristic may be related to the physical aspect and/or to the function of the building.<br />"
            "This attribute focuses on the physical aspect of the building; however, this physical aspect is often "
            "expressed as a function (e.g. stadium, silo, windmill); this attribute aims to fulfil mainly mapping "
            "purposes and addresses only specific, noticeable buildings. ",
        ),
    )

    class Meta:
        abstract = True


class AbstractDocument(models.Model):
    """Document

    Definition
        Any document providing information about the building or building part or building unit.


    Description
        EXAMPLES: the building permit, a photo of facade or inner yard, a sketch of interior, the building code, the
                energy performance assessment, an emergency plan
    """

    document_link = models.URLField(
        help_text=_("The Internet address where the document may be found."),
    )
    date = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("Date of validity of the document"),
    )
    document_description = models.TextField(
        blank=True,
        help_text=_(
            "A short text providing overview of the document content. May be just title of the document",
        ),
    )
    # SourceStatusValue
    source_status = models.ForeignKey(
        CodeListValue,
        limit_choices_to={"code_list__code": "SourceStatusValue"},
        related_name="%(app_label)s_%(class)s_source_status",
        related_query_name="%(app_label)s_%(class)s_source_statuss",
        on_delete=models.PROTECT,
        help_text=_(
            "The status of the document, i.e. this attribute indicates if the document comes from official "
            "source or not",
        ),
    )

    class Meta:
        abstract = True


class AbstractOfficialArea(models.Model):
    """Official area

    Definition
        This data types includes the official area of the building, building part or building unit and information
        about the exact meaning of this area.

    """

    # OfficialAreaReferenceValue
    reference = models.ForeignKey(
        CodeListValue,
        on_delete=models.PROTECT,
        limit_choices_to={"code_list__code": "OfficialAreaReferenceValue"},
        help_text=_(
            "The type of official area may be described either by using the values provided by "
            "the CLGE measurement code for the floor area of buildings (which values are "
            "provided by the CLGE_OfficialAreaReferenceValue) or by using another "
            "standard (which values are provided by the empty code list OtherStandard "
            "OfficialAreaReferenceValue, this code list having to be defined at Member State "
            "level)..",
        ),
    )
    value = models.FloatField(blank=True, help_text=_("The value of the official area"))
    # value_uom = models.CharField(max_length=1,
    value_uom = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        blank=True,
    )
    height_parameter = models.FloatField(
        blank=True,
        null=True,
        help_text=_(
            "The height parameter used to differentiate internal primary area of internal other "
            "area, if the official area is referenced using the CLGE measurement code for the "
            "floor area of buildings",
        ),
    )
    height_parameter_uom = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        help_text=_("Value of Elevation shall be given in meters"),
    )

    class Meta:
        abstract = True


class AbstractElevation(models.Model):
    """Elevation

    Definition
        This data types includes the elevation value itself  and information on how this elevation was measured.


    References
        https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:3:2:1:7901
    """

    # ElevationReferenceValue
    reference = models.ForeignKey(
        CodeListValue,
        on_delete=models.PROTECT,
        limit_choices_to={"code_list__code": "ElevationReferenceValue"},
        help_text=_("Element where the elevation was measured."),
        related_name="%(app_label)s_%(class)s_elevation_reference",
        related_query_name="%(app_label)s_%(class)s_elevation_references",
    )
    value = models.FloatField(
        blank=True,
        help_text=_(
            "Vertically-constrained dimensional property consisting of an absolute measure referenced to a "
            "well-defined surface which is commonly taken as origin (geoïd, water level, etc.).<br />"
            "Source: adapted from the definition given in the data specification of the theme Elevation.",
        ),
    )
    # value_uom = models.CharField(max_length=1,
    value_uom = models.ForeignKey(
        UnitOfMeasure,
        on_delete=models.PROTECT,
        blank=True,
        help_text=_("Value of Elevation shall be given in meters"),
        related_name="%(app_label)s_%(class)s_value_uom",
        related_query_name="%(app_label)s_%(class)s_value_uoms",
    )

    class Meta:
        abstract = True


class AbstractExternalReference(models.Model):
    """External reference

    Definition
        Reference to an external information system containing any piece of information related to the spatial object.

    References
        https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:3:2:1:7908

    """

    information_system = models.URLField(
        help_text=_("Uniform Resource Identifier of the external information system"),
    )
    information_system_name = models.CharField(
        max_length=32,
        blank=True,
        help_text=_(
            "The name of the external information system"
            "EXAMPLES: Danish Register of Dwellings, Spanish Cadastre",
        ),
    )
    reference = models.CharField(
        max_length=24,
        help_text=_(
            "Thematic identifier of the spatial object or of any piece of information related to the "
            "spatial object.<br />"
            "NOTE: This reference will act as a foreign key to implement the association between the spatial "
            "object in the INSPIRE data set and in the external information system<br />"
            "EXAMPLE: The cadastral reference of a given building in the national cadastral register.",
        ),
    )

    class Meta:
        abstract = True


class AbstractHeightAboveGround(models.Model):
    """Height above ground

    Definition
        Vertical distance (measured or estimated) between a low reference and a high reference.

    References
        https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:3:2:1:7898

    """

    # ElevationReferenceValue
    height_reference = models.ForeignKey(
        CodeListValue,
        on_delete=models.PROTECT,
        limit_choices_to={"code_list__code": "ElevationReferenceValue"},
        help_text=_(
            "Element used as the high reference.<br />"
            "EXAMPLE: The height of the building has been captured up to the top of building.",
        ),
        related_name="%(app_label)s_%(class)s_height_reference",
        related_query_name="%(app_label)s_%(class)s_height_references",
    )
    # ElevationReferenceValue
    low_reference = models.ForeignKey(
        CodeListValue,
        on_delete=models.PROTECT,
        limit_choices_to={"code_list__code": "ElevationReferenceValue"},
        help_text=_(
            "Element as the low reference.<br />"
            "EXAMPLE: The height of the building has been captured from its the lowest ground point.",
        ),
        related_name="%(app_label)s_%(class)s_low_reference",
        related_query_name="%(app_label)s_%(class)s_low_references",
    )
    # HeightStatusValue
    status = models.ForeignKey(
        CodeListValue,
        on_delete=models.PROTECT,
        limit_choices_to={"code_list__code": "HeightStatusValue"},
        help_text=_("The way the height has been captured."),
        related_name="%(app_label)s_%(class)s_height_status",
        related_query_name="%(app_label)s_%(class)s_s_height_statuss",
    )
    value = models.SmallIntegerField(
        help_text=_("Value of the height above ground"),
    )

    class Meta:
        abstract = True


class AbstractBuildingNature(models.Model):
    """Building nature

    Definition
        Characteristic of the building that makes it generally of interest for mappings applications.
        The characteristic may be related to the physical aspect and/or to the function of the building.

    Description
        This attribute focuses on the physical aspect of the building; however, this physical aspect is often
        expressed as a function (e.g. stadium, silo, windmill); this attribute aims to fulfil mainly mapping
        purposes and addresses only specific, noticeable buildings.

    Vocabulary
        https://inspire.ec.europa.eu/codeList/BuildingNatureValue

    """

    # BuildingNatureValue
    nature = models.ForeignKey(
        CodeListValue,
        on_delete=models.PROTECT,
        limit_choices_to={"code_list__code": "BuildingNatureValue"},
        related_name="%(app_label)s_%(class)s_nature",
        related_query_name="%(app_label)s_%(class)s_natures",
        help_text=_(
            "Characteristic of the building that makes it generally of interest for mappings applications. The "
            "characteristic may be related to the physical aspect and/or to the function of the building.<br />"
            "This attribute focuses on the physical aspect of the building; however, this physical aspect is "
            "often expressed as a function (e.g. stadium, silo, windmill); this attribute aims to fulfil mainly "
            "mapping purposes and addresses only specific, noticeable buildings.",
        ),
    )

    class Meta:
        abstract = True


class AbstractBuildingCurrentUse(models.Model):
    """Current use

    Definition
        This data type enables to detail the current use(s).

    References
        https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:3:2:1:7906

    """

    # CurrentUseValue
    current_use = models.ForeignKey(
        CodeListValue,
        on_delete=models.PROTECT,
        limit_choices_to={"code_list__code": "CurrentUseValue"},
        related_name="%(app_label)s_%(class)s_current_use",
        related_query_name="%(app_label)s_%(class)s_current_uses",
        help_text=_("Current use"),
    )
    percentage = models.SmallIntegerField(
        blank=True,
        null=True,
        help_text=_(
            "The proportion of the real world object, given as a percentage, devoted to this current "
            "use. <br />"
            "NOTE: The percentage of use is generally the percentage of floor area dedicated to this "
            "given use. If it is not the case, it is recommended to explain what the percentage refers "
            "to in metadata (template for additional information)",
        ),
    )

    class Meta:
        abstract = True


class AbstractEnergyPerformance(models.Model):
    """Energy performance

    Definition
        The energy performance of the building or building part or building unit

    Description
        NOTE: The energy performance is required by the Energy Performance of
        Building Directive for the new buildings being rent or sold.

    """

    energy_performance_value = models.ForeignKey(
        CodeListValue,
        on_delete=models.PROTECT,
        limit_choices_to={"code_list__code": "EnergyPerformanceValue"},
        help_text=_(
            "The date when the energy performance of the building or building unit was assessed",
        ),
        related_name="energy_performance_value",
    )
    date_of_assessment = models.DateTimeField(
        blank=True,
        help_text=_(
            "Date and time at which this version of the spatial object was inserted or changed in "
            "the spatial data set.",
        ),
    )
    # DocumentCitation: INSPIRE Generic Conceptual Model, version 3.4 [DS-D2.5]
    #                   Citation for the purposes of unambiguously referencing a document.
    assessment_method = models.CharField(
        max_length=1,
        blank=True,
        help_text=_(
            "The reference to the document describing the assessment method of energy performance",
        ),
    )

    class Meta:
        abstract = True


class AbstractBuildingAndBuildingUnitInfo(models.Model):
    """Building and building unit info

    Definition
        Abstract spatial object type grouping the additional properties that are common to Building, Building Part and
        BuildingUnit.

    Description

        NOTE 1: The additional properties are those that are not already included in the base application schema.

        NOTE 2: These additional properties concern mainly the official information that may be attached to
        buildings / building parts or to building units.
    """

    connection_to_electricity = models.BooleanField(blank=True, null=True)
    connection_to_gas = models.BooleanField(blank=True, null=True)
    connection_to_sewage = models.BooleanField(blank=True, null=True)
    connection_to_water = models.BooleanField(blank=True, null=True)
    # energy_performance = models.ForeignKey(EnergyPerformance)

    class Meta:
        abstract = True


class AbstractBuildingUnit(AbstractBuildingAndBuildingUnitInfo):
    """Building unit

    Definition
        Abstract spatial object type grouping the semantic properties of building units. A BuildingUnit is a
        subdivision of Building with its own lockable access from the outside or from a common area (i.e. not
        from another BuildingUnit), which is atomic, functionally independent, and may be separately sold,
        rented out, inherited, etc.

    Description

        Building units are spatial objects aimed at subdividing buildings and/or building parts into smaller
        parts that are treated as separate entities in daily life. A building unit is homogeneous, regarding
        management aspects.

        EXAMPLES: It may be e.g. an apartment in a condominium, a terraced house, or a shop inside a shopping arcade.

        NOTE 1: According to national regulations, a building unit may be a flat, a cellar, a garage or set of a flat,
        a cellar and  a garage.

        NOTE 2: According to national regulation, a building that is one entity for daily life (typically, a single
        family house) may be considered as a Building composed of one BuildingUnit or as a Building composed of
        zero BuildingUnit.

    """

    class Meta:
        abstract = True


class AbstractBuildingInfo(AbstractBuildingAndBuildingUnitInfo):
    """Building info

    Definition
        Abstract spatial object type grouping the additional specific properties of Building and Building Part

    Description

        NOTE 1: The additional properties are those that are not already included in the base application schema.

        NOTE 2: The specific properties are the properties that apply to Building and BuildingPart without
        applying to BuildingUnit.

    .. warning::

        Pending ToDo:

        + floorDescription: FloorDescription [0..*]
        + floorDistribution: FloorRange [1..*]
        + heightBelowGround: Length [0..1]
        + materialOfFacade: MaterialOfFacadeValue [0..*]
        + materialOfRoof: MaterialOfRoofValue [0..*]
        + materialOfStructure: MaterialOfStructureValue [0..*]
        + numberOfFloorsBelowGround: Integer [0..1]
        + roofType: RoofTypeValue [0..*]
    """

    class Meta:
        abstract = True
