#!/bin/bash

echo "[SETTING UP ALEMBIC]"
echo "[ALEMBIC_MODE] = " "${ALEMBIC_MODE}"
echo "========================="

cd src/API

ls -a alembic/versions

if [ "${ALEMBIC_MODE}" = "upgrade" ]
then
  alembic upgrade head
elif [ "${ALEMBIC_MODE}" = "init" ]
then
  alembic revision --autogenerate -m "API Migration"
  alembic upgrade head
elif [ "${ALEMBIC_MODE}" = "reset" ]
then
  echo TODO
fi

