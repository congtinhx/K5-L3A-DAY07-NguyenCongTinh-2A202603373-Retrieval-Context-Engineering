@echo off
REM Day 7 - chay toan bo thi nghiem. Chay tu thu muc goc repo Day 7 (double-click hoac CMD).
setlocal
cd /d "%~dp0"
if "%DAY6_DIR%"=="" set "DAY6_DIR=%~dp0..\K5-L3A-DAY06-NguyenCongTinh-2A202603373-DataIngestion"
set "PY=%DAY6_DIR%\.venv\Scripts\python.exe"
if not exist "%PY%" (echo Khong tim thay venv Day 6: %PY% & exit /b 1)
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

echo === Bat PostgreSQL + pgvector Day 6
pushd "%DAY6_DIR%\starter"
docker compose -p day6_student_starter up -d --wait || (popd & echo Loi Docker & exit /b 1)
popd

"%PY%" -m unittest discover -s tests || exit /b 1
"%PY%" run.py export-chunks --from db || exit /b 1
"%PY%" run.py check --db || exit /b 1
"%PY%" run.py retrieval --split dev || exit /b 1
"%PY%" run.py select || exit /b 1
"%PY%" run.py agent --split dev --configs dense_k3 bm25_k3 hybrid_k3 hybrid_rerank_k3 hybrid_k5_neighbors || exit /b 1
"%PY%" run.py retrieval --split test || exit /b 1
"%PY%" run.py agent --split test --configs baseline selected || exit /b 1
"%PY%" run.py report
echo.
echo XONG. Ket qua trong thu muc results\ . Tiep theo: cham tay review_sheet.md -^> reviews.json, roi chay "run.py metrics".
endlocal
