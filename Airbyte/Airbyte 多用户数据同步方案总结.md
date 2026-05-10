# Airbyte 多用户数据同步方案总结

## 背景需求

开发一个 SaaS 应用，允许用户绑定第三方服务（Teams、Slack、Outlook、Calendar、Jira 等），
通过 OAuth 获取 Token，并借助 Airbyte 实现用户级别的数据同步。

---

## 一、核心架构概念

- **Source**：数据来源（如 Microsoft Teams）
- **Destination**：数据写入目标（如数据仓库）
- **Connection**：将 Source 和 Destination 连接的自动化数据管道
- **Connector**：Airbyte 用于连接和交互第三方服务的组件

---

## 二、多用户场景方案

### 推荐方案：Airbyte AI Agents API

每个用户绑定一个服务时，创建一个独立的 **Connector**（存储该用户的凭证），
通过 `connector_id` 区分不同用户，按需执行数据操作。

- 每个用户 × 每个服务 = 一个 Connector
- 无需为每个用户创建传统意义上的 Connection
- 更轻量，适合多用户 SaaS 场景

---

## 三、Microsoft Teams 连接器的限制

- 当前官方 Teams 连接器**仅支持 Full Refresh Sync，不支持 Incremental Sync**
- 部分 API（如 channel messages）在 Graph API v1.0 中不被支持
- 如需增量同步，需要开发**自定义连接器**

---

## 四、自定义连接器开发

### 工具选择

| 工具 | 适用场景 | 语言 |
|------|----------|------|
| Connector Builder | 大多数 REST API，推荐首选 | 无需编码（YAML 配置） |
| Low-Code CDK | 需要更多灵活性的 HTTP API | YAML（可选 Python） |
| Python CDK | 最复杂场景，完全自定义 | Python |

### 使用 Connector Builder 实现增量同步

1. 进入 Airbyte UI → **Builder** → **Import a YAML**
2. 导入现有 Teams 连接器的 `manifest.yaml` 作为起点
3. 在 **Inputs** 页面添加用户凭证字段（`tenant_id`、`client_id`、`client_secret`、`start_date`）
4. 为目标 Stream 开启 **Incremental Sync**，配置：
   - **Cursor Field**：如 `lastModifiedDateTime`
   - **Cursor Datetime Formats**：如 `%Y-%m-%dT%H:%M:%SZ`
   - **Start Datetime**：引用用户输入 `{{ config['start_date'] }}`
   - **Inject start/end time** 到 API 请求参数
5. 测试并发布到 Workspace

> ⚠️ 增量同步前提：Microsoft Graph API 需支持按时间戳过滤记录。

---

## 五、迁移（开发环境 → 生产环境）

- **自定义连接器**：导出 YAML manifest，在生产环境通过 Import YAML 重新导入
- **整体配置迁移**：两个实例版本需相同，可通过 UI export/import 或 API 逐个重建
- 注意：通过 API 迁移会丢失增量同步的 state，需重新全量同步

---

## 六、整体工作流程

### Sequence Diagram

```mermaid
用户（浏览器）          您的后端应用          Microsoft Teams (OAuth)          Airbyte API          您的数据库
     |                      |                          |                           |                    |
     |-- 点击"绑定 Teams" -->|                          |                           |                    |
     |                      |-- 重定向到 OAuth 授权页 -->|                           |                    |
     |-- 用户授权同意 ------->|                          |                           |                    |
     |                      |<-- 回调，携带 auth_code --|                           |                    |
     |                      |-- 用 code 换取 token ---->|                           |                    |
     |                      |<-- 返回 access/refresh token                          |                    |
     |                      |-- POST /integrations/connectors（携带用户 token）----->|                    |
     |                      |<-- 返回 connector_id ------------------------------ --|                    |
     |                      |-- 存储 user_id → connector_id ------------------------------------------>|
     |                      |                          |                           |                    |
     |-- 请求查看 Teams 数据->|                          |                           |                    |
     |                      |-- 查询 connector_id ----------------------------------------------------->|
     |                      |<-- 返回 connector_id -----------------------------------------------------|
     |                      |-- POST /connectors/{connector_id}/execute ----------->|                    |
     |                      |                          |<-- 调用 Graph API ---------|                    |
     |                      |                          |-- 返回数据 -------------->|                    |
     |                      |<-- 返回数据结果 ---------------------------------------|                    |
     |<-- 展示数据 ----------|                          |                           |                    |
```

---

## 七、Python 伪代码

### 安装 SDK

```bash
uv add airbyte-agent-sdk
# 或
uv pip install airbyte-agent-sdk
```

### 步骤 1：获取 Application Token

```python
import requests

response = requests.post(
    "https://api.airbyte.ai/api/v1/account/applications/token",
    json={
        "client_id": "<your_airbyte_client_id>",
        "client_secret": "<your_airbyte_client_secret>"
    }
)
application_token = response.json()["access_token"]
```

### 步骤 2：用户绑定 Teams 时，创建 Connector

```python
def create_teams_connector_for_user(user_id: str, teams_access_token: str, teams_client_id: str, teams_client_secret: str):
    response = requests.post(
        "https://api.airbyte.ai/api/v1/integrations/connectors",
        headers={
            "Authorization": f"Bearer {application_token}",
            "Content-Type": "application/json"
        },
        json={
            "workspace_name": "default",
            "connector_type": "microsoft-teams",  # 替换为实际 definition_id
            "name": f"User_{user_id}_Teams",
            "credentials": {
                "access_token": teams_access_token,
                "client_id": teams_client_id,
                "client_secret": teams_client_secret
            }
        }
    )
    connector_id = response.json()["connector_id"]
    db.save(user_id=user_id, service="teams", connector_id=connector_id)
    return connector_id
```

### 步骤 3：按需读取用户的 Teams 数据

```python
def get_teams_data_for_user(user_id: str, entity: str = "teams", action: str = "list"):
    connector_id = db.get_connector_id(user_id=user_id, service="teams")
    
    response = requests.post(
        f"https://api.airbyte.ai/api/v1/integrations/connectors/{connector_id}/execute",
        headers={
            "Authorization": f"Bearer {application_token}",
            "Content-Type": "application/json"
        },
        json={
            "entity": entity,
            "action": action,
            "params": {"per_page": 50}
        }
    )
    return response.json()

# 使用示例
data = get_teams_data_for_user(user_id="user_123")
```

---

## 八、关键注意事项

1. **Teams 连接器不支持增量同步**，如需增量同步需自定义连接器
2. **自定义连接器与原有连接器可共存**，但写入同一目标表会有数据重复风险，建议写入不同表或完全替代
3. **迁移时**，自定义连接器可通过 YAML 文件迁移，但用户凭证和 Connection 状态需额外处理
4. **每个用户对应一个 Connector**，通过 `connector_id` 区分，Airbyte 负责管理凭证和 API 通信

---

## 参考文档

- [Microsoft Teams Source Connector](https://docs.airbyte.com/integrations/sources/microsoft-teams)
- [Connector Builder Overview](https://docs.airbyte.com/platform/connector-development/connector-builder-ui/overview)
- [Incremental Sync](https://docs.airbyte.com/platform/connector-development/connector-builder-ui/incremental-sync)
- [AI Agents SDK](https://docs.airbyte.com/ai-agents/interfaces/sdk)
- [Execute Operations (API)](https://docs.airbyte.com/ai-agents/interfaces/api/execute)
- [Microsoft Teams Migration Guide](https://docs.airbyte.com/integrations/sources/microsoft-teams-migrations)
