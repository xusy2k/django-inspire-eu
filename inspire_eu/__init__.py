# -*- coding: utf-8 -*-
"""**************
INSPIRE themes
**************

The INSPIRE theme register contains all spatial data themes, as defined in the Annexes of the INSPIRE Directive
(Directive 2007/2/EC of the European Parliament and of the Council of 14 March 2007 establishing an Infrastructure
for Spatial Information in the European Community (INSPIRE)). The descriptions of the themes are based on version
3.0 of the Definition of Annex Themes and Scope (D 2.3) by the data specifications drafting team and subsequent
updates by the INSPIRE Thematic Working Groups (TWGs).

.. automodule:: inspire_eu.models

=============
Common Models
=============

.. automodule:: inspire_eu.models.abstract
   :members: BaseModel,Identifier,DataLifeCycleInfo,AbstractGeographicalName
   :member-order: bysource
   :inherited-members:
   :exclude-members: __init__,clean,clean_fields,full_clean,get_deferred_fields,refresh_from_db,save,save_base,serializable_value,validate_unique,DoesNotExist, MultipleObjectsReturned

=============
Core Models
=============

.. automodule:: inspire_eu.models.core
   :members: Status,Namespace,Theme,ApplicationSchema,CodeList,CodeListValue,UnitOfMeasure
   :member-order: bysource
   :noindex:
   :inherited-members:
   :exclude-members: __init__,clean,clean_fields,full_clean,get_deferred_fields,refresh_from_db,save,save_base,serializable_value,validate_unique,DoesNotExist, MultipleObjectsReturned,BaseModel

"""  # noqa

__version__ = "0.2.0"
