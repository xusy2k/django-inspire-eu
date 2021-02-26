"""*********
Buildings
*********

Definition
==========
Geographical location of buildings specifications

Description
===========
A building is a covered facility usable for the protection of humans animals things or the production of economic
goods A building refers to any structure permanently constructed or erected on its site Information on location of
buildings may be supplied as points or with the actual basic form of the building Usually buildings are part of
cadastre On the local level buildings are available within the large scale cadastral maps or cadastral data sets
and are geometrically represented as surfaces

Most buildings can be identified geocoded by address separate theme in INSPIRE

References
==========
    * `Data Specifications <https://inspire.ec.europa.eu/Themes/126/2892>`_
    * `INSPIRE Data Specification on Buildings – Technical Guidelines <https://inspire.ec.europa.eu/id/document/tg/bu>`_
    * `Theme description from Registry <https://inspire.ec.europa.eu/theme/bu>`_
    * `Building Base UML <https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:3:2:1:7883>`_

    .. figure:: ../../../docs/_static/img/buildings_base.png
        :align: center
        :target: https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:3:2:1:7883

    * `Building2D Base UML <https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:3:2:2:7911>`_

    .. figure:: ../../../docs/_static/img/buildings2D.png
        :align: center
        :target: https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:3:2:2:7911

    * `Building3D Base UML <https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:3:2:3:7916>`_

    .. figure:: ../../../docs/_static/img/buildings3D.png
        :align: center
        :target: https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:3:2:3:7916


Models
======

.. automodule:: inspire_eu.models.buildings.abstract
   :members:
   :inherited-members:
   :exclude-members: __init__,clean,clean_fields,full_clean,get_deferred_fields,refresh_from_db,save,save_base,serializable_value,validate_unique

"""  # noqa

import logging

from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from .. import INSPIRE_EU_THEMES

log = logging.getLogger(__name__)


if "buildings" in INSPIRE_EU_THEMES and INSPIRE_EU_THEMES["buildings"]:
    from ...models import INSPIRE_EU_DEFAULT_SRID, BaseInspireEUModel
    from ...models.abstract import AbstractGeographicalName
    from ..cadastral_parcels import CadastralParcel
    from .abstract import (
        AbstractBuildingCurrentUse,
        AbstractBuildingExtended2D,
        AbstractBuildingGeometry2D,
        AbstractBuildingNature,
        AbstractConstruction,
        AbstractDocument,
        AbstractElevation,
        AbstractExternalReference,
        AbstractHeightAboveGround,
        AbstractOtherConstruction,
    )

    class Building(
        BaseInspireEUModel,
        AbstractConstruction,
        AbstractBuildingExtended2D,
        AbstractBuildingGeometry2D,
    ):
        """Building

        Definition
        ----------
        A Building is an enclosed construction above and/or underground, used or intended for the shelter of humans,
        animals or things or for the production of economic goods. A building refers to any structure permanently
        constructed or erected on its site.
        """

        parent = models.ForeignKey(
            "self",
            blank=True,
            null=True,
            on_delete=models.PROTECT,
            related_name="parts",
        )
        cadastral_parcels = models.ManyToManyField(CadastralParcel)
        is_building_part = models.BooleanField(
            help_text=_("Is it a BuildingPart?"),
            default=False,
        )

        class Meta:
            verbose_name = _("Building")
            verbose_name_plural = _("Buildings")

        def __str__(self):
            return self.local_id

    class BuildingDocument(BaseInspireEUModel, AbstractDocument):
        """Building Document

        Definition
        ----------
        This data types provides the address where the document may be found and a minimum set of metadata elements
        considered as necessary to exploit the document.

        """

        building = models.ForeignKey(Building, on_delete=models.PROTECT)

        class Meta:
            verbose_name = _("Building Document")
            verbose_name_plural = _("Building Documents")
            ordering = ["building", "document_link"]

        def __str__(self):
            return "%s %s" % (self.building, self.document_link)

    class BuildingElevation(BaseInspireEUModel, AbstractElevation):
        """Building Elevation

        Definition
        ----------
        Vertically-constrained dimensional property consisting of an absolute measure referenced to a well-defined
        surface which is commonly taken as origin (geoïd, water level, etc.).

        Description
        ------------
        Source: adapted from the definition given in the data specification of the theme Elevation.
        """

        building = models.ForeignKey(Building, on_delete=models.PROTECT)

        # DirectPosition : Public Class
        # https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=1:3:6:1:1:985
        coordinate = models.PointField(
            srid=INSPIRE_EU_DEFAULT_SRID,
            blank=True,
            null=True,
        )
        dimension = models.IntegerField(blank=True, null=True)

        class Meta:
            verbose_name = _("Building Elevation")
            verbose_name_plural = _("Building Elevations")
            ordering = ["building", "dimension"]

        def __str__(self):
            return "%s %s" % (self.building, self.dimension)

    class BuildingExternalReference(BaseInspireEUModel, AbstractExternalReference):
        """Building External Reference

        Description
        -----------
        Reference to an external information system containing any piece of information related to the spatial object.

        EXAMPLE 1: Reference to another spatial data set containing another view on buildings; the externalReference may
                be used for instance to ensure consistency between 2D and 3D representations of the same buildings
        EXAMPLE 2: Reference to cadastral or dwelling register. The reference to this register may enable to find legal
                information related to the building, such as the owner(s) or valuation criteria (e.g. type of heating,
                toilet, kitchen)
        EXAMPLE 3: Reference to the system recording the building permits. The reference to the building permits may be
                used to find detailed information about the building physical and temporal aspects.

        """  # noqa

        building = models.ForeignKey(Building, on_delete=models.PROTECT)

        class Meta:
            verbose_name = _("Building External Reference")
            verbose_name_plural = _("Building External References")
            ordering = ["building", "reference"]

        def __str__(self):
            return "%s %s" % (self.building, self.reference)

    class BuildingHeightAboveGround(BaseInspireEUModel, AbstractHeightAboveGround):
        """Height above ground

        Definition
        ----------
        Vertical distance (measured or estimated) between a low reference and a high reference.

        References
        ----------
        https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:3:2:1:7898

        """

        building = models.ForeignKey(Building, on_delete=models.PROTECT)

        class Meta:
            verbose_name = _("Building Height Above Ground")
            verbose_name_plural = _("Building Heights Above Ground")
            ordering = ["building", "height_reference"]

        def __str__(self):
            return "%s %s %s" % (self.building, self.height_reference, self.value)

    class BuildingNature(BaseInspireEUModel, AbstractBuildingNature):
        building = models.ForeignKey(Building, on_delete=models.PROTECT)

        class Meta:
            verbose_name = _("Building Nature")
            verbose_name_plural = _("Building Natures")
            ordering = ["building", "nature"]

        def __str__(self):
            return "%s %s" % (self.building, self.nature)

    class BuildingCurrentUse(BaseInspireEUModel, AbstractBuildingCurrentUse):
        building = models.ForeignKey(Building, on_delete=models.PROTECT)

        class Meta:
            verbose_name = _("Building Current Use")
            verbose_name_plural = _("Building Current Uses")
            ordering = ["building", "current_use"]

        def __str__(self):
            return "%s %s %s" % (self.building, self.current_use, self.percentage)

    class BuildingGeographicalName(BaseInspireEUModel, AbstractGeographicalName):
        building = models.ForeignKey(Building, on_delete=models.PROTECT)

        class Meta:
            verbose_name = _("Geographical Name")
            verbose_name_plural = _("Geographical Names")
            ordering = ["building", "source_of_name"]

        def __str__(self):
            return "%s %s" % (self.building, self.source_of_name)

    class OtherConstruction(BaseInspireEUModel, AbstractOtherConstruction):
        building = models.ForeignKey(
            Building,
            on_delete=models.PROTECT,
            blank=True,
            null=True,
        )
        cadastral_parcels = models.ManyToManyField(CadastralParcel)
        geometry = models.MultiPolygonField(
            srid=INSPIRE_EU_DEFAULT_SRID,
            blank=True,
            null=True,
            help_text=_("2D or 2.5D geometric representation"),
        )

        class Meta:
            verbose_name = _("Other Construction")
            verbose_name_plural = _("Other Constructions")
