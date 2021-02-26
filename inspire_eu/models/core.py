import logging

from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from slugify import slugify

from ..utils import get_inspire_eu_base_model

log = logging.getLogger(__name__)


###############################################################################
#                             ____                                            #
#                            / ___|___  _ __ ___                              #
#                           | |   / _ \| '__/ _ \                             #
#                           | |__| (_) | | |  __/                             #
#                            \____\___/|_|  \___|                             #
#                                                                             #
###############################################################################

try:
    BaseInspireEUModel = get_inspire_eu_base_model()
except AttributeError:

    class BaseInspireEUModel(models.Model):
        """Base Model

        Definition
            Abstract class that appends common fields
        """

        class Meta:
            abstract = True


class Namespace(BaseInspireEUModel):
    """Namespace

    Definition
        Namespace uniquely identifying the data source of the spatial object.

    Description
        NOTE The namespace value will be owned by the data provider of the spatial object and will be registered
        in the INSPIRE External Object Identifier Namespaces Register.

    """

    code = models.CharField(max_length=32, help_text=_("Namespace"))
    name = models.CharField(max_length=64, blank=True)

    class Meta:
        verbose_name = _("Namespace")
        verbose_name_plural = _("Namespaces")
        ordering = ["code", "name"]

    def __str__(self):
        return "%s %s" % (self.code, self.name)


class Status(BaseInspireEUModel):
    """Status

    Description
        Possible values: Valid, Invalid

    References
        * https://inspire.ec.europa.eu/registry/status/valid
        * https://inspire.ec.europa.eu/registry/status/invalid

    """

    code = models.CharField(max_length=32, db_index=True)
    slug = models.CharField(max_length=32, blank=True, db_index=True)
    label = models.CharField(max_length=128)
    definition = models.TextField(blank=True)
    link = models.URLField()
    is_valid = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Status")
        ordering = ["is_valid", "label"]

    def __str__(self):
        return "%s: %s" % (self.code, self.label)

    def save(self, *args, **kwargs):
        self.link = self.link.replace("http://", "https://")
        if not self.code:
            self.code = self.link.split("/")[-1]
        self.slug = slugify(self.code)[:32]
        return super().save(*args, **kwargs)


class Theme(BaseInspireEUModel):
    """INSPIRE theme register

    Definition
        The INSPIRE theme register contains all spatial data themes, as defined in the Annexes of the
        INSPIRE Directive (Directive 2007/2/EC of the European Parliament and of the Council of 14 March 2007
        establishing an Infrastructure for Spatial Information in the European Community (INSPIRE)). The
        descriptions of the themes are based on version 3.0 of the Definition of Annex Themes and Scope (D 2.3)
        by the data specifications drafting team and subsequent updates by the INSPIRE Thematic Working Groups (TWGs).

    Owner
        European Union

    Register manager
        European Commission, Joint Research Centre

    Control body
        Control body for the central INSPIRE registers and INSPIRE register federation

    Submitter
        Nominated submitting organizations for the central INSPIRE registers and INSPIRE register federation

    Contact point
        JRC INSPIRE Registry Team <inspire-registry-dev@jrc.ec.europa.eu>

    Licence
        Europa Legal Notice

    References
        https://inspire.ec.europa.eu/theme
    """

    code = models.CharField(max_length=32, db_index=True)
    slug = models.CharField(max_length=32, blank=True, db_index=True)
    link = models.URLField()
    version = models.SmallIntegerField(blank=True, default=0)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    label = models.CharField(max_length=128)
    definition = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Theme")
        verbose_name_plural = _("Themes")
        ordering = ["code", "label"]

    def __str__(self):
        return "%s: %s" % (self.code, self.label)

    def save(self, *args, **kwargs):
        self.link = self.link.replace("http://", "https://")
        if not self.code:
            self.code = self.link.split("/")[-1]
        self.slug = slugify(self.code)[:32]
        return super().save(*args, **kwargs)


class ApplicationSchema(BaseInspireEUModel):
    """INSPIRE Application schema register

    Definition
        The INSPIRE application schema register contains all application schemas of the consolidated
        INSPIRE UML data model.

    Owner
        European Union

    Register manager
        European Commission, Joint Research Centre

    Control body
        Control body for the central INSPIRE registers and INSPIRE register federation

    Submitter
        Nominated submitting organizations for the central INSPIRE registers and INSPIRE register federation

    Contact point
        JRC INSPIRE Registry Team <inspire-registry-dev@jrc.ec.europa.eu>

    Licence
        Europa Legal Notice

    References
        https://inspire.ec.europa.eu/applicationschema
    """

    code = models.CharField(max_length=32, db_index=True)
    slug = models.CharField(max_length=32, blank=True, db_index=True)
    link = models.URLField()
    version = models.SmallIntegerField(blank=True, default=0)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    label = models.CharField(max_length=128)
    definition = models.TextField(blank=True)
    description = models.TextField(blank=True)
    themes = models.ManyToManyField(Theme)

    class Meta:
        verbose_name = _("Application Schema")
        verbose_name_plural = _("Application Schemes")
        ordering = ["code", "label"]

    def __str__(self):
        return "%s: %s" % (self.code, self.label)

    def save(self, *args, **kwargs):
        self.link = self.link.replace("http://", "https://")
        if not self.code:
            self.code = self.link.split("/")[-1]
        self.slug = slugify(self.code)[:32]
        return super().save(*args, **kwargs)


class CodeList(BaseInspireEUModel):
    """INSPIRE Code List Register

    Definition
        The INSPIRE code list register contains the code lists and their values, as defined in the INSPIRE
        implementing rules on interoperability of spatial data sets and services (Commission Regulation
        (EU) No 1089/2010).

        NOTE: It does not yet include references to external code lists and the additional code lists and extended
        values proposed in the Data Specification Technical Guidelines.

    Owner
        European Union

    Register manager
        European Commission, Joint Research Centre

    Control body
        Control body for the central INSPIRE registers and INSPIRE register federation

    Submitter
        Nominated submitting organizations for the central INSPIRE registers and INSPIRE register federation

    Contact point
        JRC INSPIRE Registry Team <inspire-registry-dev@jrc.ec.europa.eu>

    Licence
        Europa Legal Notice https://ec.europa.eu/info/legal-notice_en

    References
        https://inspire.ec.europa.eu/codelist

    """

    application_schema = models.ForeignKey(ApplicationSchema, on_delete=models.PROTECT)
    code = models.CharField(max_length=64, db_index=True)
    slug = models.CharField(max_length=64, blank=True, db_index=True)
    link = models.URLField(blank=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    label = models.CharField(max_length=128)
    definition = models.TextField(blank=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.PROTECT)
    themes = models.ManyToManyField(Theme)

    class Meta:
        verbose_name = _("Code list")
        verbose_name_plural = _("Code lists")
        ordering = ["code", "label"]

    def __str__(self):
        return "%s: %s" % (self.code, self.label)

    def save(self, *args, **kwargs):
        self.link = self.link.replace("http://", "https://")
        if not self.code:
            self.code = self.link.split("/")[-1]
        self.slug = slugify(self.code)[:64]
        return super().save(*args, **kwargs)


class CodeListValue(BaseInspireEUModel):
    code_list = models.ForeignKey(CodeList, on_delete=models.PROTECT)
    code = models.CharField(max_length=96, db_index=True)
    slug = models.CharField(max_length=96, blank=True, db_index=True)
    link = models.URLField()
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    label = models.CharField(max_length=200)
    definition = models.TextField(blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = _("Code list value")
        verbose_name_plural = _("Code list values")
        ordering = ["code_list__code", "code", "label"]

    def __str__(self):
        return "%s (%s): %s" % (self.code, self.code_list.code, self.label)

    def save(self, *args, **kwargs):
        if self.link:
            self.link = self.link.replace("http://", "https://")
        if not self.code:
            self.code = self.link.split("/")[-1]
        self.slug = slugify(self.code)[:96]
        return super().save(*args, **kwargs)

    @classmethod
    def search(cls, slug, code_list_slug=None, create=True):
        """Search CodeListValue

        Args:
            slug (str): Slug of CodeList
            code_list_slug (str, optional): Slug of CodeList foreign key. Defaults to None.
            create (bool, optional): If it does not exist, create a new one. Defaults to True.

        Raises:
            CodeList.DoesNotExist: When his foreign key does not exist
            CodeListValue.DoesNotExist: Only when `create` param is false

        Returns:
            CodeListValue: Row founded, or created
        """
        clv = None
        slug_list = slug.split("/")
        if not code_list_slug:
            code_list_slug = slug_list[-2]
        kw = dict(
            {
                "code_list__slug": slugify(code_list_slug),
                "slug": slugify(slug_list[-1]),
            },
        )
        try:
            clv = CodeListValue.objects.get(**kw)
        except CodeListValue.DoesNotExist:
            if create:
                kw_new = dict(
                    {
                        "code": slug_list[-1],
                        "label": slug_list[-1],
                        "definition": slug_list[-1],
                        "description": _("Created ad-hoc"),
                    },
                )
                try:
                    kw_new["code_list"] = CodeList.objects.get(
                        slug=kw["code_list__slug"],
                    )
                except CodeList.DoesNotExist:
                    msg = _(f"There is no CodeList with code '{code_list_slug}'")
                    raise CodeList.DoesNotExist(msg)
                kw_new["status"] = Status.objects.get(slug="valid")
                clv = CodeListValue.objects.create(**kw_new)
                msg = _(f"Created new CodeListValue: '{slug}' at '{code_list_slug}'")
                log.warning(msg)
            else:
                msg = _(f"There is no CodeListValue '{slug}' at '{code_list_slug}'")
                raise CodeListValue.DoesNotExist(msg)
        return clv


class UnitOfMeasure(BaseInspireEUModel):
    """Unit Of Measure

    Definition
        Any of the systems devised to measure some physical quantity such distance or area or a system devised
        to measure such things as the passage of time.

        The classes of UnitOfMeasure are determined by the member "measureType." Subclasses are not needed for
        implementation, but their use makes type constraints on measure valued attributes easier to specify.
        -- conversionToISOstandardUnit is not null only if the conversion is a simple scale

    References
        * `UnitOfMeasure Class <https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=1:3:7:1:1:1:1397>`_
        * `MeasureType Class <https://inspire.ec.europa.eu/data-model/approved/r4618-ir/html/index.htm?goto=1:3:7:1:1:1:1392>`_
    """  # noqa

    MEASURE_TYPE_UNKNOWN = ""
    MEASURE_TYPE_AREA = _("area")
    MEASURE_TYPE_LENGTH = _("length")
    MEASURE_TYPE_ANGLE = _("angle")
    MEASURE_TYPE_TIME = _("time")
    MEASURE_TYPE_VELOCITY = _("velocity")
    MEASURE_TYPE_VOLUME = _("volume")
    MEASURE_TYPE_SCALE = _("scale")
    MEASURE_TYPE_WEIGHT = _("weight")
    MEASURE_TYPE_CHOICES = (
        (MEASURE_TYPE_UNKNOWN, _("Unknown")),
        (MEASURE_TYPE_AREA, _("Area")),
        (MEASURE_TYPE_LENGTH, _("Length")),
        (MEASURE_TYPE_ANGLE, _("Angle")),
        (MEASURE_TYPE_TIME, _("Time")),
        (MEASURE_TYPE_VELOCITY, _("Velocity")),
        (MEASURE_TYPE_VOLUME, _("Volume")),
        (MEASURE_TYPE_SCALE, _("Scale")),
        (MEASURE_TYPE_WEIGHT, _("Weight")),
    )

    name = models.CharField(
        max_length=32,
        blank=True,
        help_text=_(
            "The name(s) of a particular unit of measure. Examples would include the following: "
            "1) for uomArea - square feet <br />"
            "2) for uomTime - seconds <br />"
            "3) for uomArea - miles<br />"
            "4) uomAngle - degrees.",
        ),
    )
    slug = models.CharField(max_length=32, blank=True, db_index=True)
    symbol = models.CharField(
        max_length=8,
        help_text=_(
            """The symbol used for this unit of measure, such at "ft" for feet, or "m" for meter.""",
        ),
    )
    measure_type = models.CharField(
        max_length=8,
        choices=MEASURE_TYPE_CHOICES,
        help_text=_("Measure Type"),
    )
    name_standard_unit = models.CharField(
        max_length=8,
        blank=True,
        help_text=_(
            "Name of the standard units to which this unit of measure can be directly converted. "
            "If this variable is NULL, then the standard unit for this measure type given by the local "
            "copy of the StandardsUnits code list.",
        ),
    )
    scale_to_standard_unit = models.FloatField(
        blank=True,
        null=True,
        help_text=_(
            "If the implementation system used for this object does not support NULL, the  scale set to 0 "
            "is equivalent to NULL for both scale and offset.<br />"
            "If X is the current unit, and S is the standard one the of two variables scale(ToStandardUnit) "
            "and offset(ToStandardUnit) can be used to make the conversion from X to S by:<br />"
            "S = offset + scale*X <br />"
            "and, conversely, <br />"
            "X = (S-offset)/scale",
        ),
    )
    offset_to_standard_unit = models.FloatField(
        blank=True,
        null=True,
        help_text=_(
            "See scaleToStandardUnit for a description. Again, this variable is NULL is no linear conversion "
            "is possible. If the two units are only a scale in difference, then this number is zero (0). "
            "If the implementation system used for this object does not support NULL, the then scale set "
            "to 0 is equivalent to NULL for both scale and offset.",
        ),
    )
    formula = models.CharField(
        blank=True,
        max_length=32,
        help_text=_(
            "An algebraic formula (probably in some programming language) converting this unit of measure "
            "(represented in the formula by its uomSymbol) to the ISO standard (represented by its symbol. "
            "This member attribute is not required, but it is a valuable piece of documentation. ",
        ),
    )

    # objects = models.Manager()
    # uom_length = models.Manager()
    # uom_area = models.Manager()
    # uom_length = models.Manager()
    # uom_angle = models.Manager()
    # uom_time = models.Manager()
    # uom_velocity = models.Manager()
    # uom_volume = models.Manager()
    # uom_scale = models.Manager()
    # uom_weight = models.Manager()

    class Meta:
        verbose_name = _("Unit Of Measure")
        verbose_name_plural = _("Units Of Measure")
        ordering = ["symbol", "name"]

    def __str__(self):
        return "%s %s" % (self.symbol, self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)[:32]
        return super().save(*args, **kwargs)
