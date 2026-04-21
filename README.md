# sample-payment-system

FastAPI + Uvicorn で構成した、モジュール分割型のサンプル決済システムです。

## セットアップ

1. 依存関係をインストール

```bash
pip install -r requirements.txt
```

2. サーバー起動

```bash
uvicorn src.main:app --reload
```

## 動作確認

ヘルスチェック:

```bash
curl http://127.0.0.1:8000/health
```

注文作成:

```bash
curl -X POST http://127.0.0.1:8000/orders \\
	-H "Content-Type: application/json" \\
	-d '{
		"customer_id": "customer-001",
		"currency": "jpy",
		"items": [
			{"sku": "SKU-APPLE", "quantity": 2, "unit_price": 120},
			{"sku": "SKU-BANANA", "quantity": 1, "unit_price": 80}
		]
	}'
```
