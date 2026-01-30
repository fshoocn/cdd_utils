from dataclasses import dataclass, field
from typing import Optional, Union, List


@dataclass
class Author:
    class Meta:
        name = "AUTHOR"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    obs: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    responsible: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    lastname: Optional[str] = field(
        default=None,
        metadata={
            "name": "LASTNAME",
            "type": "Element",
            "required": True,
        },
    )
    firstname: Optional[str] = field(
        default=None,
        metadata={
            "name": "FIRSTNAME",
            "type": "Element",
            "required": True,
        },
    )
    shortname: Optional[str] = field(
        default=None,
        metadata={
            "name": "SHORTNAME",
            "type": "Element",
            "required": True,
        },
    )
    company: Optional[str] = field(
        default=None,
        metadata={
            "name": "COMPANY",
            "type": "Element",
            "required": True,
        },
    )
    dept: Optional[str] = field(
        default=None,
        metadata={
            "name": "DEPT",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Comp:
    class Meta:
        name = "COMP"

    s: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    e: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    f: Optional[Union[int, float]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    div: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    o: Optional[Union[int, float]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class Cstr:
    class Meta:
        name = "CSTR"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    attrref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    commonstring: Optional[str] = field(
        default=None,
        metadata={
            "name": "COMMONSTRING",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Cvaluetype:
    class Meta:
        name = "CVALUETYPE"

    bl: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    bo: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    enc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    sig: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    df: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    qty: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    sz: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    minsz: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    maxsz: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "UNIT",
            "type": "Element",
        },
    )


@dataclass
class Dtcstatusbitgroup:
    class Meta:
        name = "DTCSTATUSBITGROUP"

    conv: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dtref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class EnumType:
    class Meta:
        name = "ENUM"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    attrref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Enumrecorditem:
    class Meta:
        name = "ENUMRECORDITEM"

    idref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Fc:
    class Meta:
        name = "FC"

    fs: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class Para:
    class Meta:
        name = "PARA"

    list_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "list",
            "type": "Attribute",
        },
    )
    fc: list[Union[Fc, str]] = field(
        default_factory=list,
        metadata={
            "name": "FC",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Tuv:
    class Meta:
        name = "TUV"

    lang: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "namespace": "http://www.w3.org/XML/1998/namespace",
            "required": True,
        },
    )
    uptodate: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    struct: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    para: list[Para] = field(
        default_factory=list,
        metadata={
            "name": "PARA",
            "type": "Element",
        },
    )
    value: Union[str, int, bool] = field(default="")


@dataclass
class Choice:
    class Meta:
        name = "CHOICE"

    tuv: list[Tuv] = field(
        default_factory=list,
        metadata={
            "name": "TUV",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Addinfo:
    class Meta:
        name = "ADDINFO"

    tuv: list[Tuv] = field(
        default_factory=list,
        metadata={
            "name": "TUV",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Caption:
    class Meta:
        name = "CAPTION"

    tuv: list[Tuv] = field(
        default_factory=list,
        metadata={
            "name": "TUV",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Filecontents:
    class Meta:
        name = "FILECONTENTS"

    len: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )


@dataclass
class Extdoc:
    class Meta:
        name = "EXTDOC"

    creationdt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    changedt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    filename: Optional[str] = field(
        default=None,
        metadata={
            "name": "FILENAME",
            "type": "Element",
            "required": True,
        },
    )
    filecontents: Optional[Filecontents] = field(
        default=None,
        metadata={
            "name": "FILECONTENTS",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Extstorageitem:
    class Meta:
        name = "EXTSTORAGEITEM"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    caption: Optional[Caption] = field(
        default=None,
        metadata={
            "name": "CAPTION",
            "type": "Element",
            "required": True,
        },
    )
    extdoc: Optional[Extdoc] = field(
        default=None,
        metadata={
            "name": "EXTDOC",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Histitem:
    class Meta:
        name = "HISTITEM"

    authorref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    stid: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    tool: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dt: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    label: Optional[str] = field(
        default=None,
        metadata={
            "name": "LABEL",
            "type": "Element",
            "required": True,
        },
    )
    mod: Optional[str] = field(
        default=None,
        metadata={
            "name": "MOD",
            "type": "Element",
            "required": True,
        },
    )
    reason: Optional[str] = field(
        default=None,
        metadata={
            "name": "REASON",
            "type": "Element",
        },
    )


@dataclass
class Histitems:
    class Meta:
        name = "HISTITEMS"

    histitem: list[Histitem] = field(
        default_factory=list,
        metadata={
            "name": "HISTITEM",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Negrescodeproxy:
    class Meta:
        name = "NEGRESCODEPROXY"

    idref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Proxycompref:
    class Meta:
        name = "PROXYCOMPREF"

    idref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Pvaluetype:
    class Meta:
        name = "PVALUETYPE"

    bl: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    bo: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    enc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    sig: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    df: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    qty: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    sz: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    minsz: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    maxsz: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    unit: Optional[str] = field(
        default=None,
        metadata={
            "name": "UNIT",
            "type": "Element",
        },
    )


@dataclass
class Qualgenoptions:
    class Meta:
        name = "QUALGENOPTIONS"

    case: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    min_len: Optional[int] = field(
        default=None,
        metadata={
            "name": "minLen",
            "type": "Attribute",
            "required": True,
        },
    )
    max_len: Optional[int] = field(
        default=None,
        metadata={
            "name": "maxLen",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Recordref:
    class Meta:
        name = "RECORDREF"

    idref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Snapshotdatadidref:
    class Meta:
        name = "SNAPSHOTDATADIDREF"

    did_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "didRef",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Staticcompref:
    class Meta:
        name = "STATICCOMPREF"

    idref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Staticvalue:
    class Meta:
        name = "STATICVALUE"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shstaticref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Default:
    class Meta:
        name = "DEFAULT"

    tuv: list[Tuv] = field(
        default_factory=list,
        metadata={
            "name": "TUV",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Uns:
    class Meta:
        name = "UNS"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    attrref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Unsrecorditem:
    class Meta:
        name = "UNSRECORDITEM"

    idref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Vckmgr:
    class Meta:
        name = "VCKMGR"

    vckmode: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    vckmin: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    vckmax: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    vcknext: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class Desc:
    class Meta:
        name = "DESC"

    tuv: list[Tuv] = field(
        default_factory=list,
        metadata={
            "name": "TUV",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Authors:
    class Meta:
        name = "AUTHORS"

    author: list[Author] = field(
        default_factory=list,
        metadata={
            "name": "AUTHOR",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Dtcstatusmask:
    class Meta:
        name = "DTCSTATUSMASK"

    dtref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dtcstatusbitgroup: list[Dtcstatusbitgroup] = field(
        default_factory=list,
        metadata={
            "name": "DTCSTATUSBITGROUP",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Etag:
    class Meta:
        name = "ETAG"

    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    tuv: list[Tuv] = field(
        default_factory=list,
        metadata={
            "name": "TUV",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Name:
    class Meta:
        name = "NAME"

    tuv: list[Tuv] = field(
        default_factory=list,
        metadata={
            "name": "TUV",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Negrescodeproxies:
    class Meta:
        name = "NEGRESCODEPROXIES"

    negrescodeproxy: list[Negrescodeproxy] = field(
        default_factory=list,
        metadata={
            "name": "NEGRESCODEPROXY",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Shortcutname:
    class Meta:
        name = "SHORTCUTNAME"

    tuv: list[Tuv] = field(
        default_factory=list,
        metadata={
            "name": "TUV",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class String:
    class Meta:
        name = "STRING"

    tuv: list[Tuv] = field(
        default_factory=list,
        metadata={
            "name": "TUV",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Text:
    class Meta:
        name = "TEXT"

    tuv: list[Tuv] = field(
        default_factory=list,
        metadata={
            "name": "TUV",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Excl:
    class Meta:
        name = "EXCL"
    # 当数据位数太多时，例如17个字节的无效值，可能出现<EXCL s='(48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48)' e='(48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48,48)' inv='invalidSignal'></EXCL>
    s: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    e: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    inv: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    text: Optional[Text] = field(
        default=None,
        metadata={
            "name": "TEXT",
            "type": "Element",
        },
    )


@dataclass
class Attrcat:
    class Meta:
        name = "ATTRCAT"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    usage: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    xauth: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Constcomp:
    class Meta:
        name = "CONSTCOMP"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    must: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    spec: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    bl: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    respsupbit: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Cstrdef:
    class Meta:
        name = "CSTRDEF"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    attrcatref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    restr: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    listable: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    xauth: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    may_be_reported: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeReported",
            "type": "Attribute",
        },
    )
    usage: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    commonstring: Optional[object] = field(
        default=None,
        metadata={
            "name": "COMMONSTRING",
            "type": "Element",
        },
    )


@dataclass
class Dataobj:
    class Meta:
        name = "DATAOBJ"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    spec: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    def_value: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "name": "def",
            "type": "Attribute",
        },
    )
    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    dtref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    data_object_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "dataObjectRef",
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Dclsrvtmpl:
    class Meta:
        name = "DCLSRVTMPL"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    tmplref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dtref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    conv: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    may_be_exec: Optional[str] = field(
        default=None,
        metadata={
            "name": "mayBeExec",
            "type": "Attribute",
        },
    )
    not_exec_in_state_groups: Optional[str] = field(
        default=None,
        metadata={
            "name": "notExecInStateGroups",
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    semantic: Optional[str] = field(
        default=None,
        metadata={
            "name": "SEMANTIC",
            "type": "Element",
        },
    )


@dataclass
class Didcommonsnapshotdata:
    class Meta:
        name = "DIDCOMMONSNAPSHOTDATA"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    support_dtc_specific_data: Optional[int] = field(
        default=None,
        metadata={
            "name": "supportDtcSpecificData",
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    snapshotdatadidref: list[Snapshotdatadidref] = field(
        default_factory=list,
        metadata={
            "name": "SNAPSHOTDATADIDREF",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Diddataref:
    class Meta:
        name = "DIDDATAREF"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    did_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "didRef",
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Doctmpl:
    class Meta:
        name = "DOCTMPL"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    saveno: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    label: Optional[str] = field(
        default=None,
        metadata={
            "name": "LABEL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Domaindataproxycomp:
    class Meta:
        name = "DOMAINDATAPROXYCOMP"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    must: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dest: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Enumdef:
    class Meta:
        name = "ENUMDEF"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    attrcatref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    xauth: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    restr: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    may_be_reported: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeReported",
            "type": "Attribute",
        },
    )
    usage: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    sort: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    etag: list[Etag] = field(
        default_factory=list,
        metadata={
            "name": "ETAG",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Enumrecorditemtmpl:
    class Meta:
        name = "ENUMRECORDITEMTMPL"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    may_be_dup: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeDup",
            "type": "Attribute",
            "required": True,
        },
    )
    conv: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    sort: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    etag: list[Etag] = field(
        default_factory=list,
        metadata={
            "name": "ETAG",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Gapdataobj:
    class Meta:
        name = "GAPDATAOBJ"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    bl: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Groupofdtcproxycomp:
    class Meta:
        name = "GROUPOFDTCPROXYCOMP"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    must: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dest: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    minbl: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    maxbl: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dtref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Ident:
    class Meta:
        name = "IDENT"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    bm: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    xauth: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    enum: Optional[EnumType] = field(
        default=None,
        metadata={
            "name": "ENUM",
            "type": "Element",
        },
    )
    cstr: list[Cstr] = field(
        default_factory=list,
        metadata={
            "name": "CSTR",
            "type": "Element",
        },
    )
    cvaluetype: Optional[Cvaluetype] = field(
        default=None,
        metadata={
            "name": "CVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    excl: list[Excl] = field(
        default_factory=list,
        metadata={
            "name": "EXCL",
            "type": "Element",
        },
    )
    pvaluetype: Optional[Pvaluetype] = field(
        default=None,
        metadata={
            "name": "PVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Jobcnr:
    class Meta:
        name = "JOBCNR"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    tmplref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    req: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Lincomp:
    class Meta:
        name = "LINCOMP"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    bm: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    cvaluetype: Optional[Cvaluetype] = field(
        default=None,
        metadata={
            "name": "CVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    excl: list[Excl] = field(
        default_factory=list,
        metadata={
            "name": "EXCL",
            "type": "Element",
        },
    )
    pvaluetype: Optional[Pvaluetype] = field(
        default=None,
        metadata={
            "name": "PVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    comp: Optional[Comp] = field(
        default=None,
        metadata={
            "name": "COMP",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Muxcomp:
    class Meta:
        name = "MUXCOMP"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    must: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    selref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    selbm: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dest: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    minbl: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    maxbl: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Negrescode:
    class Meta:
        name = "NEGRESCODE"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Service:
    class Meta:
        name = "SERVICE"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    tmplref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    func: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    phys: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    resp_on_phys: Optional[int] = field(
        default=None,
        metadata={
            "name": "respOnPhys",
            "type": "Attribute",
            "required": True,
        },
    )
    resp_on_func: Optional[int] = field(
        default=None,
        metadata={
            "name": "respOnFunc",
            "type": "Attribute",
            "required": True,
        },
    )
    req: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    may_be_exec: Optional[str] = field(
        default=None,
        metadata={
            "name": "mayBeExec",
            "type": "Attribute",
        },
    )
    trans: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    sprmibonfunc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    sprmibonphys: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    enum: list[EnumType] = field(
        default_factory=list,
        metadata={
            "name": "ENUM",
            "type": "Element",
        },
    )
    shortcutname: Optional[Shortcutname] = field(
        default=None,
        metadata={
            "name": "SHORTCUTNAME",
            "type": "Element",
            "required": True,
        },
    )
    shortcutqual: Optional[str] = field(
        default=None,
        metadata={
            "name": "SHORTCUTQUAL",
            "type": "Element",
            "required": True,
        },
    )
    semantic: Optional[str] = field(
        default=None,
        metadata={
            "name": "SEMANTIC",
            "type": "Element",
        },
    )


@dataclass
class Sgndef:
    class Meta:
        name = "SGNDEF"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    attrcatref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Shproxy:
    class Meta:
        name = "SHPROXY"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dest: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    spec: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    proxycompref: list[Proxycompref] = field(
        default_factory=list,
        metadata={
            "name": "PROXYCOMPREF",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Shstatic:
    class Meta:
        name = "SHSTATIC"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    spec: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    staticcompref: list[Staticcompref] = field(
        default_factory=list,
        metadata={
            "name": "STATICCOMPREF",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Simpleproxycomp:
    class Meta:
        name = "SIMPLEPROXYCOMP"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    must: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dest: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    minbl: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    maxbl: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    must_at_rt: Optional[int] = field(
        default=None,
        metadata={
            "name": "mustAtRT",
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Specdataobj:
    class Meta:
        name = "SPECDATAOBJ"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    negrescodeproxies: Optional[Negrescodeproxies] = field(
        default=None,
        metadata={
            "name": "NEGRESCODEPROXIES",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Specificsnapshotrecord:
    class Meta:
        name = "SPECIFICSNAPSHOTRECORD"

    rn: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    may_be_del: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeDel",
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    may_be_mod: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeMod",
            "type": "Attribute",
            "required": True,
        },
    )
    may_be_mod_data: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeModData",
            "type": "Attribute",
            "required": True,
        },
    )
    csd_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "csdRef",
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class State:
    class Meta:
        name = "STATE"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Staticcomp:
    class Meta:
        name = "STATICCOMP"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    must: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    spec: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dtref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    respsupbit: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Statusdtcproxycomp:
    class Meta:
        name = "STATUSDTCPROXYCOMP"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    must: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dest: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    minbl: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    maxbl: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Str:
    class Meta:
        name = "STR"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    attrref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    string: Optional[String] = field(
        default=None,
        metadata={
            "name": "STRING",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Strdef:
    class Meta:
        name = "STRDEF"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    attrcatref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    xauth: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    may_be_reported: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeReported",
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    string: Optional[String] = field(
        default=None,
        metadata={
            "name": "STRING",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Targetgroup:
    class Meta:
        name = "TARGETGROUP"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Textmap:
    class Meta:
        name = "TEXTMAP"

    s: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    e: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    text: Optional[Text] = field(
        default=None,
        metadata={
            "name": "TEXT",
            "type": "Element",
            "required": True,
        },
    )
    addinfo: Optional[Addinfo] = field(
        default=None,
        metadata={
            "name": "ADDINFO",
            "type": "Element",
        },
    )


@dataclass
class Trrecorditem:
    class Meta:
        name = "TRRECORDITEM"

    idref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    text: Optional[Text] = field(
        default=None,
        metadata={
            "name": "TEXT",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Trrecorditemtmpl:
    class Meta:
        name = "TRRECORDITEMTMPL"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    may_be_dup: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeDup",
            "type": "Attribute",
            "required": True,
        },
    )
    conv: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    default: Optional[Default] = field(
        default=None,
        metadata={
            "name": "DEFAULT",
            "type": "Element",
        },
    )
    choice: list[Choice] = field(
        default_factory=list,
        metadata={
            "name": "CHOICE",
            "type": "Element",
        },
    )


@dataclass
class Unsdef:
    class Meta:
        name = "UNSDEF"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    attrcatref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    xauth: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    may_be_reported: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeReported",
            "type": "Attribute",
        },
    )
    usage: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    restr: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    df: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Unsrecorditemtmpl:
    class Meta:
        name = "UNSRECORDITEMTMPL"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    may_be_dup: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeDup",
            "type": "Attribute",
            "required": True,
        },
    )
    conv: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    df: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
            "required": True,
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Attrcats:
    class Meta:
        name = "ATTRCATS"

    attrcat: list[Attrcat] = field(
        default_factory=list,
        metadata={
            "name": "ATTRCAT",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Dataobjatts:
    class Meta:
        name = "DATAOBJATTS"

    strdef: list[Strdef] = field(
        default_factory=list,
        metadata={
            "name": "STRDEF",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    enumdef: list[Enumdef] = field(
        default_factory=list,
        metadata={
            "name": "ENUMDEF",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    cstrdef: list[Cstrdef] = field(
        default_factory=list,
        metadata={
            "name": "CSTRDEF",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Datatypeatts:
    class Meta:
        name = "DATATYPEATTS"

    enumdef: list[Enumdef] = field(
        default_factory=list,
        metadata={
            "name": "ENUMDEF",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    cstrdef: list[Cstrdef] = field(
        default_factory=list,
        metadata={
            "name": "CSTRDEF",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )


@dataclass
class Dclsrvtmplatts:
    class Meta:
        name = "DCLSRVTMPLATTS"

    cstrdef: list[Cstrdef] = field(
        default_factory=list,
        metadata={
            "name": "CSTRDEF",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    strdef: Optional[Strdef] = field(
        default=None,
        metadata={
            "name": "STRDEF",
            "type": "Element",
            "required": True,
        },
    )
    enumdef: Optional[Enumdef] = field(
        default=None,
        metadata={
            "name": "ENUMDEF",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Dcltmpl:
    class Meta:
        name = "DCLTMPL"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    cls: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    single: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    is_relevant_for_req: Optional[int] = field(
        default=None,
        metadata={
            "name": "isRelevantForReq",
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    enum: Optional[EnumType] = field(
        default=None,
        metadata={
            "name": "ENUM",
            "type": "Element",
        },
    )
    cstr: list[Cstr] = field(
        default_factory=list,
        metadata={
            "name": "CSTR",
            "type": "Element",
        },
    )
    str_value: Optional[Str] = field(
        default=None,
        metadata={
            "name": "STR",
            "type": "Element",
        },
    )
    dclsrvtmpl: list[Dclsrvtmpl] = field(
        default_factory=list,
        metadata={
            "name": "DCLSRVTMPL",
            "type": "Element",
        },
    )
    # 通常为子功能映射，只有一个
    shstatic: Optional[Shstatic] = field(
        default=None,
        metadata={
            "name": "SHSTATIC",
            "type": "Element",
        },
    )
    shproxy: list[Shproxy] = field(
        default_factory=list,
        metadata={
            "name": "SHPROXY",
            "type": "Element",
        },
    )


@dataclass
class Diagclassatts:
    class Meta:
        name = "DIAGCLASSATTS"

    enumdef: list[Enumdef] = field(
        default_factory=list,
        metadata={
            "name": "ENUMDEF",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Dcltmplatts:
    class Meta:
        name = "DCLTMPLATTS"

    enumdef: Optional[Enumdef] = field(
        default=None,
        metadata={
            "name": "ENUMDEF",
            "type": "Element",
            "required": True,
        },
    )
    cstrdef: list[Cstrdef] = field(
        default_factory=list,
        metadata={
            "name": "CSTRDEF",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    strdef: Optional[Strdef] = field(
        default=None,
        metadata={
            "name": "STRDEF",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Diaginstatts:
    class Meta:
        name = "DIAGINSTATTS"

    enumdef: list[Enumdef] = field(
        default_factory=list,
        metadata={
            "name": "ENUMDEF",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    unsdef: list[Unsdef] = field(
        default_factory=list,
        metadata={
            "name": "UNSDEF",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    cstrdef: list[Cstrdef] = field(
        default_factory=list,
        metadata={
            "name": "CSTRDEF",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )



@dataclass
class Didatts:
    class Meta:
        name = "DIDATTS"

    cstrdef: Optional[Cstrdef] = field(
        default=None,
        metadata={
            "name": "CSTRDEF",
            "type": "Element",
            "required": True,
        },
    )
    unsdef: Optional[Unsdef] = field(
        default=None,
        metadata={
            "name": "UNSDEF",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Didref:
    class Meta:
        name = "DIDREF"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    did_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "didRef",
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
        },
    )
    dataobj: Optional[Dataobj] = field(
        default=None,
        metadata={
            "name": "DATAOBJ",
            "type": "Element",
        },
    )


@dataclass
class Ecuatts:
    class Meta:
        name = "ECUATTS"

    enumdef: list[Enumdef] = field(
        default_factory=list,
        metadata={
            "name": "ENUMDEF",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    unsdef: list[Unsdef] = field(
        default_factory=list,
        metadata={
            "name": "UNSDEF",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    cstrdef: list[Cstrdef] = field(
        default_factory=list,
        metadata={
            "name": "CSTRDEF",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    strdef: list[Strdef] = field(
        default_factory=list,
        metadata={
            "name": "STRDEF",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )


@dataclass
class Jobatts:
    class Meta:
        name = "JOBATTS"

    enumdef: list[Enumdef] = field(
        default_factory=list,
        metadata={
            "name": "ENUMDEF",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Jobcnratts:
    class Meta:
        name = "JOBCNRATTS"

    enumdef: Optional[Enumdef] = field(
        default=None,
        metadata={
            "name": "ENUMDEF",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Eositerdt:
    class Meta:
        name = "EOSITERDT"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    bm: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    min_num_of_items: Optional[int] = field(
        default=None,
        metadata={
            "name": "minNumOfItems",
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    cvaluetype: Optional[Cvaluetype] = field(
        default=None,
        metadata={
            "name": "CVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    pvaluetype: Optional[Pvaluetype] = field(
        default=None,
        metadata={
            "name": "PVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    dataobj: list[Dataobj] = field(
        default_factory=list,
        metadata={
            "name": "DATAOBJ",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Eventatts:
    class Meta:
        name = "EVENTATTS"

    cstrdef: Optional[Cstrdef] = field(
        default=None,
        metadata={
            "name": "CSTRDEF",
            "type": "Element",
            "required": True,
        },
    )
    

@dataclass
class Extstorageitems:
    class Meta:
        name = "EXTSTORAGEITEMS"

    extstorageitem: Optional[Extstorageitem] = field(
        default=None,
        metadata={
            "name": "EXTSTORAGEITEM",
            "type": "Element",
            "required": True,
        },
    )

@dataclass
class Negrescodes:
    class Meta:
        name = "NEGRESCODES"

    bl: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    bo: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    state_group_default: Optional[int] = field(
        default=None,
        metadata={
            "name": "stateGroupDefault",
            "type": "Attribute",
            "required": True,
        },
    )
    negrescode: list[Negrescode] = field(
        default_factory=list,
        metadata={
            "name": "NEGRESCODE",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Numitercomp:
    class Meta:
        name = "NUMITERCOMP"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    must: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    selref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    selbm: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    simpleproxycomp: Optional[Simpleproxycomp] = field(
        default=None,
        metadata={
            "name": "SIMPLEPROXYCOMP",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Record:
    class Meta:
        name = "RECORD"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    v: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    text: Optional[Text] = field(
        default=None,
        metadata={
            "name": "TEXT",
            "type": "Element",
            "required": True,
        },
    )
    trrecorditem: list[Trrecorditem] = field(
        default_factory=list,
        metadata={
            "name": "TRRECORDITEM",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    unsrecorditem: list[Unsrecorditem] = field(
        default_factory=list,
        metadata={
            "name": "UNSRECORDITEM",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    enumrecorditem: list[Enumrecorditem] = field(
        default_factory=list,
        metadata={
            "name": "ENUMRECORDITEM",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    enum: list[EnumType] = field(
        default_factory=list,
        metadata={
            "name": "ENUM",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    cstr: list[Cstr] = field(
        default_factory=list,
        metadata={
            "name": "CSTR",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 2,
        },
    )
    uns: list[Uns] = field(
        default_factory=list,
        metadata={
            "name": "UNS",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 2,
        },
    )


@dataclass
class Recordatts:
    class Meta:
        name = "RECORDATTS"

    enumdef: list[Enumdef] = field(
        default_factory=list,
        metadata={
            "name": "ENUMDEF",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    cstrdef: list[Cstrdef] = field(
        default_factory=list,
        metadata={
            "name": "CSTRDEF",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    unsdef: list[Unsdef] = field(
        default_factory=list,
        metadata={
            "name": "UNSDEF",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )


@dataclass
class Recordtmpl:
    class Meta:
        name = "RECORDTMPL"

    spec: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    cvaluetype: Optional[Cvaluetype] = field(
        default=None,
        metadata={
            "name": "CVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    pvaluetype: Optional[Pvaluetype] = field(
        default=None,
        metadata={
            "name": "PVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    trrecorditemtmpl: list[Trrecorditemtmpl] = field(
        default_factory=list,
        metadata={
            "name": "TRRECORDITEMTMPL",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    unsrecorditemtmpl: list[Unsrecorditemtmpl] = field(
        default_factory=list,
        metadata={
            "name": "UNSRECORDITEMTMPL",
            "type": "Element",
            "sequence": 1,
        },
    )
    enumrecorditemtmpl: list[Enumrecorditemtmpl] = field(
        default_factory=list,
        metadata={
            "name": "ENUMRECORDITEMTMPL",
            "type": "Element",
            "sequence": 1,
        },
    )


@dataclass
class Serviceatts:
    class Meta:
        name = "SERVICEATTS"

    enumdef: list[Enumdef] = field(
        default_factory=list,
        metadata={
            "name": "ENUMDEF",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    strdef: list[Strdef] = field(
        default_factory=list,
        metadata={
            "name": "STRDEF",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    sgndef: list[Sgndef] = field(
        default_factory=list,
        metadata={
            "name": "SGNDEF",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )


@dataclass
class Shproxyatts:
    class Meta:
        name = "SHPROXYATTS"

    cstrdef: list[Cstrdef] = field(
        default_factory=list,
        metadata={
            "name": "CSTRDEF",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    strdef: Optional[Strdef] = field(
        default=None,
        metadata={
            "name": "STRDEF",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Snapshotrecords:
    class Meta:
        name = "SNAPSHOTRECORDS"

    specificsnapshotrecord: list[Specificsnapshotrecord] = field(
        default_factory=list,
        metadata={
            "name": "SPECIFICSNAPSHOTRECORD",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Stategroup:
    class Meta:
        name = "STATEGROUP"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    spec: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    state: list[State] = field(
        default_factory=list,
        metadata={
            "name": "STATE",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    negrescodeproxy: Optional[Negrescodeproxy] = field(
        default=None,
        metadata={
            "name": "NEGRESCODEPROXY",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Stategroupatts:
    class Meta:
        name = "STATEGROUPATTS"

    cstrdef: Optional[Cstrdef] = field(
        default=None,
        metadata={
            "name": "CSTRDEF",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Struct:
    class Meta:
        name = "STRUCT"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    spec: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dtref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    items: list[Union[Dataobj, Gapdataobj]] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "DATAOBJ",
                    "type": Dataobj,
                },
                {
                    "name": "GAPDATAOBJ",
                    "type": Gapdataobj,
                },
            ),
        },
    )


@dataclass
class Targetgroups:
    class Meta:
        name = "TARGETGROUPS"

    targetgroup: list[Targetgroup] = field(
        default_factory=list,
        metadata={
            "name": "TARGETGROUP",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Texttbl:
    class Meta:
        name = "TEXTTBL"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    bm: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    xauth: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
               default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    enum: Optional[EnumType] = field(
        default=None,
        metadata={
            "name": "ENUM",
            "type": "Element",
        },
    )
    cstr: list[Cstr] = field(
        default_factory=list,
        metadata={
            "name": "CSTR",
            "type": "Element",
        },
    )
    cvaluetype: Optional[Cvaluetype] = field(
        default=None,
        metadata={
            "name": "CVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    excl: list[Excl] = field(
        default_factory=list,
        metadata={
            "name": "EXCL",
            "type": "Element",
        },
    )
    pvaluetype: Optional[Pvaluetype] = field(
        default=None,
        metadata={
            "name": "PVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    textmap: list[Textmap] = field(
        default_factory=list,
        metadata={
            "name": "TEXTMAP",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Varatts:
    class Meta:
        name = "VARATTS"

    enumdef: Optional[Enumdef] = field(
        default=None,
        metadata={
            "name": "ENUMDEF",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Dcltmpls:
    class Meta:
        name = "DCLTMPLS"

    dcltmpl: list[Dcltmpl] = field(
        default_factory=list,
        metadata={
            "name": "DCLTMPL",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Defatts:
    class Meta:
        name = "DEFATTS"
    dataobjatts: Optional[Dataobjatts] = field(
        default=None,
        metadata={
            "name": "DATAOBJATTS",
            "type": "Element",
            "required": True,
        },
    )
    datatypeatts: Optional[Datatypeatts] = field(
        default=None,
        metadata={
            "name": "DATATYPEATTS",
            "type": "Element",
            "required": True,
        },
    )
    diagclassatts: Optional[Diagclassatts] = field(
        default=None,
        metadata={
            "name": "DIAGCLASSATTS",
            "type": "Element",
            "required": True,
        },
    )
    diaginstatts: Optional[Diaginstatts] = field(
        default=None,
        metadata={
            "name": "DIAGINSTATTS",
            "type": "Element",
            "required": True,
        },
    )
    ecuatts: Optional[Ecuatts] = field(
        default=None,
        metadata={
            "name": "ECUATTS",
            "type": "Element",
            "required": True,
        },
    )
    jobatts: Optional[Jobatts] = field(
        default=None,
        metadata={
            "name": "JOBATTS",
            "type": "Element",
            "required": True,
        },
    )
    jobcnratts: Optional[Jobcnratts] = field(
        default=None,
        metadata={
            "name": "JOBCNRATTS",
            "type": "Element",
            "required": True,
        },
    )
    recordatts: Optional[Recordatts] = field(
        default=None,
        metadata={
            "name": "RECORDATTS",
            "type": "Element",
            "required": True,
        },
    )
    serviceatts: Optional[Serviceatts] = field(
        default=None,
        metadata={
            "name": "SERVICEATTS",
            "type": "Element",
            "required": True,
        },
    )
    varatts: Optional[Varatts] = field(
        default=None,
        metadata={
            "name": "VARATTS",
            "type": "Element",
            "required": True,
        },
    )
    stategroupatts: Optional[Stategroupatts] = field(
        default=None,
        metadata={
            "name": "STATEGROUPATTS",
            "type": "Element",
            "required": True,
        },
    )
    dcltmplatts: Optional[Dcltmplatts] = field(
        default=None,
        metadata={
            "name": "DCLTMPLATTS",
            "type": "Element",
            "required": True,
        },
    )
    dclsrvtmplatts: Optional[Dclsrvtmplatts] = field(
        default=None,
        metadata={
            "name": "DCLSRVTMPLATTS",
            "type": "Element",
            "required": True,
        },
    )
    shproxyatts: Optional[Shproxyatts] = field(
        default=None,
        metadata={
            "name": "SHPROXYATTS",
            "type": "Element",
            "required": True,
        },
    )
    didatts: Optional[Didatts] = field(
        default=None,
        metadata={
            "name": "DIDATTS",
            "type": "Element",
            "required": True,
        },
    )
    eventatts: Optional[Eventatts] = field(
        default=None,
        metadata={
            "name": "EVENTATTS",
            "type": "Element",
            "required": True,
        },
    )

@dataclass
class Didrefs:
    class Meta:
        name = "DIDREFS"

    didref: list[Didref] = field(
        default_factory=list,
        metadata={
            "name": "DIDREF",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Godtcdataobj:
    class Meta:
        name = "GODTCDATAOBJ"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    spec: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    individual_dtcs: Optional[int] = field(
        default=None,
        metadata={
            "name": "individualDtcs",
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    texttbl: Optional[Texttbl] = field(
        default=None,
        metadata={
            "name": "TEXTTBL",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Recorddt:
    class Meta:
        name = "RECORDDT"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    bm: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    rt_spec: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtSpec",
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    cvaluetype: Optional[Cvaluetype] = field(
        default=None,
        metadata={
            "name": "CVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    pvaluetype: Optional[Pvaluetype] = field(
        default=None,
        metadata={
            "name": "PVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    record: list[Record] = field(
        default_factory=list,
        metadata={
            "name": "RECORD",
            "type": "Element",
            "sequence": 1,
        },
    )
    recordref: list[Recordref] = field(
        default_factory=list,
        metadata={
            "name": "RECORDREF",
            "type": "Element",
            "sequence": 1,
        },
    )


@dataclass
class Recordtmpls:
    class Meta:
        name = "RECORDTMPLS"

    recordtmpl: list[Recordtmpl] = field(
        default_factory=list,
        metadata={
            "name": "RECORDTMPL",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Stategroups:
    class Meta:
        name = "STATEGROUPS"

    stategroup: list[Stategroup] = field(
        default_factory=list,
        metadata={
            "name": "STATEGROUP",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Structdt:
    class Meta:
        name = "STRUCTDT"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    bm: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    cvaluetype: Optional[Cvaluetype] = field(
        default=None,
        metadata={
            "name": "CVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    pvaluetype: Optional[Pvaluetype] = field(
        default=None,
        metadata={
            "name": "PVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    dataobj: Optional[Dataobj] = field(
        default=None,
        metadata={
            "name": "DATAOBJ",
            "type": "Element",
        },
    )
    struct: Optional[Struct] = field(
        default=None,
        metadata={
            "name": "STRUCT",
            "type": "Element",
        },
    )


@dataclass
class Structure:
    class Meta:
        name = "STRUCTURE"

    items: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "DATAOBJ",
                    "type": Dataobj,
                },
                {
                    "name": "STRUCT",
                    "type": Struct,
                },
                {
                    "name": "GAPDATAOBJ",
                    "type": Gapdataobj,
                },
                {
                    "name": "DIDREF",
                    "type": Didref,
                },
            ),
        },
    )


@dataclass
class Anycommonsnapshotdata:
    class Meta:
        name = "ANYCOMMONSNAPSHOTDATA"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    support_dtc_specific_data: Optional[int] = field(
        default=None,
        metadata={
            "name": "supportDtcSpecificData",
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    structure: Optional[Structure] = field(
        default=None,
        metadata={
            "name": "STRUCTURE",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Case:
    class Meta:
        name = "CASE"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    s: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    e: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    structure: Optional[Structure] = field(
        default=None,
        metadata={
            "name": "STRUCTURE",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Did:
    class Meta:
        name = "DID"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    n: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    structure: Optional[Structure] = field(
        default=None,
        metadata={
            "name": "STRUCTURE",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Extendeddatarecord:
    class Meta:
        name = "EXTENDEDDATARECORD"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    rn: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    may_be_mod: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeMod",
            "type": "Attribute",
            "required": True,
        },
    )
    may_be_del: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeDel",
            "type": "Attribute",
            "required": True,
        },
    )
    may_be_mod_data: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeModData",
            "type": "Attribute",
            "required": True,
        },
    )
    support_edr_for_dtc: Optional[int] = field(
        default=None,
        metadata={
            "name": "supportEdrForDtc",
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    structure: Optional[Structure] = field(
        default=None,
        metadata={
            "name": "STRUCTURE",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Recorddataobj:
    class Meta:
        name = "RECORDDATAOBJ"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    rt_spec: Optional[str] = field(
        default=None,
        metadata={
            "name": "rtSpec",
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    recorddt: Optional[Recorddt] = field(
        default=None,
        metadata={
            "name": "RECORDDT",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Recorddtpool:
    class Meta:
        name = "RECORDDTPOOL"

    recorddt: list[Recorddt] = field(
        default_factory=list,
        metadata={
            "name": "RECORDDT",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Commonsnapshotdatapool:
    class Meta:
        name = "COMMONSNAPSHOTDATAPOOL"

    anycommonsnapshotdata: list[Anycommonsnapshotdata] = field(
        default_factory=list,
        metadata={
            "name": "ANYCOMMONSNAPSHOTDATA",
            "type": "Element",
            "required": True,
        },
    )
    didcommonsnapshotdata: list[Didcommonsnapshotdata] = field(
        default_factory=list,
        metadata={
            "name": "DIDCOMMONSNAPSHOTDATA",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Dids:
    class Meta:
        name = "DIDS"

    did: list[Did] = field(
        default_factory=list,
        metadata={
            "name": "DID",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Extendeddatarecords:
    class Meta:
        name = "EXTENDEDDATARECORDS"

    extendeddatarecord: list[Extendeddatarecord] = field(
        default_factory=list,
        metadata={
            "name": "EXTENDEDDATARECORD",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Muxdt:
    class Meta:
        name = "MUXDT"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    bm: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dtref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    cvaluetype: Optional[Cvaluetype] = field(
        default=None,
        metadata={
            "name": "CVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    pvaluetype: Optional[Pvaluetype] = field(
        default=None,
        metadata={
            "name": "PVALUETYPE",
            "type": "Element",
            "required": True,
        },
    )
    structure: Optional[Structure] = field(
        default=None,
        metadata={
            "name": "STRUCTURE",
            "type": "Element",
            "required": True,
        },
    )
    case: list[Case] = field(
        default_factory=list,
        metadata={
            "name": "CASE",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Simplecompcont:
    class Meta:
        name = "SIMPLECOMPCONT"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    shproxyref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    items: List[Union[Specdataobj, Dataobj, Godtcdataobj, Struct, Recorddataobj, Diddataref, Gapdataobj]] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "SPECDATAOBJ",
                    "type": Specdataobj,
                },
                {
                    "name": "DATAOBJ",
                    "type": Dataobj,
                },
                {
                    "name": "GODTCDATAOBJ",
                    "type": Godtcdataobj,
                },
                {
                    "name": "STRUCT",
                    "type": Struct,
                },
                {
                    "name": "RECORDDATAOBJ",
                    "type": Recorddataobj,
                },
                {
                    "name": "DIDDATAREF",
                    "type": Diddataref,
                },
                {
                    "name": "GAPDATAOBJ",
                    "type": Gapdataobj,
                },
            ),
        },
    )
    value: str = field(default="")


@dataclass
class Contentcomp:
    class Meta:
        name = "CONTENTCOMP"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    must: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    simplecompcont: Optional[Simplecompcont] = field(
        default=None,
        metadata={
            "name": "SIMPLECOMPCONT",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Datatypes:
    class Meta:
        name = "DATATYPES"

    ident: list[Ident] = field(
        default_factory=list,
        metadata={
            "name": "IDENT",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    texttbl: list[Texttbl] = field(
        default_factory=list,
        metadata={
            "name": "TEXTTBL",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    lincomp: list[Lincomp] = field(
        default_factory=list,
        metadata={
            "name": "LINCOMP",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    structdt: list[Structdt] = field(
        default_factory=list,
        metadata={
            "name": "STRUCTDT",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 2,
        },
    )
    muxdt: list[Muxdt] = field(
        default_factory=list,
        metadata={
            "name": "MUXDT",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    eositerdt: list[Eositerdt] = field(
        default_factory=list,
        metadata={
            "name": "EOSITERDT",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 2,
        },
    )


@dataclass
class Muxcompcont:
    class Meta:
        name = "MUXCOMPCONT"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    shproxyref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    muxdt: Optional[Muxdt] = field(
        default=None,
        metadata={
            "name": "MUXDT",
            "type": "Element",
            "required": True,
        },
    )
    dataobj: Optional[Dataobj] = field(
        default=None,
        metadata={
            "name": "DATAOBJ",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Diaginst:
    class Meta:
        name = "DIAGINST"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    tmplref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    act: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    req: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    xauth: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    enum: List[EnumType] = field(
        default_factory=list,
        metadata={
            "name": "ENUM",
            "type": "Element",
        },
    )
    service: list[Service] = field(
        default_factory=list,
        metadata={
            "name": "SERVICE",
            "type": "Element",
        },
    )
    staticvalue: Optional[Staticvalue] = field(
        default=None,
        metadata={
            "name": "STATICVALUE",
            "type": "Element",
        },
    )
    items: List[Union[Simplecompcont, Muxcompcont]] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "SIMPLECOMPCONT",
                    "type": Simplecompcont,
                },
                {
                    "name": "MUXCOMPCONT",
                    "type": Muxcompcont,
                },
            ),
        },
    )
    eventdata: List[str] = field(
        default_factory=list,
        metadata={
            "name": "EVENTDATA",
            "type": "Element",
        },
    )


@dataclass
class Faultmemory:
    class Meta:
        name = "FAULTMEMORY"

    may_be_add_del_sr: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeAddDelSr",
            "type": "Attribute",
            "required": True,
        },
    )
    support_dtc_specific_data: Optional[int] = field(
        default=None,
        metadata={
            "name": "supportDtcSpecificData",
            "type": "Attribute",
            "required": True,
        },
    )
    force_same_snapshot_data: Optional[int] = field(
        default=None,
        metadata={
            "name": "forceSameSnapshotData",
            "type": "Attribute",
            "required": True,
        },
    )
    force_did_snapshot_data: Optional[int] = field(
        default=None,
        metadata={
            "name": "forceDidSnapshotData",
            "type": "Attribute",
            "required": True,
        },
    )
    may_be_add_del_edr: Optional[int] = field(
        default=None,
        metadata={
            "name": "mayBeAddDelEdr",
            "type": "Attribute",
            "required": True,
        },
    )
    support_edr_for_dtc: Optional[int] = field(
        default=None,
        metadata={
            "name": "supportEdrForDtc",
            "type": "Attribute",
            "required": True,
        },
    )
    commonsnapshotdatapool: Optional[Commonsnapshotdatapool] = field(
        default=None,
        metadata={
            "name": "COMMONSNAPSHOTDATAPOOL",
            "type": "Element",
            "required": True,
        },
    )
    snapshotrecords: Optional[Snapshotrecords] = field(
        default=None,
        metadata={
            "name": "SNAPSHOTRECORDS",
            "type": "Element",
            "required": True,
        },
    )
    extendeddatarecords: Optional[Extendeddatarecords] = field(
        default=None,
        metadata={
            "name": "EXTENDEDDATARECORDS",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Diagclass:
    class Meta:
        name = "DIAGCLASS"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    tmplref: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    diaginst: list[Diaginst] = field(
        default_factory=list,
        metadata={
            "name": "DIAGINST",
            "type": "Element",
        },
    )


@dataclass
class Eositercomp:
    class Meta:
        name = "EOSITERCOMP"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    must: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    min_num_of_items: Optional[int] = field(
        default=None,
        metadata={
            "name": "minNumOfItems",
            "type": "Attribute",
            "required": True,
        },
    )
    max_num_of_items: Optional[int] = field(
        default=None,
        metadata={
            "name": "maxNumOfItems",
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    items: List[Union[Constcomp, Contentcomp, Statusdtcproxycomp, Domaindataproxycomp, Simpleproxycomp, Muxcomp]] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "CONSTCOMP",
                    "type": Constcomp,
                },
                {
                    "name": "CONTENTCOMP",
                    "type": Contentcomp,
                },
                {
                    "name": "STATUSDTCPROXYCOMP",
                    "type": Statusdtcproxycomp,
                },
                {
                    "name": "DOMAINDATAPROXYCOMP",
                    "type": Domaindataproxycomp,
                },
                {
                    "name": "SIMPLEPROXYCOMP",
                    "type": Simpleproxycomp,
                },
                {
                    "name": "MUXCOMP",
                    "type": Muxcomp,
                },
            ),
        },
    )


@dataclass
class Unsuppsrvneg:
    class Meta:
        name = "UNSUPPSRVNEG"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    constcomp: Optional[Constcomp] = field(
        default=None,
        metadata={
            "name": "CONSTCOMP",
            "type": "Element",
            "required": True,
        },
    )
    staticcomp: Optional[Staticcomp] = field(
        default=None,
        metadata={
            "name": "STATICCOMP",
            "type": "Element",
            "required": True,
        },
    )
    contentcomp: Optional[Contentcomp] = field(
        default=None,
        metadata={
            "name": "CONTENTCOMP",
            "type": "Element",
            "required": True,
        },
    )

@dataclass
class Req:
    class Meta:
        name = "REQ"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    items: List[Union[Constcomp,Statusdtcproxycomp,Simpleproxycomp,Muxcomp,Contentcomp,Staticcomp,Eositercomp,Domaindataproxycomp,Groupofdtcproxycomp,Numitercomp]] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "CONSTCOMP",
                    "type": Constcomp,
                },
                {
                    "name": "STATUSDTCPROXYCOMP",
                    "type": Statusdtcproxycomp,
                },
                {
                    "name": "SIMPLEPROXYCOMP",
                    "type": Simpleproxycomp,
                },
                {
                    "name": "MUXCOMP",
                    "type": Muxcomp,
                },
                {
                    "name": "CONTENTCOMP",
                    "type": Contentcomp,
                },
                {
                    "name": "STATICCOMP",
                    "type": Staticcomp,
                },
                {
                    "name": "EOSITERCOMP",
                    "type": Eositercomp,
                },
                {
                    "name": "DOMAINDATAPROXYCOMP",
                    "type": Domaindataproxycomp,
                },
                {
                    "name": "GROUPOFDTCPROXYCOMP",
                    "type": Groupofdtcproxycomp,
                },
                {
                    "name": "NUMITERCOMP",
                    "type": Numitercomp,
                },
            ),
        },
    )
    # constcomp: list[Constcomp] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "CONSTCOMP",
    #         "type": "Element",
    #         "min_occurs": 1,
    #         "sequence": 1,
    #     },
    # )
    # statusdtcproxycomp: list[Statusdtcproxycomp] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "STATUSDTCPROXYCOMP",
    #         "type": "Element",
    #         "sequence": 1,
    #     },
    # )
    # simpleproxycomp: list[Simpleproxycomp] = field(
    #     default_factory=list,
    #     metadata={
    #         "name": "SIMPLEPROXYCOMP",
    #         "type": "Element",
    #     },
    # )
    # muxcomp: Optional[Muxcomp] = field(
    #     default=None,
    #     metadata={
    #         "name": "MUXCOMP",
    #         "type": "Element",
    #     },
    # )
    # contentcomp: Optional[Contentcomp] = field(
    #     default=None,
    #     metadata={
    #         "name": "CONTENTCOMP",
    #         "type": "Element",
    #     },
    # )
    # staticcomp: Optional[Staticcomp] = field(
    #     default=None,
    #     metadata={
    #         "name": "STATICCOMP",
    #         "type": "Element",
    #     },
    # )
    # eositercomp: Optional[Eositercomp] = field(
    #     default=None,
    #     metadata={
    #         "name": "EOSITERCOMP",
    #         "type": "Element",
    #     },
    # )
    # domaindataproxycomp: Optional[Domaindataproxycomp] = field(
    #     default=None,
    #     metadata={
    #         "name": "DOMAINDATAPROXYCOMP",
    #         "type": "Element",
    #     },
    # )
    # groupofdtcproxycomp: Optional[Groupofdtcproxycomp] = field(
    #     default=None,
    #     metadata={
    #         "name": "GROUPOFDTCPROXYCOMP",
    #         "type": "Element",
    #     },
    # )
    # numitercomp: Optional[Numitercomp] = field(
    #     default=None,
    #     metadata={
    #         "name": "NUMITERCOMP",
    #         "type": "Element",
    #     },
    # )

@dataclass
class Var:
    class Meta:
        name = "VAR"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    base: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    didrefs: Optional[Didrefs] = field(
        default=None,
        metadata={
            "name": "DIDREFS",
            "type": "Element",
            "required": True,
        },
    )
    diag: List[Union[Diagclass,Diaginst]] = field(
        default_factory=list,
        metadata={
            "type": "Elements",
            "choices": (
                {
                    "name": "DIAGCLASS",
                    "type": Diagclass,
                },
                {
                    "name": "DIAGINST",
                    "type": Diaginst,
                },
            ),
        },
    )

    jobcnr: list[Jobcnr] = field(
        default_factory=list,
        metadata={
            "name": "JOBCNR",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Ecu:
    class Meta:
        name = "ECU"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    max_combined_service_ids: Optional[int] = field(
        default=None,
        metadata={
            "name": "maxCombinedServiceIds",
            "type": "Attribute",
            "required": True,
        },
    )
    max_ecu_scheduler_ids: Optional[int] = field(
        default=None,
        metadata={
            "name": "maxEcuSchedulerIds",
            "type": "Attribute",
            "required": True,
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    uns: list[Uns] = field(
        default_factory=list,
        metadata={
            "name": "UNS",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    str_value: list[Str] = field(
        default_factory=list,
        metadata={
            "name": "STR",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    cstr: list[Cstr] = field(
        default_factory=list,
        metadata={
            "name": "CSTR",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    faultmemory: Optional[Faultmemory] = field(
        default=None,
        metadata={
            "name": "FAULTMEMORY",
            "type": "Element",
            "required": True,
        },
    )
    enum: list[EnumType] = field(
        default_factory=list,
        metadata={
            "name": "ENUM",
            "type": "Element",
            "min_occurs": 1,
            "sequence": 1,
        },
    )
    var: Optional[Var] = field(
        default=None,
        metadata={
            "name": "VAR",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Protocolservice:
    class Meta:
        name = "PROTOCOLSERVICE"

    id: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    func: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    phys: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    mresp: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    periodicresp: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    resp_on_phys: Optional[int] = field(
        default=None,
        metadata={
            "name": "respOnPhys",
            "type": "Attribute",
            "required": True,
        },
    )
    resp_on_func: Optional[int] = field(
        default=None,
        metadata={
            "name": "respOnFunc",
            "type": "Attribute",
            "required": True,
        },
    )
    sprmibonfunc: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    sprmibonphys: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    maycombcont: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    name: Optional[Name] = field(
        default=None,
        metadata={
            "name": "NAME",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
        },
    )
    qual: Optional[str] = field(
        default=None,
        metadata={
            "name": "QUAL",
            "type": "Element",
            "required": True,
        },
    )
    req: Optional[Req] = field(
        default=None,
        metadata={
            "name": "REQ",
            "type": "Element",
            "required": True,
        },
    )
    pos: Optional[Req] = field(
        default=None,
        metadata={
            "name": "POS",
            "type": "Element",
            "required": True,
        },
    )
    neg: Optional[Req] = field(
        default=None,
        metadata={
            "name": "NEG",
            "type": "Element",
        },
    )
    negrescodeproxies: Optional[Negrescodeproxies] = field(
        default=None,
        metadata={
            "name": "NEGRESCODEPROXIES",
            "type": "Element",
        },
    )


@dataclass
class Protocolservices:
    class Meta:
        name = "PROTOCOLSERVICES"

    protocolservice: list[Protocolservice] = field(
        default_factory=list,
        metadata={
            "name": "PROTOCOLSERVICE",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass
class Ecudoc:
    class Meta:
        name = "ECUDOC"

    oid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    temploid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    doctype: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    manufacturer: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    mid: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    saveno: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    languages: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    uptodate_languages: Optional[str] = field(
        default=None,
        metadata={
            "name": "uptodateLanguages",
            "type": "Attribute",
            "required": True,
        },
    )
    jobfileext: Optional[object] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    ftb_pool_path: Optional[str] = field(
        default=None,
        metadata={
            "name": "ftbPoolPath",
            "type": "Attribute",
            "required": True,
        },
    )
    xdtauth: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    dt_nesting: Optional[str] = field(
        default=None,
        metadata={
            "name": "dtNesting",
            "type": "Attribute",
            "required": True,
        },
    )
    extstorageitems: Optional[Extstorageitems] = field(
        default=None,
        metadata={
            "name": "EXTSTORAGEITEMS",
            "type": "Element",
            "required": True,
        },
    )
    desc: Optional[Desc] = field(
        default=None,
        metadata={
            "name": "DESC",
            "type": "Element",
            "required": True,
        },
    )
    protocolstandard: Optional[str] = field(
        default=None,
        metadata={
            "name": "PROTOCOLSTANDARD",
            "type": "Element",
            "required": True,
        },
    )
    specowner: Optional[str] = field(
        default=None,
        metadata={
            "name": "SPECOWNER",
            "type": "Element",
            "required": True,
        },
    )
    dtid: Optional[str] = field(
        default=None,
        metadata={
            "name": "DTID",
            "type": "Element",
            "required": True,
        },
    )
    qualgenoptions: Optional[Qualgenoptions] = field(
        default=None,
        metadata={
            "name": "QUALGENOPTIONS",
            "type": "Element",
            "required": True,
        },
    )
    attrcats: Optional[Attrcats] = field(
        default=None,
        metadata={
            "name": "ATTRCATS",
            "type": "Element",
            "required": True,
        },
    )
    defatts: Optional[Defatts] = field(
        default=None,
        metadata={
            "name": "DEFATTS",
            "type": "Element",
            "required": True,
        },
    )
    authors: Optional[Authors] = field(
        default=None,
        metadata={
            "name": "AUTHORS",
            "type": "Element",
            "required": True,
        },
    )
    histitems: Optional[Histitems] = field(
        default=None,
        metadata={
            "name": "HISTITEMS",
            "type": "Element",
            "required": True,
        },
    )
    targetgroups: Optional[Targetgroups] = field(
        default=None,
        metadata={
            "name": "TARGETGROUPS",
            "type": "Element",
            "required": True,
        },
    )
    negrescodes: Optional[Negrescodes] = field(
        default=None,
        metadata={
            "name": "NEGRESCODES",
            "type": "Element",
            "required": True,
        },
    )
    stategroups: Optional[Stategroups] = field(
        default=None,
        metadata={
            "name": "STATEGROUPS",
            "type": "Element",
            "required": True,
        },
    )
    vckmgr: Optional[Vckmgr] = field(
        default=None,
        metadata={
            "name": "VCKMGR",
            "type": "Element",
            "required": True,
        },
    )
    datatypes: Optional[Datatypes] = field(
        default=None,
        metadata={
            "name": "DATATYPES",
            "type": "Element",
            "required": True,
        },
    )
    doctmpl: Optional[Doctmpl] = field(
        default=None,
        metadata={
            "name": "DOCTMPL",
            "type": "Element",
            "required": True,
        },
    )
    recordtmpls: Optional[Recordtmpls] = field(
        default=None,
        metadata={
            "name": "RECORDTMPLS",
            "type": "Element",
            "required": True,
        },
    )
    dtcstatusmask: Optional[Dtcstatusmask] = field(
        default=None,
        metadata={
            "name": "DTCSTATUSMASK",
            "type": "Element",
            "required": True,
        },
    )
    unsuppsrvneg: Optional[Unsuppsrvneg] = field(
        default=None,
        metadata={
            "name": "UNSUPPSRVNEG",
            "type": "Element",
            "required": True,
        },
    )
    dids: Optional[Dids] = field(
        default=None,
        metadata={
            "name": "DIDS",
            "type": "Element",
            "required": True,
        },
    )
    protocolservices: Optional[Protocolservices] = field(
        default=None,
        metadata={
            "name": "PROTOCOLSERVICES",
            "type": "Element",
            "required": True,
        },
    )
    dcltmpls: Optional[Dcltmpls] = field(
        default=None,
        metadata={
            "name": "DCLTMPLS",
            "type": "Element",
            "required": True,
        },
    )
    recorddtpool: Optional[Recorddtpool] = field(
        default=None,
        metadata={
            "name": "RECORDDTPOOL",
            "type": "Element",
            "required": True,
        },
    )
    ecu: Optional[Ecu] = field(
        default=None,
        metadata={
            "name": "ECU",
            "type": "Element",
            "required": True,
        },
    )


@dataclass
class Candela:
    class Meta:
        name = "CANDELA"

    dtdvers: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    ecudoc: Optional[Ecudoc] = field(
        default=None,
        metadata={
            "name": "ECUDOC",
            "type": "Element",
            "required": True,
        },
    )
