#!/bin/bash
cp quartz.config.dev.ts quartz.config.ts
node quartz/bootstrap-cli.mjs build --serve

