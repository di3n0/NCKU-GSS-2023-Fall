### 計畫說明
數位產業署沙崙資安服務基地(以下簡稱沙崙基地)為挖掘資安新秀、培育產業所需資安人才，  
協同資安企業以「企業出專題、學生來解題」形式，鼓勵大專校院學生投入資安專題實作，  
為資安產業培植新血、預約潛力人才。  
說明頁面：https://www.acwsouth.org/event/cybersec-star-2023    

### 智慧安全會議室管理系統
智慧物聯網、其他跨領域資安情境
<img width="800" height="400" src="https://github.com/SmallliDinosaur/NCKU-GSS-2023-Fall/blob/main/picture/Meet.png"/>
  
<img width="800" height="400" src="https://github.com/SmallliDinosaur/NCKU-GSS-2023-Fall/blob/main/picture/%E5%AD%B8%E7%BF%92%E6%B5%81%E7%A8%8B.PNG"/>
  
<img width="800" height="400" src="https://github.com/SmallliDinosaur/NCKU-GSS-2023-Fall/blob/main/picture/%E6%92%B0%E5%AF%AB%E6%AA%94%E6%A1%88.PNG"/>
  
<img width="800" height="400" src="https://github.com/SmallliDinosaur/NCKU-GSS-2023-Fall/blob/main/picture/%E6%A8%B9%E8%8E%93%E6%B4%BE%E8%88%87%E9%9B%B2%E7%9A%84%E6%87%89%E7%94%A8.PNG"/>

<img width="800" height="400" src="https://github.com/SmallliDinosaur/NCKU-GSS-2023-Fall/blob/main/picture/%E5%AF%A6%E9%AB%94%E5%B1%95%E7%A4%BA.PNG"/>

  
#### 第一次相見
<img width="800" src="https://github.com/SmallliDinosaur/NCKU-GSS-2023-Fall/blob/main/picture/20230908%20meeting.jpg"/>

  
#### 固定時間開會
<img width="800" src="https://github.com/SmallliDinosaur/NCKU-GSS-2023-Fall/blob/main/picture/20230921meeting.jpg"/>

#### 企業參訪
<img width="800" height="400" src="https://github.com/SmallliDinosaur/NCKU-GSS-2023-Fall/blob/main/picture/20231026_GSS%E5%8F%83%E8%A8%AA.jpg"/>

<br/>
<br/>

### ZAP
<img width="800" height="400" src="https://github.com/SmallliDinosaur/NCKU-GSS-2023-Fall/blob/main/picture/ZAP.PNG"/>

#### High
**SQL 注入 - SQLite**
https://xxxxxx.azurewebsites.net/meeting/register/  
解：.clean 輸入  

#### Medium
**Content Security Policy (CSP) Header Not Set**
```python
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src https://*; child-src 'none';">  
@csp_update(SCRIPT_SRC="'self'")  
Debug=False  

CSP_DEFAULT_SRC = ("'self'",)  
CSP_IMG_SRC = ("'none'",)  
CSP_CHILD_SRC = ("'none'",)  
CSP_FRAME_ANCESTORS = ("'self'",)  
CSP_FORM_ACTION = ("'self'",)  
```

<br/>

**CSP: Wildcard Directive**
```python
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self'; child-src 'none'; form-action 'self';">  
```

<br/>
<br/>
<br/>

### Checkmarx （達到 0 漏洞檢出）
<img width="800" height="400" src="https://github.com/SmallliDinosaur/NCKU-GSS-2023-Fall/blob/main/picture/Checkmarx.PNG"/>

#### High
- Vulnerable packages

#### Medium
- Vulnerable packages
- Parameter_Tampering
- CSRF
- DB_Parameter_Tampering

<br/>
<br/>
<br/>

### 安全的措施
**註冊密碼**
大寫、小寫、特殊字元、至少10碼
  
**API Authentication**
使用者名稱和密碼傳送到伺服器，伺服器解碼後進行驗證。


