### 用法

```bat=
run.bat
```

#### 啟動流程

run.bat -> driver.py -> runner.py (*4，依照driver裡面設定的數量) -> main.py

至此就會開啟四個節點

#### 系統架構

* 專案目錄
    > 主要存放啟動用程式
    * 有使用
        1. run.bat: 在windows下執行會啟動driver.py
        2. driver.py:    啟動後會開4個執行緒，每個執行緒都會執行runner.py
        3. runner.py:    有兩種模式可以執行main.py
            1. stdout在終端上
            2. 寫在./log/port裡面
                > 還需要分ip，因為目前我都只需要用port來區分不同節點
        4. data.bin.txt: 來自無人機的資料
    * 沒有使用
        1. update.py:    之前寫紀錄用的
        2. Parser.cpp:   廢棄
        3. bug.txt: 之前debug用的
        4. temp.log:   之前debug用的
* ./main目錄
    > 主要存放




