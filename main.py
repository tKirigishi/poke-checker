name: Pokemon Card Checker

on:
  schedule:
    - cron: '*/10 * * * *'  # 10分おきに実行
  workflow_dispatch:        # 手動実行ボタンを有効にする

jobs:
  run-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install playwright
          playwright install chromium
      - name: Run script
        env:
          GMAIL_USER: ${{ secrets.GMAIL_USER }}
          GMAIL_PASS: ${{ secrets.GMAIL_PASS }}
          TO_EMAIL: ${{ secrets.TO_EMAIL }}
        run: python main.py
