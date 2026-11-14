@echo off
REM Day 7 - lan chay 2: agent v2 (sua loi citation tim thay tren dev) + bo test moi.
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
"%PY%" run.py agent --split dev --configs dense_k3 bm25_k3 hybrid_k3 hybrid_rerank_k3 hybrid_k5_neighbors || exit /b 1
"%PY%" run.py report
echo.
echo XONG DEV V2. Bao Claude kiem tra truoc khi chay test.
endlocal
