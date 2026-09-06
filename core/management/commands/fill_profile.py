"""一次性填充「AI 大模型工程师（3 年）」示例资料。

用法：python manage.py fill_profile
会覆盖（删除后重建）技能、项目、经历时间线，并更新个人资料与站点配置。
"""
import datetime

from django.core.management.base import BaseCommand

from core.models import Profile, SiteSetting
from portfolio.models import CareerTimeline, Project, Skill


class Command(BaseCommand):
    help = "填充 AI 大模型工程师示例资料（覆盖技能/项目/经历，更新个人资料与站点配置）"

    def handle(self, *args, **options):
        # 1. 个人资料
        profile = Profile.load()
        profile.name = "零花钱没着落"
        profile.title = "AI 大模型工程师 · 探索 AI 编程的能力尽头"
        profile.bio = (
            "3 年 AI 大模型方向研发经验，专注大模型微调、RAG 检索增强与 Agent 应用落地，"
            "熟悉从数据、训练到推理部署的完整链路。主导过多个企业级知识库与智能体项目从 0 到 1，"
            "热衷把前沿技术工程化，也喜欢在博客里沉淀踩坑与思考。"
        )
        profile.location = "上海"
        profile.email = "me@example.com"
        profile.github = "https://github.com/yourname"
        profile.save()
        self.stdout.write("Profile updated")

        # 2. 站点配置
        site = SiteSetting.load()
        site.site_name = "零花钱没着落"
        site.site_description = "AI 大模型工程师的技术博客 · 求职与作品集"
        site.footer_text = "© 2026 零花钱没着落 · 用 Django 构建"
        site.job_seeking = True
        site.job_status_text = "求职中 · 可到岗"
        site.job_target = "AI 大模型 / 算法工程师"
        site.job_available = True
        site.career_category_slug = "career"
        site.save()
        self.stdout.write("SiteSetting updated")

        # 3. 技能（覆盖）
        Skill.objects.all().delete()
        skill_rows = [
            ("Python", "语言", 5, "主力开发语言，异步与并发、性能调优", 1),
            ("Go", "语言", 3, "高并发服务与工具链", 2),
            ("SQL", "语言", 4, "复杂查询、索引与执行计划优化", 3),
            ("PyTorch", "大模型与框架", 4, "模型训练、微调与分布式", 1),
            ("HuggingFace / Transformers", "大模型与框架", 5, "预训练模型、LoRA/QLoRA 微调", 2),
            ("LangChain / LangGraph", "大模型与框架", 4, "RAG、工具调用、多智能体编排", 3),
            ("vLLM", "大模型与框架", 4, "高吞吐推理部署", 4),
            ("FastAPI", "大模型与框架", 4, "模型服务化与 API 设计", 5),
            ("PostgreSQL", "数据与存储", 3, "业务数据建模", 1),
            ("Redis", "数据与存储", 3, "缓存、队列、限流", 2),
            ("Milvus / 向量库", "数据与存储", 4, "RAG 检索、向量索引", 3),
            ("Elasticsearch", "数据与存储", 3, "全文检索与日志", 4),
            ("Docker", "工具与部署", 4, "容器化与镜像优化", 1),
            ("Kubernetes", "工具与部署", 3, "服务编排与滚动发布", 2),
            ("Linux", "工具与部署", 4, "日常开发与排障", 3),
            ("模型量化与推理优化", "工具与部署", 4, "AWQ/GPTQ、TensorRT-LLM", 4),
        ]
        Skill.objects.bulk_create(
            [Skill(name=n, category=c, level=l, description=d, order=o) for n, c, l, d, o in skill_rows]
        )
        self.stdout.write(f"Skills: {len(skill_rows)}")

        # 4. 项目（覆盖）
        Project.objects.all().delete()
        project_rows = [
            dict(
                title="企业级 RAG 知识库平台",
                summary="面向企业内部文档的多模态检索增强问答系统，支持混合检索与引用溯源。",
                description="""## 背景
企业内部文档散落在多个系统，检索效率低、回答缺乏来源依据。基于大模型构建统一的知识库问答平台。

## 我的职责
- 设计并实现文档解析、切片、向量化与入库流水线，支持 PDF / Word / Markdown 等格式
- 构建「向量检索 + 关键词检索 + 重排序」的混合检索链路，提升召回准确率
- 实现引用溯源，让回答可追溯到原文片段

## 成果
- 知识库问答准确率提升 30%，平均响应延迟 < 2s
- 服务 10+ 个内部团队，日查询量 5w+
""",
                tech_stack="Python,LangChain,Milvus,Elasticsearch,FastAPI,PostgreSQL",
                order=0,
                is_featured=True,
            ),
            dict(
                title="多智能体 Agent 编排框架",
                summary="支持工具调用、长短期记忆与多 Agent 协作的通用 Agent 运行框架。",
                description="""## 背景
复杂任务（竞品调研、代码生成等）难以用单个 LLM 一次性完成，需要多智能体分工协作。

## 我的职责
- 基于 LangGraph 设计可编排的 Agent 图，支持并行、条件分支与人工确认节点
- 实现工具调用沙箱与重试、超时、降级机制
- 引入分层记忆（短期会话 + 长期向量记忆）

## 成果
- 多步任务的端到端成功率从 62% 提升到 85%
- 已复用于 3 条产品线，平均节省 40% 人工处理时间
""",
                tech_stack="Python,LangGraph,OpenAI API,Redis,PostgreSQL",
                order=1,
                is_featured=True,
            ),
            dict(
                title="大模型推理加速与量化服务",
                summary="基于 vLLM + AWQ 量化的高吞吐推理服务，显著降低部署成本。",
                description="""## 背景
自部署 7B/13B 模型成本高、吞吐低，无法满足业务并发需求。

## 我的职责
- 基于 vLLM 搭建推理服务，实现连续批处理与动态显存管理
- 用 AWQ/GPTQ 做 4-bit 量化，在精度损失 < 1% 的前提下压缩模型
- 编写压测脚本，调优并发、显存与延迟

## 成果
- 7B 模型推理吞吐提升 3 倍，单卡成本降低 60%
- 线上 P99 延迟从 3.2s 降到 1.1s
""",
                tech_stack="Python,vLLM,PyTorch,量化,GPU",
                order=2,
                is_featured=True,
            ),
            dict(
                title="AI 技术博客与阅读笔记助手",
                summary="用 Django 构建的个人技术博客，集成本地 LLM 自动生成文章摘要与标签。",
                description="""## 背景
搭建个人技术博客，沉淀大模型方向的踩坑与思考，同时作为求职作品展示。

## 我的职责
- 用 Django 从零搭建博客，含 Markdown 渲染、评论、相册、搜索、深色模式
- 接入 LLM API，为文章自动生成摘要与标签建议
""",
                tech_stack="Python,Django,LLM API,Markdown",
                order=3,
                is_featured=False,
            ),
        ]
        for p in project_rows:
            Project.objects.create(**p)
        self.stdout.write(f"Projects: {len(project_rows)}")

        # 5. 经历时间线（覆盖）
        CareerTimeline.objects.all().delete()
        CareerTimeline.objects.bulk_create(
            [
                CareerTimeline(
                    type="work",
                    org="某 AI 科技公司",
                    role="大模型算法工程师",
                    start_date=datetime.date(2023, 7, 1),
                    end_date=None,
                    description="负责企业级 RAG 知识库与多智能体平台的研发：主导检索链路优化、Agent 编排框架设计与推理服务降本，推动多项能力从 0 到 1 落地。",
                    order=0,
                ),
                CareerTimeline(
                    type="education",
                    org="某大学",
                    role="硕士 · 计算机科学与技术（人工智能方向）",
                    start_date=datetime.date(2020, 9, 1),
                    end_date=datetime.date(2023, 6, 1),
                    description="研究方向为大语言模型与自然语言处理，期间在互联网公司实习，参与搜索/推荐相关算法工作。",
                    order=1,
                ),
                CareerTimeline(
                    type="education",
                    org="某大学",
                    role="本科 · 软件工程",
                    start_date=datetime.date(2016, 9, 1),
                    end_date=datetime.date(2020, 6, 1),
                    description="系统学习计算机基础，多次获校级奖学金，参加 ACM 校队。",
                    order=2,
                ),
            ]
        )
        self.stdout.write("Timeline: 3")

        self.stdout.write(self.style.SUCCESS("Done"))
