"""*****************
Cadastral Parcels
*****************

Definition
==========
Areas defined by cadastral registers or equivalent.

Description
===========

The INSPIRE Directive focuses on the geographical part of cadastral data. In the INSPIRE context, cadastral
parcels will be mainly used as locators for geo-information in general, including environmental data.
As much as possible, in the INSPIRE context, cadastral parcels should be forming a partition of national
territory. Cadastral parcel should be considered as a single area of Earth surface, under homogeneous real
property rights and unique ownership (adapted from UN ECE 2004 and WG-CPI, 2006). Remark: By unique ownership
is meant that the ownership is held by one or several owners for the whole parcel. By homogeneous property
rights is meant that rights of ownership, leases and mortgages affect the whole parcel. This does not apply
to specific rights as servitudes which may only affect part of the parcel.

In the definition given by the INSPIRE directive, or equivalent refers to all public agencies and institutions
other than the main traditional/nominal cadastre or land registry, that register parts of the Earth's surface
such as special domains, urban cadastres, public lands, which spatially complement the registrations by the
main cadastre or land registry.

Cadastral parcels are considered in the INSPIRE scope if they are available as vector data.

Rights and owners are out of the INSPIRE scope.

Buildings, land use, addresses are considered in other INSPIRE themes.

References
==========
    * `Data Specifications <https://inspire.ec.europa.eu/Themes/122/2892>`_
    * `INSPIRE Data Specification on Cadastral Parcels – Technical Guidelines <https://inspire.ec.europa.eu/id/document/tg/cp>`_
    * `Theme description from Registry  <https://inspire.ec.europa.eu/theme/cp>`_
    * `UML <https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:1:3:1:7204>`_

    .. figure:: ../../../docs/_static/img/cadastral_parcels.png
        :align: center
        :target: https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:1:3:1:7204

Models
======

.. automodule:: inspire_eu.models.cadastral_parcels.abstract
   :members:
   :inherited-members:
   :exclude-members: __init__,clean,clean_fields,full_clean,get_deferred_fields,refresh_from_db,save,save_base,serializable_value,validate_unique

"""  # noqa

import logging

from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from .. import INSPIRE_EU_THEMES

log = logging.getLogger(__name__)


if "cadastral_parcels" in INSPIRE_EU_THEMES and INSPIRE_EU_THEMES["cadastral_parcels"]:
    from .abstract import AbstractCadastralParcel, AbstractCadastralZoning

    class CadastralZoning(AbstractCadastralZoning, models.Model):
        """CadastralZoning

        Definition
            Intermediary areas used in order to divide national territory into cadastral parcels.

        Description
            Cadastral zonings are the intermediary areas (such as municipalities, sections, blocks, …) used in
            order to divide national territory into cadastral parcels. In the INSPIRE context, cadastral zonings are
            to be used to carry metadata information and to facilitate portrayal and search of data.
            Cadastral zonings have the following additional attributes:
            − a geometry
            − a national cadastral zoning reference
            − a name, if any
            − a level in the national cadastral hierarchy and the name of this level
            − portrayal attributes: reference point and label
            − metadata attributes: original map scale denominator and estimated accuracy
            If cadastral zonings are provided, cadastral parcels shall belong to one cadastral zoning of lowest
            level. When several levels of zonings exist in a Member State, it must be ensured that the higher level
            units are composed of that of lower level.

        References
            * `UML <https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:1:3:1:7204>`_
        """

        class Meta:
            verbose_name = _("Cadastral Zoning")
            verbose_name_plural = _("Cadastral Zonings")

        def __str__(self):
            return "%s %s" % (self.label, self.national_cadastal_zoning_reference)

    class CadastralParcel(AbstractCadastralParcel, models.Model):
        """Cadastral Parcel

        Definition
            Areas defined by cadastral registers or equivalent.

        Description
            Areas defined by cadastral registers or equivalent

            NOTE As much as possible, in the INSPIRE context, cadastral parcels should be forming a partition of national
            territory. Cadastral parcel should be considered as a single area of Earth surface (land and/or water), under
            homogeneous real property rights and unique ownership, real property rights and ownership being defined by
            national law (adapted from UN ECE 2004 and WG-CPI, 2006). By unique ownership is meant that the ownership is
            held by one or several joint owners for the whole parcel.

        References
            * https://inspire.ec.europa.eu/id/document/tg/cp
            * https://inspire.ec.europa.eu/schemas/cp/4.0/CadastralParcels.xsd
            * https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=2:1:3:1:7209
            * https://inspire.ec.europa.eu/documents/Data_Specifications/INSPIRE_DataSpecification_CP_v3.0.1.pdf
        """  # noqa

        cadastral_zoning = models.ForeignKey(
            CadastralZoning,
            on_delete=models.PROTECT,
            blank=True,
            null=True,
            help_text=_(
                _("Cadastral Zoning"),
            ),
        )

        class Meta:
            verbose_name = _("Cadastral Parcel")
            verbose_name_plural = _("Cadastral Parcels")

        def __str__(self):
            return "%s %s" % (self.label, self.national_cadastal_reference)
