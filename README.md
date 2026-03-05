# CDD Diagnostic Data Parser V2

用于解析 Vector Candela `*.cdd` 诊断描述文件的 Python 工具库。将 CDD XML 结构转换为分层、不可变（`frozen dataclass`）的对象模型，支持编码、解码和按名称查询。

---

## 目录

- [快速开始](#快速开始)
- [公共 API](#公共-api)
- [架构总览](#架构总览)
- [数据模型层](#数据模型层-cddmodels)
- [转换器层](#转换器层-cddtransformers)
- [编解码引擎](#编解码引擎-cddcodec)
- [工具模块](#工具模块-cddutils)
- [CDD 数据类型对照表](#cdd-数据类型对照表)
- [目录结构](#目录结构)
- [示例脚本](#示例脚本)
- [设计特点](#设计特点)
- [常见问题](#常见问题)

---

## 快速开始

### 安装依赖

```bash
pip install xsdata
```

### 加载并查询

```python
from Backend.cdd import load_cdd

db = load_cdd("Backend/testfile/1.cdd", strict=False)

# 基本信息
print(db)                       # <CddDatabase ecu='ECU_NAME' services=42 frozen=True>
print(db.ecu)                   # EcuModel
print(len(db.services))         # 服务总数
print(db.warnings)              # 非严格模式下的警告列表

# 按名称查找服务
svc = db.find_service("ReadDataByIdentifier")
svc = db.services.ReadDataByIdentifier   # 等价的属性访问
svc = db.services.by_name("ReadDataByIdentifier")

# 模糊搜索
results = db.search_services("DTC")

# 编码请求报文
req_bytes = svc.request.encode_default()
print(req_bytes.hex(" "))

# 解码正响应
decoded = svc.positive_responses.decode_values(b'\x62\xF1\x90...')
print(decoded)   # {'SID_PR': 98, 'DID': 61840, ...}
```

---

## 公共 API

通过 `cdd/__init__.py` 导出，版本 `2.0.0`：

| 符号 | 类型 | 说明 |
|------|------|------|
| `load_cdd(path, *, strict=True)` | 函数 | 加载 CDD 文件，返回 `CddDatabase` |
| `load_cdd_from_candela(candela, *, strict=True)` | 函数 | 从已有 `Candela` 对象构建数据库 |
| `CddDatabase` | 类 | 顶层只读容器（详见下文） |
| `CddRef[T]` | 泛型类 | 有类型的延迟引用（Phase 2→3 自动解析） |
| `ObjectRegistry` | 类 | ID → 对象 的全局注册表 |
| `NamedItemList[T]` | 泛型列表 | 支持 `list[idx]`、`list.qualifier`、`list.by_name()`、`list.search()` |
| `DuplicateIdError` | 异常 | 注册时 ID 重复 |
| `IdNotFoundError` | 异常 | 引用解析时 ID 找不到 |

### CddDatabase 属性与方法

```python
db.model             # CddModel (dtdvers, ecu, state_groups)
db.ecu               # EcuModel
db.services          # NamedItemList[DiagnosticService]
db.warnings          # list[str]
db.is_frozen         # bool
db.find_service(q)   # 精确查找
db.search_services(k)# 模糊搜索
db.refresh()         # 重新执行 4 阶段构建
```

### strict 模式

| 模式 | 行为 |
|------|------|
| `strict=True`（默认） | 遇到错误立即抛异常 |
| `strict=False` | 尽量继续解析，错误写入 `db.warnings` |

---

## 架构总览

### 5 阶段生命周期

```
CDD XML 文件
    │  Phase 0: xsdata.XmlParser
    ▼
Candela 对象 (xsdata 生成的数据类)
    │  Phase 1: CddDatabase._build_registry()
    │           递归扫描对象图，注册所有 id/oid → ObjectRegistry
    ▼
ObjectRegistry (raw_objects)
    │  Phase 2: CddDatabase._transform()
    │           TransformerRegistry 按类型匹配转换器
    │           深度优先递归转换 + 幂等 + 循环检测 + 自动注册
    ▼
ObjectRegistry (model_objects)
    │  Phase 3: CddDatabase._resolve_refs()
    │           遍历所有 CddRef[T]，替换为真实模型对象
    ▼
ObjectRegistry (refs resolved)
    │  Phase 4: CddDatabase._freeze()
    │           构建 CddModel / NamedItemList[DiagnosticService]
    ▼
CddDatabase (frozen, read-only)
```

### 核心类协作关系

| 类 | 文件 | 职责 |
|----|------|------|
| `CddDatabase` | `database.py` | 顶层容器，驱动 4 阶段构建，提供公共 API |
| `ObjectRegistry` | `registry.py` | 管理 raw/model 两份 ID→对象映射 + CddRef 追踪 |
| `CddRef[T]` | `refs.py` | Phase 2 创建的延迟引用，Phase 3 自动解析后透明代理 |
| `TransformerRegistry` | `transformer_registry.py` | 单例，自动发现转换器，按 `handles_type` 索引，核心入口 `transform_one()` |
| `BaseTransformer` | `transformers/base.py` | 转换器抽象基类，提供 `_resolve_children()` / `_resolve_one()` 递归辅助 |
| `NamedItemList[T]` | `named_list.py` | list 子类，支持按 qualifier 属性访问 / 精确查找 / 模糊搜索 |

---

## 数据模型层 (`cdd/models/`)

所有模型类均为 `frozen=True` 的 `dataclass`，构建后不可修改，天然线程安全。

### 类型继承关系

```
IdentifiableElement          (id, name, desc, qualifier, spec, must)
├── CodedElement             (+constvalue, bit_length, encoding, byte_order, quantity, minsz, maxsz, …)
│   ├── ConstElement         常量 — SID、SubFunction 等固定值
│   ├── TextTableElement     文本映射 — 值↔文本 映射表 (textmap)
│   ├── LinCompElement       线性转换 — 物理值 = raw × f + o (comp)
│   └── PlaceholderElement   占位 — 保留位/填充位
├── StructElement            结构体 — 有序子元素 (children)  [容器]
│   └── RecordElement        记录 — 带 record_number
├── MultiplexedElement       多路复用 — 按 selector 分支 (cases) [容器]
├── NumIterElement           数字迭代器 — count × body (children) [容器]
└── DidElement               DID 引用 — (did, children) [容器]
```

> 容器类型继承 `IdentifiableElement` 而非 `CodedElement`，因为容器本身没有 bit_length、encoding 等编码属性。

### 消息与服务

| 类 | 文件 | 说明 |
|----|------|------|
| `DiagnosticMessage` | `messages.py` | 请求/正响应/负响应报文，包含 `elements` 元组。提供 `encode_default()` 和 `decode_values(data)` |
| `DiagnosticService` | `messages.py` | 单个诊断服务。字段：`service_name`, `protocol_svc_name`, `qualifier`, `is_used`, `func/phys`, `request`, `positive_responses`, `negative_responses` 等 |
| `DiagnosticInstance` | `ecu.py` | 诊断实例 — 包含一组 `DiagnosticService` |
| `DiagnosticGroup` | `ecu.py` | 诊断组 — 包含一组 `DiagnosticInstance` |
| `EcuModel` | `ecu.py` | ECU 模型 — 包含 `diag_list` |
| `StateGroup` | `ecu.py` | 状态组 |
| `CddModel` | `database_model.py` | 顶层聚合：`dtdvers`, `ecu`, `state_groups` |
| `MuxCase` | `containers.py` | 多路复用分支 (s, e, structure) |
| `candela.py` | `models/candela.py` | xsdata 自动生成的 XML 绑定类（Candela 原始模型） |

### 枚举类型（`base.py`）

| 枚举 | 值 |
|------|----|
| `ByteOrder` | `BIG_ENDIAN("21")`, `LITTLE_ENDIAN("12")` |
| `DisplayFormat` | `HEX`, `DECIMAL`, `TEXT`, `BINARY`, `FLOAT` |
| `Encoding` | `UNSIGNED`, `SIGNED`, `ASCII`, `UTF8`, `BCD`, `FLOAT`, `DOUBLE` |
| `Quantity` | `ATOM`, `FIELD` |

---

## 转换器层 (`cdd/transformers/`)

每个转换器继承 `BaseTransformer`，实现 `match()` + `transform()`。
`TransformerRegistry`（单例）在首次实例化时自动扫描 `transformers/` 包，按 `handles_type` 建立 O(1) 类型索引，按 `priority` 排序。

### 转换器一览

#### 顶层转换器

| 转换器 | 优先级 | 源类型 | 目标类型 | 说明 |
|--------|--------|--------|----------|------|
| `DiagTransformer` | 91 | `Diagclass` / `Diaginst` | `DiagnosticGroup` / `DiagnosticInstance` | 解析模板继承 (tmplref)、SHSTATIC 静态映射、SHPROXY 代理映射、Service 属性覆盖 |
| `EcuTransformer` | 90 | `Ecu` | `EcuModel` | ECU 顶层，递归转换 DiagClass 子对象 |
| `ProtocolserviceTransformer` | 90 | `Protocolservice` | `DiagnosticService` | 请求/正响应/负响应消息转换 + NRC 注入 |

#### 元素转换器 (`transformers/elements/`)

| 转换器 | 优先级 | 源类型 → 目标类型 |
|--------|--------|-------------------|
| `DataobjTransformer` | 60 | `Dataobj` → 引用 dtref 后用自身属性覆盖 |
| `SpecdataobjTransformer` | 55 | `Specdataobj` → `TextTableElement` (NRC 列表) |
| `RecorddataobjTransformer` | 55 | `Recorddataobj` → `TextTableElement` (内联 Recorddt) |
| `GodtcdataobjTransformer` | 55 | `Godtcdataobj` → `TextTableElement` (内联 Texttbl) |
| `DiddatarefTransformer` | 55 | `Diddataref` / `Didref` → `DidElement` |
| `SimplecompcontTransformer` | 55 | `Simplecompcont` → `StructElement` 或单元素 |
| `ConstcompTransformer` | 50 | `Constcomp` → `ConstElement` |
| `ContentcompTransformer` | 50 | `Contentcomp` → `StructElement` |
| `MuxcompTransformer` | 50 | `Muxcomp` → `MultiplexedElement` (引用 Muxdt) |
| `MuxcompcontTransformer` | 50 | `Muxcompcont` → 透明容器，委托 Muxdt/Dataobj |
| `NumitercompTransformer` | 50 | `Numitercomp` → `NumIterElement` |
| `EositercompTransformer` | 50 | `Eositercomp` → `StructElement` (可变重复) |
| `StaticcompTransformer` | 50 | `Staticcomp` → 引用 dtref 后覆盖属性 |
| `SimpleproxycompTransformer` | 50 | `Simpleproxycomp` → `CodedElement` (占位代理) |
| `DomaindataproxycompTransformer` | 50 | `Domaindataproxycomp` → 按 dest 分发到 TextTable/Struct/Coded |
| `GroupofdtcproxycompTransformer` | 50 | `Groupofdtcproxycomp` → `CodedElement` (引用 dtref) |
| `StatusdtcproxycompTransformer` | 50 | `Statusdtcproxycomp` → `CodedElement` |
| `GapdataobjTransformer` | 50 | `Gapdataobj` → `PlaceholderElement` |

#### 数据类型转换器 (`transformers/datatypes/`)

| 转换器 | 优先级 | 源类型 → 目标类型 |
|--------|--------|-------------------|
| `TexttblTransformer` | 50 | `Texttbl` → `TextTableElement` |
| `LincompTransformer` | 50 | `Lincomp` → `LinCompElement` |
| `IdentTransformer` | 50 | `Ident` → `CodedElement` |
| `StructureTransformer` | 50 | `Structure` / `Struct` → `StructElement` |
| `StructdtTransformer` | 50 | `Structdt` → `StructElement` (内联 Struct/Dataobj) |
| `MuxdtTransformer` | 50 | `Muxdt` → `MultiplexedElement` (选择器 + CASE 分支) |
| `RecorddtTransformer` | 50 | `Recorddt` → `TextTableElement` (Record + Recordref) |

### transform_one() 核心流程

```
transform_one(raw_obj)
  ① 幂等检查 → 已有 model 则直接返回
  ② 循环检测 → _transforming set 防止 A→B→A
  ③ 查找转换器 → handles_type 索引 O(1) + fallback 线性扫描
  ④ 标记进入 → 调用 transformer.transform()
  ⑤ 自动注册 → registry.register_transformed(id, model)
  ⑥ 返回 model
```

---

## 编解码引擎 (`cdd/codec/`)

| 类/函数 | 文件 | 说明 |
|---------|------|------|
| `EncodeState` | `encode_state.py` | 编码状态机：`bytearray` 缓冲 + bit 级游标。`write_bits(value, bit_length, byte_order)` 支持大端/小端 |
| `DecodeState` | `decode_state.py` | 解码状态机：源 `bytes` + bit 级游标。`read_bits(bit_length, byte_order)` 支持大端/小端 |
| `parse_textmap_s(s)` | `codec_utils.py` | 解析 `'(31,0,0)'` 元组字符串为大端整数 `0x1F0000` |
| `format_textmap_s(s)` | `codec_utils.py` | 格式化为十六进制显示 |
| `bcd_encode/bcd_decode` | `codec_utils.py` | BCD 编解码 |
| `twos_complement` | `codec_utils.py` | 二进制补码 |
| `sign_extend` | `codec_utils.py` | 符号扩展 |

编解码由 `DiagnosticMessage` 驱动：
- `encode_default()`：递归遍历 elements，按 `constvalue > textmap首项 > comp.s > 0` 填充默认值
- `decode_values(data)`：递归遍历 elements，根据 bit_length/byte_order 从字节流读取值返回 dict

---

## 工具模块 (`cdd/utils/`)

### 异常层级

```
CddParseError
├── TransformError     (transformer_name, obj_id, original_error)
└── CodecError
    ├── EncodeError
    └── DecodeError
```

### 辅助函数

| 函数 | 说明 |
|------|------|
| `default_name(en, zh)` | 快速创建 `Name(tuv=[Tuv(...)])` |

### 兼容模块 (`compat.py`)

从 `models/candela.py` 集中导出所有 Candela 原始类型（约 40+ 类），供转换器通过 `from ..compat import Xxx` 引用，不依赖 V1。

---

## CDD 数据类型对照表

### 组件类型 (CDD → 模型)

| CDD 标签 | 模型类型 | 说明 |
|----------|----------|------|
| `CONSTCOMP` | `ConstElement` | 常量 (SID/Sub 等固定值) |
| `CONTENTCOMP` | `StructElement` | 内容组件（内含 SIMPLECOMPCONT） |
| `SIMPLECOMPCONT` | `StructElement` / 单元素 | 简单容器 |
| `MUXCOMP` | `MultiplexedElement` | 多路复用 (引用 MUXDT) |
| `MUXCOMPCONT` | 透明委托 | 多路复用容器 |
| `NUMITERCOMP` | `NumIterElement` | 数字迭代器 |
| `EOSITERCOMP` | `StructElement` | 流终止迭代器 (可变重复) |
| `STATICCOMP` | `TextTableElement` | 静态占位 (引用 dtref) |
| `SIMPLEPROXYCOMP` | `CodedElement` | 代理占位 |
| `DOMAINDATAPROXYCOMP` | `TextTableElement` / `StructElement` / `CodedElement` | 域数据代理 (按 dest 分发) |
| `GROUPOFDTCPROXYCOMP` | `CodedElement` | DTC 组代理 |
| `STATUSDTCPROXYCOMP` | `CodedElement` | DTC 状态代理 |
| `DIDDATAREF` / `DIDREF` | `DidElement` | DID 引用 |

### 数据对象类型

| CDD 标签 | 模型类型 | 说明 |
|----------|----------|------|
| `DATAOBJ` | 引用 dtref 的目标类型 | 数据对象 (解引用 + 属性覆盖) |
| `SPECDATAOBJ` | `TextTableElement` | 特殊数据对象 (NRC 列表) |
| `GAPDATAOBJ` | `PlaceholderElement` | 间隙/填充 |
| `RECORDDATAOBJ` | `TextTableElement` | 记录数据对象 (内联 RECORDDT) |
| `GODTCDATAOBJ` | `TextTableElement` | DTC 组数据对象 (内联 TEXTTBL) |

### 数据类型

| CDD 标签 | 模型类型 | 说明 |
|----------|----------|------|
| `TEXTTBL` | `TextTableElement` | 文本表/枚举 (textmap) |
| `LINCOMP` | `LinCompElement` | 线性转换 (comp: f, o, s, e) |
| `IDENT` | `CodedElement` | 标识符 |
| `STRUCTURE` / `STRUCT` | `StructElement` | 结构体 |
| `STRUCTDT` | `StructElement` | 结构体数据类型 |
| `MUXDT` | `MultiplexedElement` | 多路复用数据类型 (CASE 分支) |
| `RECORDDT` | `TextTableElement` | 记录数据类型 (Record + Recordref) |

### 高级逻辑

| 机制 | 处理位置 | 说明 |
|------|----------|------|
| 模板继承 (`tmplref`) | `DiagTransformer` | DiagInst 引用 Dcltmpl 中的 Dclsrvtmpl |
| 静态映射 (`SHSTATIC` / `STATICVALUE`) | `DiagTransformer._apply_shstatic_mapping()` | 将常量值注入到模板中的 STATICCOMP |
| 代理映射 (`SHPROXY` / `PROXYCOMP`) | `DiagTransformer._apply_shproxy_mapping()` | 将实例数据替换到模板中的 SIMPLEPROXYCOMP |
| 服务属性覆盖 | `DiagTransformer._transform_diaginst()` | `is_used`, `func`, `phys`, `qualifier`, `service_name` 等从 SERVICE 节点覆盖 |
| NRC 注入 | `ProtocolserviceTransformer._inject_nrc_textmap()` | 将 NEGRESCODEPROXIES 注入到 NEG.resCode 元素 |
| FAULTMEMORY 关联 | `DomaindataproxycompTransformer` | 域代理 edrn/ed/srn/sd 自动关联 ECU FAULTMEMORY 数据 |

---

## 目录结构

```text
Backend/
├── cdd/
│   ├── __init__.py              # 公共 API 导出 (v2.0.0)
│   ├── loadfile.py              # load_cdd() / load_cdd_from_candela()
│   ├── database.py              # CddDatabase — 4 阶段生命周期
│   ├── registry.py              # ObjectRegistry — ID 注册表 + CddRef 追踪
│   ├── refs.py                  # CddRef[T] — 延迟引用 (代理模式)
│   ├── named_list.py            # NamedItemList — 按名属性访问的列表
│   ├── compat.py                # 兼容层 — 集中导出 Candela 原始类型
│   ├── codec/
│   │   ├── __init__.py
│   │   ├── encode_state.py      # EncodeState — bit 级编码状态机
│   │   ├── decode_state.py      # DecodeState — bit 级解码状态机
│   │   └── codec_utils.py       # BCD/补码/textmap 解析等工具
│   ├── models/
│   │   ├── __init__.py          # 统一导出所有模型类
│   │   ├── base.py              # IdentifiableElement / CodedElement / 枚举
│   │   ├── elements.py          # ConstElement / TextTableElement / LinCompElement / PlaceholderElement
│   │   ├── containers.py        # StructElement / MultiplexedElement / NumIterElement / DidElement / MuxCase
│   │   ├── messages.py          # DiagnosticMessage / DiagnosticService (编解码逻辑)
│   │   ├── ecu.py               # EcuModel / DiagnosticGroup / DiagnosticInstance / StateGroup
│   │   ├── database_model.py    # CddModel — 顶层聚合
│   │   └── candela.py           # xsdata 生成的 XML 绑定类
│   ├── transformers/
│   │   ├── __init__.py
│   │   ├── base.py              # BaseTransformer (ABC + 递归辅助)
│   │   ├── transformer_registry.py  # TransformerRegistry (单例, 自动发现)
│   │   ├── ecu_transformer.py       # Ecu → EcuModel
│   │   ├── diag_transformer.py      # Diagclass/Diaginst → Group/Instance + 模板/映射逻辑
│   │   ├── protocolservice_transformer.py  # Protocolservice → DiagnosticService + NRC 注入
│   │   ├── elements/            # 18 个元素转换器
│   │   │   ├── const.py         # Constcomp → ConstElement
│   │   │   ├── contentcomp.py   # Contentcomp → StructElement
│   │   │   ├── dataobj.py       # Dataobj → 解引用 dtref
│   │   │   ├── diddataref.py    # Diddataref/Didref → DidElement
│   │   │   ├── domaindataproxycomp.py  # 域数据代理 (FAULTMEMORY 关联)
│   │   │   ├── eositercomp.py   # Eositercomp → StructElement
│   │   │   ├── gapdataobj.py    # Gapdataobj → PlaceholderElement
│   │   │   ├── godtcdataobj.py  # Godtcdataobj → TextTableElement
│   │   │   ├── groupofdtcproxycomp.py  # DTC 组代理
│   │   │   ├── muxcomp.py       # Muxcomp → MultiplexedElement
│   │   │   ├── muxcompcont.py   # Muxcompcont → 透明委托
│   │   │   ├── numitercomp.py   # Numitercomp → NumIterElement
│   │   │   ├── recorddataobj.py # Recorddataobj → TextTableElement
│   │   │   ├── simplecompcont.py# Simplecompcont → StructElement
│   │   │   ├── simpleproxycomp.py  # 简单代理
│   │   │   ├── specdataobj.py   # Specdataobj → TextTableElement (NRC)
│   │   │   ├── staticcomp.py    # Staticcomp → 引用 dtref
│   │   │   └── statusdtcproxycomp.py  # DTC 状态代理
│   │   └── datatypes/           # 7 个数据类型转换器
│   │       ├── ident.py         # Ident → CodedElement
│   │       ├── lincomp.py       # Lincomp → LinCompElement
│   │       ├── muxdt.py         # Muxdt → MultiplexedElement
│   │       ├── recorddt.py      # Recorddt → TextTableElement
│   │       ├── structdt.py      # Structdt → StructElement
│   │       ├── structure.py     # Structure/Struct → StructElement
│   │       └── texttbl.py       # Texttbl → TextTableElement
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py        # CddParseError / TransformError / CodecError / EncodeError / DecodeError
│       └── helpers.py           # default_name()
├── example.py                   # 快速加载并编码
├── example_services.py          # 打印所有服务 + 参数 + 默认 Hex
├── example_decode.py            # 报文解码示例
├── test.py                      # 命令行测试入口
└── testfile/                    # 测试用 CDD 文件
```

---

## 示例脚本

### example.py — 快速加载并编码

```bash
cd Backend && python example.py
```

### example_services.py — 遍历所有服务

```bash
python Backend/example_services.py
python Backend/example_services.py Backend/testfile/XIAOPENG_CMS019-A1.cdd
```

输出包含每个服务的请求/正响应/负响应元素结构、类型、编码属性、默认值及 Hex 编码。

### example_decode.py — 报文解码

```bash
python Backend/example_decode.py Backend/testfile/1.cdd ReadAllIdentified request
python Backend/example_decode.py Backend/testfile/1.cdd ReadAllIdentified positive "59 02 00 00 00 00 00"
```

### test.py — 命令行解析工具

```bash
python Backend/test.py Backend/testfile/1.cdd
python Backend/test.py Backend/testfile/1.cdd --strict
```

---

## 设计特点

1. **不可变模型** — 所有 model dataclass 均 `frozen=True`，构建后只读，天然线程安全
2. **转换器自动发现** — `TransformerRegistry` 单例启动时递归扫描 `transformers/` 包，新增转换器只需创建文件
3. **深度优先递归转换** — `transform_one()` 保证幂等 + 防环 + 自动注册，不需要手动排序依赖
4. **类型安全延迟引用** — `CddRef[T]` 在 Phase 2 创建、Phase 3 批量解析，解析后透明代理属性访问
5. **O(1) 类型匹配** — 按 `handles_type` 建立索引，快速找到对应转换器
6. **bit 级编解码** — `EncodeState` / `DecodeState` 支持任意位长度、大端/小端
7. **按名查询** — `NamedItemList` 支持 `db.services.ReadDTCInformation` 属性访问 + IDE 补全
8. **pickle 支持** — `CddDatabase` 实现 `__getstate__` / `__setstate__`，可序列化缓存

---

## 常见问题

**Q: `CDD 文件不存在`**
检查路径是否正确。建议使用绝对路径或从项目根目录运行。

**Q: `db.services.SomeName` 报 AttributeError**
某些 qualifier 含特殊字符（如空格、连字符），属性访问时会自动转为 `_`。可用 `db.services.by_name("Some-Name")` 或 `db.find_service("Some-Name")` 精确匹配。

**Q: 警告/错误很多怎么办？**
先用 `strict=False` 加载，检查 `db.warnings` 列表定位具体对象 ID。

**Q: 如何新增一种 CDD 组件的支持？**
在 `transformers/elements/` 或 `transformers/datatypes/` 下新建文件，创建 `BaseTransformer` 子类并设置 `handles_type`。`TransformerRegistry` 会自动发现。

---

## 技术栈

- **Python 3.10+**
- **xsdata** — XML 解析和数据绑定
- **dataclasses** (`frozen=True`) — 不可变数据模型

## 版本

当前代码版本：`2.0.0`（`cdd/__init__.py`）
