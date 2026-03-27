@echo off
chcp 65001 >nul
echo ================================================
echo        六爻起卦系统 - 环境配置脚本
echo ================================================
echo.

:: 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [√] Python 已安装
python --version
echo.

:: 升级 pip
echo [*] 正在升级 pip...
python -m pip install --upgrade pip -q
echo [√] pip 升级完成
echo.

:: 安装依赖
echo [*] 正在安装项目依赖...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)
echo [√] 依赖安装完成
echo.

:: 初始化 unihan 数据（用于笔画计算）
echo [*] 正在初始化汉字笔画数据（首次运行需要下载，请耐心等待）...
python -c "from stroke_counter import get_text_stroke; print('测试笔画: 股票 =', get_text_stroke('股票'))"
if errorlevel 1 (
    echo [警告] 笔画数据初始化可能有问题，但不影响其他功能
)
echo.

echo ================================================
echo [√] 环境配置完成！
echo.
echo 运行命令启动程序: python main.py
echo ================================================
pause