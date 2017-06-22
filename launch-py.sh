#!/usr/bin/env bash
until python3 Main.py; do echo attempting to recover; sleep 2;
echo exited successfully
done
