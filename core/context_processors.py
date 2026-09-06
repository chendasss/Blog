"""把站点配置注入所有模板上下文。"""
from .models import SiteSetting


def site_settings(request):
    try:
        return {"site": SiteSetting.load()}
    except Exception:
        # 数据库未迁移等情况下降级，避免站点崩溃
        return {}
