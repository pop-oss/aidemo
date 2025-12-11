@echo off
REM AI 代码流水线快速设置脚本 (Windows)

echo 🚀 AI 代码流水线 - 快速设置
echo ==============================
echo.

REM 检查 Python
echo 检查 Python 版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到 Python
    echo    请安装 Python 3.11 或更高版本
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python 版本: %PYTHON_VERSION%
echo.

REM 创建虚拟环境
echo 创建虚拟环境...
if not exist "venv" (
    python -m venv venv
    echo ✅ 虚拟环境已创建
) else (
    echo ✅ 虚拟环境已存在
)
echo.

REM 激活虚拟环境
echo 激活虚拟环境...
call venv\Scripts\activate.bat
echo ✅ 虚拟环境已激活
echo.

REM 安装依赖
echo 安装依赖...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ 依赖安装失败
    exit /b 1
)
echo ✅ 依赖安装完成
echo.

REM 创建 .env 文件
if not exist ".env" (
    echo 创建 .env 文件...
    copy .env.example .env
    echo ✅ .env 文件已创建
    echo.
    echo ⚠️  重要: 请编辑 .env 文件并设置以下变量:
    echo    - OPENAI_API_KEY=your-key
    echo    - CLAUDE_API_KEY=your-key (可选)
    echo    - LLM_PROVIDER=openai
    echo.
) else (
    echo ✅ .env 文件已存在
    echo.
)

REM 运行测试
echo 运行测试验证安装...
pytest example_app\tests\ -v -q
if errorlevel 1 (
    echo ⚠️  部分测试失败,但不影响主流程
) else (
    echo ✅ 测试通过!
)
echo.

echo ==============================
echo ✅ 设置完成!
echo.
echo 下一步:
echo   1. 编辑 .env 文件,设置 API Key
echo   2. 运行流水线:
echo      python orchestrator\orchestrator.py --requirement "你的需求"
echo.
echo 示例:
echo   python orchestrator\orchestrator.py --requirement "创建一个用户认证 API"
echo.
echo 查看帮助:
echo   python orchestrator\orchestrator.py --help
echo.

pause
