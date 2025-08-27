# 检查需要的模块列表
required_modules = ['psutil', 'requests', 'numpy']
missing_modules = []

for module in required_modules:
    try:
        # 尝试导入模块
        __import__(module)
    except ImportError:
        # 捕获导入失败，记录缺失模块
        missing_modules.append(module)

if missing_modules:
    print(f"缺少以下模块：{', '.join(missing_modules)}")
    print(f"请安装：pip install {' '.join(missing_modules)}")
else:
    print("所有依赖模块均已安装")