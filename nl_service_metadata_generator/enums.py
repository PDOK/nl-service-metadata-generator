import enum


class NgrEnv(str, enum.Enum):
    PROD = "prod"
    ACC = "acc"


class ServiceType(str, enum.Enum):
    CSW = "csw"
    WMS = "wms"
    WMTS = "wmts"
    WFS = "wfs"
    WCS = "wcs"
    SOS = "sos"
    ATOM = "atom"
    TMS = "tms"
    OAF = "oaf"


class InspireType(str, enum.Enum):
    NETWORK = "network"
    OTHER = "other"
    NONE = "none"


class SdsType(str, enum.Enum):
    INVOCABLE = "invocable"
    INTEROPERABLE = "interoperable"
    HARMONISED = "harmonised"
