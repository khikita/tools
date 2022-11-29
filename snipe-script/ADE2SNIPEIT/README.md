
## 概要
Jamf ProとApple Business Managerを利用している場合に、Jamf ProのDEPに登録されたことをトリガーにWebhookを受信し、そのデータを利用してSNIPE-ITへ資産登録します。

## 前提
- Jamf Proライセンスがあること
- Apple Business Managerの設定が完了していること
- SNIPE-ITの設定が完了していること
- 有効なAWSアカウントがあること（Lambda利用のため）

## 設定変更部分

以下の部分の、
- category_id
- manufacturer_id
- fieldset_id
は設定したい内容に変更してください

```
def create_model(modelName):
    url = urljoin(SNIPE_URL, "/api/v1/models")
    #拡張フィールドセットIDにJamf用をセットして作成する
    payload = {
        "name" : modelName,
        "model_number" : modelName,
        "category_id" : 2,
        "manufacturer_id" : 1,
        "fieldset_id" : 2 
    }
```

## 解説ブログ
