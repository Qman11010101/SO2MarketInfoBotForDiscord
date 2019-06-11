def alias(itemName):
    if itemName == "紙":
        return "紙束"
    elif itemName == "彩薬":
        return "駆け出し勇者の彩薬"
    elif itemName == "極彩薬":
        return "駆け出し勇者の極彩薬"
    elif itemName == "スピポ":
        return "スピードポーション"
    else:
        # エイリアス名がない場合はそのまま返す
        return itemName
