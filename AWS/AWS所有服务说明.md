---
title: AWS所有服务说明
url: https://www.yuque.com/stevenyin/liv/brdqb9
---

<a name="43562ab1"></a>

## Compute 计算

- EC2：虚拟私有服务器
- Lightsail：亚马逊提供的托管服务商(VPS、DNS、存储)
- Lambda：可以运行用Python，Node.js，Go等语言编写的代码，还可以并行运行。
- Batch：在EC2机器的Docker容器中运行软件指令
- Elastic Beanstalk：在托管的虚拟机上运行软件
- Serverless Application Repository：(在Lambda)可部署的无服务器应用程序的存储库
- AWS Outposts：可以在您的数据中心使用亚马逊服务
- EC2 Image Builder：自动创建EC2图像

<a name="88c1d422"></a>

## Storage 存储

- S3：不能直接挂载，但可以通过HTTP下载的文件存储
- EFS：可以将网络上的磁盘挂载到您的机器上使用的网络文件系统
- FSx：可以从EC2机器连接的Windows或Lustre的文件系统
- S3 Glacier：用于备份和归档的低成本存储系统
- Storage Gateway：可以把S3连接到自有（或远程控制）的机器上使用的iSCSI
- AWS Backup：自动备份不同AWS服务(如EC2和RDS)

<a name="c6091076"></a>

## Database 数据库

- RDS：托管的MySQL，PostgreSQL数据库
- DynamoDB：大规模可扩展的非关系数据库
- ElastiCache：托管的分布式的memcache高速缓存系统和redis高性能Key-Value数据库
- Neptune：图表数据库
- Amazon Redshift：用来大量存储流计算可处理数据的数据仓
- Amazon QLDB：可供选择的用于加密验证的数据(如货币交易)的数据库
- Amazon DocumentDB：MongoDB的克隆(不完全兼容)
- Amazon Keyspaces：托管的Apache Cassandra的克隆

<a name="53612a60"></a>

## Migration & Transfer 数据迁移和传输

- Migration Hub：从数据中心迁移到AWS
- Application Discovery Service：在您的数据中心提供检测服务
- Database Migration Service：可以将运行中的数据库迁移到RDS，不同的数据结构之间也可以实施
- Server Migration Service：：可以将虚拟机迁移到AWS
- AWS Transfer Family：以S3为基础的(s)FTP服务。可以通过FTP将数据传输到S3存储桶
- Snowball：可申领一台AWS机器并连接到您的数据中心，将数据快速传输到AWS后再归还机器
- DataSync(DataSync)：在数据中心和AWS之间同步数据

<a name="b440ff46"></a>

## Networking & Content Delivery 网络和内容传送

- VPC：在AWS中创建您自己的VPN
- CloudFront：内容传送网络CDC
- Route 53：管理域名和记录DNS
- API Gateway：创建HTTP API并将它们连接到不同的后端
- Direct Connect：(物理)连接您的系统(或数据中心)和AWS
- AWS App Mesh：可以作为您的容器(ECS或EKS)的sidecar自动运行Envoy
- AWS Cloud Map：为您的容器提供检测服务
- Global Accelerator：在边缘位置运行应用程序（CDN的应用程序版本）

<a name="b5b1c447"></a>

## Developer Tools 开发工具

- CodeStar(CodeStar)：可以使用template code、CodeCommit和CodeBuild的模板快速开发应用程序
- CodeCommit：亚马逊资源存储库(如git存储库等)
- CodeBuild：持续集成服务
- CodeDeploy：部署服务
- CodePipeline：按照定义的工作流进行代码传送
- Cloud9：在线的集成开发环境IDE
- X-Ray：可以分析和调试应用程序，支持Python、Node.js、Go等开发语言

<a name="925e90e3"></a>

## Robotics 机器人

- AWS RoboMaker：为机器人工程师提供的云端解决方案，可用于模拟、测试和安全部署机器人的应用程序

<a name="00a11ee9"></a>

## Customer Enablement 针对每个客户的优化

- AWS IQ：可以根据需要聘请AWS专家的招工板
- Support：AWS支持中心
- Managed Services：委托AWS为您运行管理AWS服务

<a name="15b49ff4"></a>

## Blockchain 区块链

- Amazon Managed Blockchain：区块链

<a name="dd9c0a82"></a>

## Satellite 卫星

- Ground Station：分时无线电和指向太空的大型天线

<a name="66d261c2"></a>

## Quantum Technologies 量子技术

- Amazon Braket：一些量子技术

<a name="81efd513"></a>

## Management & Governance 管理与监管

- AWS Organizations：设置多个组织和帐户
- CloudWatch：从不同的AWS组件获取日志
- AWS Auto Scaling：根据您自己设置的输入和规则对资源进行缩放
- CloudFormation：使用模板创建和设置AWS组件
- CloudTrail：记录在您的AWS服务中谁做了什么
- Config：审核您的AWS资源配置
- OpsWorks：通过Ansible实现自动化运维
- Service Catalog：管理云端的项目或代码的列表
- Systems Manager：可以自由对资源进行分组和查看数据，例如单个应用程序
- AWS AppConfig：可以保存或发布应用程序的配置数据
- Trusted Advisor：检查账户成本和安全性等问题
- Control Tower：管理多个帐户
- AWS License Manager：管理许可证
- AWS Well-Architected Tool：创建关于系统的问卷调查，并查看其是否符合最佳实践路线
- Personal Health Dashboard：AWS状态页面
- AWS Chatbot：可以使AWS与Slack联动
- Launch Wizard：用来部署MS SQL或SAP的软件
- AWS Compute Optimizer：发现最佳资源并指导您如何降低成本

<a name="1041ac50"></a>

## Media Services：媒体服务

- Elastic Transcoder：将S3的文件转换为不同的格式或者以S3格式存储
- Kinesis Video Streams：捕获媒体流
- Elemental MediaConnect：截止目前内容不明
- Elemental MediaConvert：将媒体转换为不同的格式
- Elemental MediaLive：分享实时视频
- Elemental MediaPackage：截止目前内容不明
- Elemental MediaStore：截止目前内容不明
- Elemental MediaTailor：在视频广播中插入广告
- Elemental Appliances & Software：可以在本地创建视频，基本上是上述服务的组合

<a name="7b798727"></a>

## Machine Learning 机器学习

- Amazon SageMaker：机器学习工具
- Amazon CodeGuru：在机器学习中配置Java代码
- Amazon Comprehend：理解并对邮件和推文的内容进行分类
- Amazon Forecast：根据数据进行预测
- Amazon Fraud Detector：截止目前内容不明
- Amazon Kendra：通过问题搜索服务
- Amazon Lex：可以创建语音对话和聊天机器人
- Amazon Machine Learning：不推荐，SageMaker是后继产品
- Amazon Personalize：可以根据数据创建针对个人做最优化的推荐
- Amazon Polly：可以从文本转换为不同语种的语音
- Amazon Rekognition：识别图像中的物体或人物
- Amazon Textract：识别图像中的文本并将其作为文本输出(光学字符识别)
- Amazon Transcribe：将音声转换为文本
- Amazon Translate：将文本翻译成其他语言
- AWS DeepLens：进行机器学习的摄像机
- AWS DeepRacer：一种在机器学习中编程竞赛的赛车游戏
- Amazon Augmented AI：让人类参与学习流程，使机器学习更好
- AWS DeepComposer：用电脑作曲，听上去相当的厉害

<a name="4067cd21"></a>

## Analytics 分析

- Athena：将查询数据保存在S3存储桶中
- EMR：大数据框架可以执行缩放
- CloudSearch：托管文档搜索系统(Elasticsearch的AWS版本)
- Elasticsearch Service：SaaS的Elasticsearch
- Kinesis：以可分析的形式收集大量数据(可能类似ELK)
- QuickSight：商业智能服务
- Data Pipeline：将数据移动或变换格式到DynamoDB、RDS或S3等
- AWS Data Exchange：寻找那些数据可以加以利用的API，但这可能会非常昂贵
- AWS Glue：ETL提高和验证服务和数据质量
- AWS Lake Formation：数据湖(数据湖)创建(创建)
- MSK：SaaS的Apache Kafka

<a name="dc50312d"></a>

## Security, Identity, & Compliance 安全、识别和合规性

- IAM：AWS权限系统，可管理用户和AWS服务
- Resource Access Manager：与其他账户共享AWS资源，如Route 53和EC2
- Cognito：用户和密码管理系统，方便应用程序的用户管理。
- Secrets Manager：保护加密数据，如密钥。也可以自动轮换秘密
- GuardDuty：CloudTrail 自动扫描VPC日志以应对威胁
- Inspector：自动检测网络和机器的(安全)问题
- Amazon Macie：分析S3存储桶中的数据并检查您的个人信息
- AWS Single Sign-On：可以在应用程序中使用单点登录功能
- Certificate Manager：管理SSL证书和颁发(免费)证书
- Key Management Service：管理加密密钥
- CloudHSM：硬件安全模块,可以生成和操作加密密钥
- Directory Service：SaaS的动态目录
- WAF & Shield：Web应用防火墙,可以设置规则或指定预先准备的规则
- AWS Firewall Manager：组织内不同帐户的防火墙管理
- Artifact：云合规性文档(ISO/IEC 27001类似的东西)
- Security Hub：利用GuardDuty网络、Inspector主机、Macie数据等的综合安全检查器
- Detective：(来自Security Hub等)将安全问题留在日志中

<a name="2289de2c"></a>

## Mobile 移动设备

- AWS Amplify：在AWS上自动生成并自动部署前端和后端应用程序
- Mobile Hub：现在Amplify的一部分
- AWS AppSync：可以创建可连接的后端API，也可以通过Amplify创建
- Device Farm：AWS的BrowserStack，可以在不同的移动设备和浏览器上自动进行测试。

<a name="c59872f6"></a>

## AR & VR 增强现实和虚拟现实

- Amazon Sumerian：创建3D场景和VR应用

<a name="7b9aba5f"></a>

## Application Integration 应用程序集成

- Step Functions：可以用亚马逊自己的语言描述机器配置
- Amazon AppFlow：可以自动绑定多个应用程序(可能类似zapier)
- Amazon EventBridge：类似eventbus系统
- Amazon MQ：由亚马逊管理的ActiveMQ
- Simple Notification Service：通过电子邮件、短信等方式通知系统
- Simple Queue Service：消息队列(消息队列)系统的系统
- SWF：可以创建工作流程

<a name="31a54a6b"></a>

## AWS Cost Management AWS的成本管理

- AWS Cost Explorer：可视化AWS成本状况
- AWS Budgets：创建AWS预算
- AWS Marketplace Subs criptions：查找并购买已安装软件的AMI

<a name="c717a959"></a>

## Customer Engagement 客户交互

- Amazon Connect：AWS呼叫中心平台
- Pinpoint：通过模板创建交易用的电子邮件、短信或语音电话
- Simple Email Service：邮件提供商，可以发送邮件

<a name="01833e75"></a>

## Business Applications 商业应用程序

- Alexa for Business：将业务与Alexa联系起来
- Amazon Chime：Zoom的AWS版本
- WorkMail：AWS版本的Gmail和谷歌日历

<a name="2d01dcdf"></a>

## End User Computing 终端用户计算机技术

- WorkSpaces：提供Windows或Linux的虚拟桌面服务
- AppStream 2.0：可以将应用程序分发到浏览器
- WorkDocs：可以在线保存和管理文档
- WorkLink：可以将移动端用户连接到内联网

<a name="0b7cd380"></a>

## Internet Of Things 物联网

- IoT Core：通过MQTT代理管理IoT设备组
- FreeRTOS：用于微型控制器的RTOS操作系统，可自动连接到IoT Core或Greengrass
- IoT1-Click：一键连接和管理Lambda等系统
- IoT Analytics：可以结构化和存储各种消息进行分析
- IoT Device Defender：检测设备异常并采取行动
- IoT Device Management：对IoT设备进行分组，为作业安排和远程访问设置
- IoT Events：监控设备使用情况，并自行执行AWS服务和作业
- IoT Greengrass：如果到IoT Core的连接是断断续续的，消息代理可以对最多200台能够相互通信的本地设备进行数据缓冲
- IoT SiteWise：收集、结构化、分析和视觉化来自工业设备的数据
- IoT Things Graph：类似CloudFormatation的设计工具，用于将设备与其他AWS服务的通信方式视觉化

<a name="62746af4"></a>

## Game Development 游戏开发

- Amazon GameLift：在AWS上部署游戏服务器

<a name="ded16b00"></a>

## Containers 容器

- Elastic Container Registry：可以像在Docker Hub一样保存Docker映像
- Elastic Container Service：可以在您自己的EC2机器或者所管理的Fargate机器上运行container
- Elastic Kubernetes Service：SaaS的Kubernetes
