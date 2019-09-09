APK=bin/pyrtm-0.1-debug.apk
SOURCE=main.py
KV=roguetrader.kv
BUILDOZER=buildozer.spec

ifneq ("$(wildcard $(HOME)/.poetry/bin/poetry)", "")
	POETRY := $(HOME)/.poetry/bin/poetry
else
	POETRY := /usr/bin/poetry
endif
POETRY_RUN := $(POETRY) run

main: data/rogue_trader_data.json
	$(POETRY_RUN) python3 main.py

$(APK): $(SOURCE) $(KV) $(BUILDOZER) data/rogue_trader_data.json
	$(POETRY_RUN) buildozer android debug

deploy: $(APK)
	cp $(APK) ~/Sync

data/rogue_trader_data.json: data/rogue_trader_data.py
	$(POETRY_RUN) data/rogue_trader_data.py

debug: data/rogue_trader_data.json
	$(POETRY_RUN) python3 -m pdb main.py
