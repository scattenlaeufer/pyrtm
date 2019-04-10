APK=bin/pyrtm-0.1-debug.apk
SOURCE=main.py
KV=roguetrader.kv
BUILDOZER=buildozer.spec

$(APK): $(SOURCE) $(KV) $(BUILDOZER) data/rogue_trader_data.json
	buildozer android debug

deploy: $(APK)
	cp $(APK) ~/Sync

data/rogue_trader_data.json: data/rogue_trader_data.py
	data/rogue_trader_data.py
