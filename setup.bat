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
    echo.
    echo 安装时请勾选 "Add Python to PATH" 选项
    pause
    exit /b 1
)

:: 获取 Python 版本
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [√] Python 已安装，版本: %PYTHON_VERSION%

:: 检查 Python 版本是否 >= 3.8
python -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>nul
if errorlevel 1 (
    echo [错误] Python 版本过低，需要 3.8 或更高版本
    echo 当前版本: %PYTHON_VERSION%
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [√] Python 版本符合要求 (>= 3.8)
echo.

:: 询问是否使用虚拟环境
echo 是否创建虚拟环境？(推荐，可以隔离项目依赖)
echo [1] 是，创建虚拟环境 (推荐)
echo [2] 否，直接安装到系统 Python
echo.
set /p VENV_CHOICE="请选择 (1/2，默认1): "

if "%VENV_CHOICE%"=="" set VENV_CHOICE=1
if "%VENV_CHOICE%"=="1" (
    echo.
    echo [*] 正在创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 虚拟环境创建失败
        pause
        exit /b 1
    )
    echo [√] 虚拟环境创建完成
    
    :: 激活虚拟环境
    echo [*] 正在激活虚拟环境...
    call venv\Scripts\activate.bat
    echo [√] 虚拟环境已激活
    set PIP_CMD=venv\Scripts\pip.exe
    set PYTHON_CMD=venv\Scripts\python.exe
) else (
    set PIP_CMD=pip
    set PYTHON_CMD=python
)
echo.

:: 升级 pip
echo [*] 正在升级 pip...
%PYTHON_CMD% -m pip install --upgrade pip -q
echo [√] pip 升级完成
echo.

:: 安装依赖
echo [*] 正在安装项目依赖...
echo     - LunarCalendar (农历计算)
echo     - unihan-etl (汉字笔画数据)
echo     - opencc-python-reimplemented (简繁转换)
echo.
%PIP_CMD% install -r requirements.txt -q
if errorlevel 1 (
    echo [错误] 依赖安装失败，请检查网络连接
    echo 提示: 如果在中国大陆，可能需要配置 pip 镜像源:
    echo   pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
    pause
    exit /b 1
)
echo [√] 依赖安装完成
echo.

:: 初始化 unihan 数据（用于笔画计算）
echo [*] 正在初始化汉字笔画数据...
echo     (首次运行需要下载数据，请耐心等待约1-2分钟)
echo.
%PYTHON_CMD% -c "import sys; sys.path.insert(0, '.'); from divination_methods.stroke_counter import get_text_stroke; result = get_text_stroke('股票'); print('[√] 笔画数据初始化成功'); print('    测试: 股票 = %d 画' % result)"
if errorlevel 1 (
    echo [警告] 笔画数据初始化可能有问题，但不影响其他功能
    echo     标的物起卦功能可能无法正常使用
)
echo.

:: 运行简单测试
echo [*] 正在验证安装...
%PYTHON_CMD% -c "from divination_methods import get_day_tiangan; print('[√] 核心模块导入成功')"
if errorlevel 1 (
    echo [警告] 部分模块导入失败，请检查安装
)
echo.

echo ================================================
echo [√] 环境配置完成！
echo ================================================
echo.
if "%VENV_CHOICE%"=="1" (
    echo 使用方法:
    echo   1. 激活虚拟环境: venv\Scripts\activate.bat
    echo   2. 运行程序: python main.py
    echo   3. 退出虚拟环境: deactivate
) else (
    echo 运行命令启动程序: python main.py
)
echo.
echo 如遇到问题，请查看 README.md 或联系开发者
echo ================================================
pause