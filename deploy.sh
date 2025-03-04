#!/bin/bash
cp quartz.config.prod.ts quartz.config.ts
git add quartz.config.ts
git commit -m "Switch to production config"
git push origin main

