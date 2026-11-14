@echo off
REM Day 7 - danh gia test moi voi cau hinh da chot.
setlocal
cd /d "%~dp0"
if "%DAY6_DIR%"=="" set "DAY6_DIR=%~dp0..\K5-L3A-DAY06-NguyenCongTinh-2A202603373-DataIngestion"
set "PY=%DAY6_DIR%\.venv\Scripts\python.exe"
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
pushd "%DAY6_DIR%\starter"
docker compose -p day6_student_starter up -d --wait || (popd & echo Loi Docker & exit /b 1)
popd
"%PY%" -m unittest discover -s tests || exit /b 1
"%PY%" run.py check --db || exit /b 1
"%PY%" run.py retrieval --split test || exit /b 1
"%PY%" run.py agent --split test --configs baseline selected || exit /b 1
"%PY%" run.py report
echo.
echo XONG TEST V2.
endlocal
