---
permalink: "AI/MCP"
title: MCP
tags:
  - агенты
---
MCP (Model Context Protocol) — открытый протокол, через который AI-приложения
подключаются к внешним инструментам и источникам данных: файлам, поиску,
базам данных и другим программам. См. [официальное введение](https://modelcontextprotocol.io/docs/getting-started/intro).

Приложение с поддержкой MCP подключается к MCP-серверу. Сервер предоставляет
инструменты и данные, с которыми приложение может работать: например, прочитать
документ или изменить параметры проекта. Сервер может работать локально или
удалённо. Подробности — в [обзоре архитектуры](https://modelcontextprotocol.io/docs/learn/architecture).

Здесь собраны материалы про MCP и интересные интеграции. Подборка будет дополняться.
Ссылки проверены 29 октября 2026 года; серверы не устанавливались и не запускались.

## Материалы

- [Что такое MCP](https://modelcontextprotocol.io/docs/getting-started/intro) — официальное введение
- [Подключение локального MCP-сервера](https://modelcontextprotocol.io/quickstart/user) — официальное руководство на примере Claude Desktop
- [Статья о MCP на Хабре](https://habr.com/ru/articles/914774/)

## Интересные интеграции

- [TWOZERO](https://twozero.ai/) — инструменты для TouchDesigner со встроенным MCP-сервером. Подключённый AI-агент может читать проект, создавать и соединять операторы, менять параметры и разбирать ошибки. [Документация TouchDesigner MCP](https://twozero.ai/docs/mcp).

- [OpenDia](https://github.com/aeonfun/opendia) — расширение браузера и MCP-сервер для подключения AI-клиента к страницам и вкладкам; поддерживает Chrome, Firefox и браузеры на Chromium

## Каталоги серверов

- [Официальный MCP Registry](https://registry.modelcontextprotocol.io/) — реестр серверов проекта MCP
- [MCP Servers](https://mcp.so/) — каталог серверов и клиентских инструментов
- [Примеры MCP-серверов](https://github.com/modelcontextprotocol/servers/tree/main)
- [Smithery](https://smithery.ai/) — каталог серверов. По [объявлению](https://smithery.ai/future), 31 октября 2026 года отключаются MCP Proxy и управление подключениями (включая run.tools, server.smithery.ai, API, CLI и SDK), но публичный каталог остаётся. На дату проверки 29 октября отключение ещё впереди
- [Glama](https://glama.ai/mcp/servers) — каталог открытых MCP-серверов


Для интерактивной графики MCP также используется в Sentinel: см. [[Модели изображений#Реалтайм рисовалки]].
