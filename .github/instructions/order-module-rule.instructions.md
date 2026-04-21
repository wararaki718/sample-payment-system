# order モジュールのルール

## 依存可能なモジュール
- inventory（在庫確認のため、読み取りのみ）
- payment（決済処理のため、読み取りのみ）

## 依存禁止
- shipping モジュールの internal/ への直接アクセス
- user モジュールの DB スキーマへの直接クエリ

## このモジュールが発行するイベント
- OrderPlaced: 注文確定時
- OrderCancelled: 注文キャンセル時