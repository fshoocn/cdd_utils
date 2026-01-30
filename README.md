# CDD Diagnostic Data Parser

本项目是一个用于解析 Vector Candela (.cdd) 诊断描述文件的 Python 工具库。它将复杂的 CDD XML 结构解析为结构化的对象模型，支持多种诊断数据类型和复杂的逻辑映射。

---

## 核心功能

### 1. 支持的 CDD 数据类型

#### 组件类型 (Components)
*   **CONSTCOMP** - 常量组件：固定值的数据元素
*   **CONTENTCOMP** - 内容组件：基础数据单元
*   **SIMPLECOMPCONT** - 简单组件容器：线性排列的数据组合
*   **MUXCOMP** - 多路复用器组件：根据选择器字段动态选择分支
*   **MUXCOMPCONT** - 多路复用容器：多路复用器的数据分支容器
*   **NUMITERCOMP** - 数字迭代器：基于计数器的重复数据块
*   **EOSITERCOMP** - 流终止迭代器：基于终止条件的重复数据块
*   **STATICCOMP** - 静态组件：用于模板定义的占位符
*   **SIMPLEPROXYCOMP** - 简单代理组件：引用其他诊断实例的数据
*   **DOMAINDATAPROXYCOMP** - 域数据代理组件
*   **GROUPOFDTCPROXYCOMP** - DTC 组代理组件
*   **STATUSDTCPROXYCOMP** - DTC 状态代理组件
*   **DIDDATAREF** - DID 数据引用：引用其他 DID 的结构定义
*   **DIDREF** - DID 简单引用

#### 数据对象类型 (Data Objects)
*   **SPECDATAOBJ** - 规范数据对象：常用于 Service ID/Sub-function 等固定标识
*   **GAPDATAOBJ** - 间隙数据对象：填充字节或保留位
*   **RECORDDATAOBJ** - 记录数据对象：记录类型的数据
*   **GODTCDATAOBJ** - DTC 组数据对象

#### 数据类型 (Data Types)
*   **STRUCTURE** / **STRUCT** - 结构体：嵌套的数据元素组合
*   **STRUCTDT** - 结构体数据类型
*   **RECORDDT** - 记录数据类型
*   **MUXDT** - 多路复用数据类型
*   **LINCOMP** - 线性组件：带物理单位转换
*   **TEXTTBL** - 文本表：枚举值与描述的映射
*   **IDENT** - 标识符数据类型

---

## 解析架构

### 整体流程

```
CDD XML 文件 (Candela)
    ↓
XmlParser (xsdata)
    ↓
Candela 对象 (源数据模型)
    ↓
CddParser (核心解析器)
    ↓
EcuModel (目标对象模型)
```

### 核心组件

#### 1. 数据模型层 (`cdd/models/`)
*   **candela.py**: 原始 CDD XML 的数据类定义（由 xsdata 自动生成）
*   **cdd_model.py**: 解析后的目标数据模型，包含：
    *   `DiagnosticElement`: 所有诊断元素的基类
    *   `StructElement`, `MultiplexedElement`, `DidElement`, `TextTableElement` 等具体元素类型
    *   `DiagnosticMessage`: 请求/响应报文定义
    *   `DiagnosticService`: 诊断服务定义
    *   `DiagnosticInstance`: 诊断实例（服务集合）
    *   `DiagnosticGroup`: 诊断分组
    *   `EcuModel`: ECU 级别的完整诊断定义

#### 2. 解析器工厂 (`cdd/parsers/factory.py`)
*   自动发现并注册所有解析器
*   根据 XML 标签名动态路由到对应解析器
*   支持自定义解析器扩展

#### 3. 解析器实现 (`cdd/parsers/`)

##### 顶层解析器
*   **cdd_parser.py**: 主解析器，协调整体解析流程
*   **ecu_parser.py**: 解析 ECU 级别信息
*   **diag_parser.py**: 解析诊断实例和服务，处理复杂逻辑映射

##### 组件解析器 (`parsers/components/`)
每个解析器对应一种 CDD 组件类型，负责将 XML 元素转换为 `DiagnosticElement` 对象。

##### 数据类型解析器 (`parsers/datatypes/`)
解析 CDD 中的数据类型定义，如结构体、枚举、文本表等。

---


## 项目结构

```
Backend/
├── main.py                    # 测试入口（仅用于开发调试）
├── cdd/
│   ├── cdd_parser.py         # 核心解析器
│   ├── models/
│   │   ├── candela.py        # 源数据模型 (xsdata 生成)
│   │   └── cdd_model.py      # 目标数据模型
│   ├── parsers/
│   │   ├── factory.py        # 解析器工厂
│   │   ├── base_parser.py    # 解析器基类
│   │   ├── ecu_parser.py     # ECU 解析器
│   │   ├── diag_parser.py    # 诊断解析器（核心逻辑）
│   │   ├── components/       # 组件解析器
│   │   │   ├── constcomp_parser.py
│   │   │   ├── simplecompcont_parser.py
│   │   │   ├── muxcomp_parser.py
│   │   │   ├── diddataref_parser.py
│   │   │   └── ...
│   │   └── datatypes/        # 数据类型解析器
│   │       ├── structure_parser.py
│   │       ├── texttbl_parser.py
│   │       └── ...
│   └── utils/
│       ├── exceptions.py     # 异常定义
│       └── logging.py        # 日志工具
```

---

## 技术栈

*   **Python 3.10+**
*   **xsdata**: XML 解析和数据绑定
*   **pydantic**: 数据验证和序列化
*   **dataclasses**: 数据类支持

---

## 设计特点

1.  **工厂模式**: 自动发现和注册解析器，易于扩展
2.  **递归解析**: 支持任意深度的嵌套结构（Struct、Mux、Container）
3.  **延迟解析**: 模板和引用在需要时才解析，避免循环依赖
4.  **严格验证**: 使用 Pydantic 进行数据类型校验，确保解析结果的正确性
5.  **可序列化**: 所有数据模型支持 JSON 序列化，便于数据交换和存储

---

## 已实现功能清单

### ✅ 基础解析
- [x] CDD XML 文件加载 (通过 xsdata)
- [x] ECU 基本信息解析
- [x] 诊断分组 (DIAGGROUP) 解析
- [x] 诊断实例 (DIAGINST) 解析
- [x] 诊断模板 (DIAGTEMPL) 解析
- [x] 状态组 (STATEGROUP) 解析

### ✅ 组件解析
- [x] CONSTCOMP - 常量组件
- [x] CONTENTCOMP - 内容组件
- [x] SIMPLECOMPCONT - 简单容器
- [x] MUXCOMP / MUXCOMPCONT - 多路复用器
- [x] NUMITERCOMP - 数字迭代器
- [x] EOSITERCOMP - 流终止迭代器
- [x] STATICCOMP - 静态占位符
- [x] SIMPLEPROXYCOMP - 简单代理
- [x] DIDDATAREF / DIDREF - DID 引用

### ✅ 数据类型解析
- [x] STRUCTURE / STRUCT - 结构体
- [x] STRUCTDT - 结构体数据类型
- [x] RECORDDT - 记录数据类型
- [x] MUXDT - 多路复用数据类型
- [x] TEXTTBL - 文本表/枚举
- [x] LINCOMP - 线性转换

### ✅ 数据对象解析
- [x] SPECDATAOBJ - 规范数据对象
- [x] GAPDATAOBJ - 间隙对象
- [x] RECORDDATAOBJ - 记录对象
- [x] GODTCDATAOBJ - DTC 组对象

### ✅ 高级逻辑
- [x] 模板继承 (`tmplref`)
- [x] 静态值映射 (`SHSTATIC` / `STATICVALUE`)
- [x] 代理组件映射 (`SHPROXY` / `PROXYCOMP`)
- [x] 服务属性继承与覆盖 (`func`, `phys`, `respsupbit` 等)
- [x] 嵌套结构递归解析
- [x] 多层级元素展开

---

## 解析结果示例

以下是解析后的 JSON 数据结构示例（部分截取）：

```json
"positive_responses": {
    "name": {
    "tuv": [
        {
        "lang": "en-US",
        "uptodate": null,
        "struct": null,
        "para": [],
        "value": "STDS-PR"
        },
        {
        "lang": "zh-HANS",
        "uptodate": 0,
        "struct": null,
        "para": [],
        "value": ""
        }
    ]
    },
    "id": null,
    "description": null,
    "qualifier": "STDS_PR",
    "elements": [
    {
        "name": {
        "tuv": [
            {
            "lang": "en-US",
            "uptodate": null,
            "struct": null,
            "para": [],
            "value": "SID-PR"
            },
            {
            "lang": "zh-HANS",
            "uptodate": 0,
            "struct": null,
            "para": [],
            "value": ""
            }
        ]
        },
        "id": "_000002B09E3123B0",
        "description": null,
        "qualifier": "SID_PR",
        "spec": "sid",
        "must": 1,
        "constvalue": 80,
        "response_suppress_bit": null,
        "bit_length": 8,
        "display_format": "hex",
        "encoding": "uns",
        "byte_order": "21",
        "sig": null,
        "quantity": "atom",
        "minsz": 1,
        "maxsz": 1,
        "excl": [],
        "ref_id": null
    },
    {
        "name": {
        "tuv": [
            {
            "lang": "en-US",
            "uptodate": null,
            "struct": null,
            "para": [],
            "value": "Type"
            },
            {
            "lang": "zh-HANS",
            "uptodate": 0,
            "struct": null,
            "para": [],
            "value": ""
            }
        ]
        },
        "id": "_000002B09DEE7630",
        "description": null,
        "qualifier": "Subfunction_DiagnosticSessionControl",
        "spec": null,
        "must": 1,
        "constvalue": 1,
        "response_suppress_bit": 1,
        "bit_length": 8,
        "display_format": "text",
        "encoding": "uns",
        "byte_order": "21",
        "sig": 0,
        "quantity": "atom",
        "minsz": 1,
        "maxsz": 1,
        "excl": [],
        "ref_id": null,
        "textmap": [
        {
            "s": 1,
            "e": 1,
            "text": {
            "tuv": [
                {
                "lang": "en-US",
                "uptodate": null,
                "struct": null,
                "para": [],
                "value": "defaultSession"
                },
                {
                "lang": "zh-HANS",
                "uptodate": 0,
                "struct": null,
                "para": [],
                "value": ""
                }
            ]
            },
            "addinfo": null
        },
        {
            "s": 2,
            "e": 2,
            "text": {
            "tuv": [
                {
                "lang": "en-US",
                "uptodate": null,
                "struct": null,
                "para": [],
                "value": "programmingSession"
                },
                {
                "lang": "zh-HANS",
                "uptodate": 0,
                "struct": null,
                "para": [],
                "value": ""
                }
            ]
            },
            "addinfo": null
        },
        {
            "s": 3,
            "e": 3,
            "text": {
            "tuv": [
                {
                "lang": "en-US",
                "uptodate": null,
                "struct": null,
                "para": [],
                "value": "extendedDiagnosticSession"
                },
                {
                "lang": "zh-HANS",
                "uptodate": 0,
                "struct": null,
                "para": [],
                "value": ""
                }
            ]
            },
            "addinfo": null
        },
        {
            "s": 4,
            "e": 4,
            "text": {
            "tuv": [
                {
                "lang": "en-US",
                "uptodate": null,
                "struct": null,
                "para": [],
                "value": "safetySystemDiagnosticSession"
                },
                {
                "lang": "zh-HANS",
                "uptodate": 0,
                "struct": null,
                "para": [],
                "value": ""
                }
            ]
            },
            "addinfo": null
            }
        ]
    },
    {
        "name": {
        "tuv": [
            {
            "lang": "en-US",
            "uptodate": null,
            "struct": null,
            "para": [],
            "value": "SessionParameterRecord"
            },
            {
            "lang": "zh-HANS",
            "uptodate": 0,
            "struct": null,
            "para": [],
            "value": ""
            }
        ]
        },
        "id": "_000002B09E083350",
        "description": null,
        "qualifier": "SessionParameterRecord",
        "spec": "data",
        "must": 1,
        "constvalue": null,
        "response_suppress_bit": null,
        "bit_length": 0,
        "display_format": "hex",
        "encoding": "uns",
        "byte_order": "21",
        "sig": null,
        "quantity": "atom",
        "minsz": 1,
        "maxsz": 1,
        "excl": [],
        "ref_id": null,
        "min_num_of_items": 1,
        "max_num_of_items": 1,
        "struct": [
        {
            "name": {
            "tuv": [
                {
                "lang": "en-US",
                "uptodate": null,
                "struct": null,
                "para": [],
                "value": "P2"
                },
                {
                "lang": "zh-HANS",
                "uptodate": 0,
                "struct": null,
                "para": [],
                "value": ""
                }
            ]
            },
            "id": "13912585-ef4a-4759-9cd2-bb2743bd229a",
            "description": null,
            "qualifier": "P2",
            "spec": "no",
            "must": null,
            "constvalue": 50,
            "response_suppress_bit": null,
            "bit_length": 16,
            "display_format": "dec",
            "encoding": "uns",
            "byte_order": "21",
            "sig": 0,
            "quantity": "atom",
            "minsz": 1,
            "maxsz": 1,
            "excl": [],
            "ref_id": null
        },
        {
            "name": {
            "tuv": [
                {
                "lang": "en-US",
                "uptodate": null,
                "struct": null,
                "para": [],
                "value": "P2Ex"
                },
                {
                "lang": "zh-HANS",
                "uptodate": 0,
                "struct": null,
                "para": [],
                "value": ""
                }
            ]
            },
            "id": "41bf9c1c-459a-4a22-b0b1-e7bd18376094",
            "description": null,
            "qualifier": "P2Ex",
            "spec": "no",
            "must": null,
            "constvalue": 200,
            "response_suppress_bit": null,
            "bit_length": 16,
            "display_format": "dec",
            "encoding": "uns",
            "byte_order": "21",
            "sig": 0,
            "quantity": "atom",
            "minsz": 0,
            "maxsz": 255,
            "excl": [],
            "ref_id": null,
            "comp": {
            "s": null,
            "e": null,
            "f": 10,
            "div": null,
            "o": 0,
            "value": "\n"
            }
        }
        ]
    }
    ]
}
```

---

## JSON 字段说明

以下是生成的 JSON 数据模型中主要字段的含义说明：

| 字段名 | 类型 | 说明 | 示例/备注 |
| :--- | :--- | :--- | :--- |
| **基础属性** | | | |
| `id` | String | 元素的内部唯一标识符 (UUID) | `"41bf9c..."` |
| `qualifier` | String | 元素的限定名/别名，通常用于代码引用 | `"P2Ex"` |
| `name` | Object | 多语言名称对象 | 包含 `en-US`, `zh-HANS` 等 |
| `description` | String | 描述信息 | |
| **数据定义** | | | |
| `spec` | String | 数据的语义角色/规范 | `sid` (Service ID), `sub` (子功能), `no` (普通数据), `data` (数据块) |
| `must` | Integer | 必须性标识 | `1`=必须存在, `0`=可选 |
| `constvalue` | Integer | 固定值/常量值 | `200` (如果该字段是固定的常量) |
| `bit_length` | Integer | 数据位长度 | `8`, `16` 等 |
| `byte_order` | String | 字节序 | `"21"` (Big Endian/Motorola), `"12"` (Little Endian/Intel) |
| `encoding` | String | 物理编码格式 | `"uns"` (Unsigned), `"asc"` (ASCII), `"flt"` (Float) |
| `display_format` | String | 建议的显示格式 | `"hex"`, `"dec"`, `"text"` |
| `response_suppress_bit`| Integer | 是否支持抑制响应位 | `1`=支持 (通常用于 Sub-function byte 的 bit 7) |
| **数组/容器** | | | |
| `quantity` | String | 数量类型 | `"atom"` (单值), `"field"` (数组/域) |
| `minsz` | Integer | 最小元素个数/字节数 | 数组的最小长度 |
| `maxsz` | Integer | 最大元素个数/字节数 | 数组的最大长度 |
| `struct` | List | 子元素列表 | 当类型为结构体 (`STRUCTURE`/`RecordElement`) 时包含的子节点 |
| **物理值转换** | | | |
| `comp` | Object | 线性转换参数 (Linear Computation) | 用于 `LINCOMP` 类型，公式: `Phys = (Raw * f) / div + o` |
| &nbsp;&nbsp;`f` | Number | Factor (系数) | 乘数 |
| &nbsp;&nbsp;`div` | Number | Divisor (除数) | 默认 1 |
| &nbsp;&nbsp;`o` | Number | Offset (偏移量) | 加数 |
| `textmap` | List | 文本映射表 | 用于枚举类型，定义数值到文本的映射关系 |

---

## 扩展开发

### 添加新的解析器

1.  在 `parsers` 下创建新的解析器文件
2.  继承 `BaseParser` 类
3.  实现 `parse()` 方法
4.  工厂会自动发现并注册

**示例**：
```python
from cdd.parsers.base_parser import BaseParser
from cdd.models.cdd_model import DiagnosticElement

class MyCustomParser(BaseParser):
    """解析 MYCUSTOMCOMP"""
    
    def parse(self, element) -> DiagnosticElement:
        # 解析逻辑
        return DiagnosticElement(...)
```

---

## 许可证

本项目仅供学习和研究使用。
