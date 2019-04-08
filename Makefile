APK=bin/pyrtm-0.1-debug.apk
SOURCE=main.py
KV=roguetrader.kv
BUILDOZER=buildozer.spec

$(APK): $(SOURCE) $(KV) $(BUILDOZER)
	buildozer android debug

deploy: $(APK)
	cp $(APK) ~/Sync
