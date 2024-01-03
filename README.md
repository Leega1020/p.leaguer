# P.LEAGUER

**P.LEAGUER** P.LEAGUER是根據台灣男子籃球聯盟 PLUS LEAGUE 官方資訊，為球迷打造快速瀏覽賽程及周邊資訊，並且提供會員功能含訂閱開啟賽程通知、我的最愛收藏、簽到系統等互動功能個人化網站

## 開發語言

- **Front-end:** HTML, CSS
- **Back-end:** Python, Flask, MySQL, Redis
- **Tools:** AWS EC2, Linux, Git, Docker, Nginx

## 特點

- 使用 Flask 框架搭建的後端應用程式
- 整合 Line 登入和推播通知功能
- 連接 MySQL 資料庫並使用 Redis 快取達到資料庫優化
- 定時任務完成資料更新
- 提供 API 供前端呼叫取得資料

## System Architecture 

![](https://github.com/Leega1020/p.leaguer/blob/main/Architecture_diagram/System_architecture.png)

## ERD 

![](Architecture diagram/ERD.png)

## 程式結構

- **app.py:** 主程式檔案，包含 Flask 應用程式的設定和路由
- **gameBot.py:** 資料更新的定時任務
- **templates/:** 存放 HTML 模板檔案
- **static/:** 存放靜態檔案，如圖片、CSS 和 JavaScript 檔案
- **requirements.txt:** 列出專案相依套件的清單

## 聯絡方式

- **作者:** CHIA-HSIN, LEE (李嘉欣)
- **郵件:** donnnnaaa1020@gmail.com
- **履歷:** [Google Drive Resume](https://drive.google.com/drive/u/0/folders/1Ng5i-rrHscPjuw5N2tLLQg059NtJ9nA4)

