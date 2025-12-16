"""
نظام مراقبة Conscious Bridge
"""
import time
from datetime import datetime
from typing import Dict, Any

class SystemMetrics:
    """جمع مقاييس أداء النظام"""
    
    def __init__(self):
        self.start_time = time.time()
        self.metrics_log = []
    
    def record_metric(self, name
cat > ~/conscious-bridge-reloaded/monitoring/metrics.py << 'EOF'
"""
نظام مراقبة Conscious Bridge
"""
import time
from datetime import datetime
from typing import Dict, Any, List
import json

class SystemMetrics:
    """جمع مقاييس أداء النظام"""
    
    def __init__(self, system_name: str = "ConsciousBridge"):
        self.system_name = system_name
        self.start_time = time.time()
        self.metrics_log: List[Dict] = []
        self.error_count = 0
        self.success_count = 0
        
    def record_metric(self, name: str, value: float, tags: Dict = None):
        """تسجيل مقياس جديد"""
        metric = {
            "timestamp": datetime.now().isoformat(),
            "metric": name,
            "value": value,
            "tags": tags or {},
            "system": self.system_name
        }
        self.metrics_log.append(metric)
        return metric
    
    def record_success(self, operation: str, duration: float):
        """تسجيل عملية ناجحة"""
        self.success_count += 1
        return self.record_metric(
            "operation_success",
            duration,
            {"operation": operation, "status": "success"}
        )
    
    def record_error(self, operation: str, error_msg: str):
        """تسجيل خطأ"""
        self.error_count += 1
        return self.record_metric(
            "operation_error",
            1.0,
            {"operation": operation, "error": error_msg, "status": "error"}
        )
    
    def get_summary(self) -> Dict[str, Any]:
        """ملخص المقاييس"""
        uptime = time.time() - self.start_time
        
        return {
            "system": self.system_name,
            "uptime_seconds": round(uptime, 2),
            "uptime_human": str(datetime.utcfromtimestamp(uptime).strftime('%H:%M:%S')),
            "total_operations": len(self.metrics_log),
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": round(self.success_count / max(1, self.success_count + self.error_count), 3),
            "timestamp": datetime.now().isoformat()
        }
    
    def export_metrics(self, filename: str = "metrics.json"):
        """تصدير المقاييس لملف"""
        data = {
            "summary": self.get_summary(),
            "recent_metrics": self.metrics_log[-100:],  # آخر 100 مقياس
            "export_time": datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filename

# نموذج استخدام
if __name__ == "__main__":
    monitor = SystemMetrics("ConsciousBridge-v2.1")
    
    # تسجيل عمليات تجريبية
    monitor.record_success("system_initialization", 0.15)
    monitor.record_success("core_module_import", 0.08)
    monitor.record_metric("memory_usage_mb", 45.2, {"type": "memory"})
    monitor.record_metric("cpu_usage_percent", 12.5, {"type": "cpu"})
    
    summary = monitor.get_summary()
    print("📊 ملخص المراقبة:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # تصدير للملف
    monitor.export_metrics("system_metrics.json")
    print(f"✅ تم تصدير المقاييس إلى: system_metrics.json")
