#!/bin/sh
# Simple backup of the SQLite database
mkdir -p backups
DATE=$(date +%Y%m%d)
zip -j backups/backup_$DATE.zip dsvgo.db 2>/dev/null
