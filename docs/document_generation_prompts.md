# Document Generation Prompts for Context Windows Lab

## Overview

This document contains detailed prompts for generating all documents needed for the Context Windows Lab experiments. The primary focus is on **20 Hebrew documents** required for Experiment 3 (RAG Impact), which tests Retrieval-Augmented Generation performance.

### Why We Need These Documents

**Current Problem**:
- All documents are currently generated synthetically in-memory at runtime
- No persistent document corpus in the codebase
- Difficult to inspect and verify what data is being fed to the LLM
- Assignment requires specific Hebrew documents for Experiment 3

**Solution**:
- Generate 20 high-quality Hebrew documents across 3 domains (Technology, Law, Medicine)
- Store them persistently in the codebase at `data/raw/hebrew_documents/`
- Enable inspection, version control, and reproducibility
- Meet assignment requirements explicitly stated in context-windows-lab.pdf

### Assignment Requirements

From `context-windows-lab.pdf` (Experiment 3):
> **Data**: מאגר של 20 מסמכים בעברית (נושאים: טכנולוגיה, משפט, רפואה)
>
> Translation: "A repository of 20 documents in Hebrew (topics: technology, law, medicine)"

### Document Specifications

- **Total Documents**: 20
- **Language**: Hebrew (עברית)
- **Length**: 500-700 words each
- **Format**: Plain text (.txt files, UTF-8 encoding)
- **Domains**:
  - Technology (7 documents)
  - Law (7 documents)
  - Medicine (6 documents)

---

## Document Organization

### Directory Structure

```
data/
├── raw/
│   └── hebrew_documents/
│       ├── technology/           # 7 documents
│       │   ├── ai_machine_learning.txt
│       │   ├── cybersecurity.txt
│       │   ├── cloud_computing.txt
│       │   ├── iot.txt
│       │   ├── blockchain.txt
│       │   ├── software_dev.txt
│       │   └── mobile_apps.txt
│       ├── law/                  # 7 documents
│       │   ├── contract_law.txt
│       │   ├── intellectual_property.txt
│       │   ├── privacy_law.txt
│       │   ├── employment_law.txt
│       │   ├── corporate_law.txt
│       │   ├── consumer_protection.txt
│       │   └── digital_rights.txt
│       ├── medicine/              # 6 documents
│       │   ├── cardiology.txt
│       │   ├── neurology.txt
│       │   ├── pharmacology.txt
│       │   ├── diabetes.txt
│       │   ├── mental_health.txt
│       │   └── preventive_medicine.txt
│       └── metadata.json          # Document metadata
└── README.md                      # Data documentation
```

---

## Technology Domain (7 Documents)

### Document 1: Artificial Intelligence and Machine Learning

**Filename**: `data/raw/hebrew_documents/technology/ai_machine_learning.txt`
**Word Count**: 500-700 words
**Topic**: בינה מלאכותית ולמידת מכונה

**Prompt**:
```
כתוב מאמר מקיף בן 600-700 מילים בעברית על בינה מלאכותית ולמידת מכונה.

כלול את הנושאים הבאים:
1. **מושגי יסוד**: הגדרה של בינה מלאכותית (AI) ולמידת מכונה (Machine Learning), ההבדלים ביניהם
2. **סוגי למידה**: למידה מפוקחת (Supervised), למידה לא מפוקחת (Unsupervised), למידת חיזוק (Reinforcement Learning)
3. **יישומים בתעשייה**:
   - רכב אוטונומי
   - זיהוי פנים וזיהוי תמונות
   - עיבוד שפה טבעית (NLP)
   - מערכות המלצה
   - אבחון רפואי
4. **אתגרים טכניים**: דאטה איכותי, כוח חישוב, הסבירות מודלים (Explainability)
5. **אתגרים אתיים**: הטיה באלגוריתמים, פרטיות, שקיפות, אחריות
6. **מגמות עתידיות**: GPT ומודלים גדולים, AI גנרטיבי, AutoML

**הנחיות כתיבה**:
- כתוב בעברית טבעית ושוטפת (לא תרגום מילולי מאנגלית)
- השתמש במינוחים טכניים נכונים בעברית (אך הוסף מינוח אנגלי בסוגריים בפעם הראשונה)
- צור טקסט אינפורמטיבי, מקצועי ומובנה
- חלק לפסקאות ברורות עם זרימה הגיונית
- התחל בפסקת פתיחה מושכת
- סיים במסקנה או מבט לעתיד
```

---

### Document 2: Cybersecurity and Data Protection

**Filename**: `data/raw/hebrew_documents/technology/cybersecurity.txt`
**Word Count**: 500-700 words
**Topic**: אבטחת סייבר והגנת מידע

**Prompt**:
```
כתוב מאמר מקיף בן 600-700 מילים בעברית על אבטחת סייבר והגנת מידע.

כלול את הנושאים הבאים:
1. **חשיבות אבטחת סייבר**: סיכונים בעידן הדיגיטלי, התקפות סייבר מתוחכמות
2. **סוגי איומים עיקריים**:
   - תוכנות זדוניות (Malware, Ransomware)
   - פישינג (Phishing) והנדסה חברתית
   - התקפות DDoS
   - פריצות למאגרי מידע
3. **שכבות הגנה**:
   - חומות אש (Firewalls)
   - הצפנה (Encryption)
   - אימות דו-שלבי (2FA)
   - ניטור וזיהוי פעילות חריגה
4. **הגנת מידע אישי**: חוק הגנת הפרטיות, GDPR, זכויות המשתמש
5. **אבטחה ארגונית**: מדיניות אבטחה, הדרכת עובדים, ניהול סיכונים
6. **טכנולוגיות חדשות**: AI בזיהוי איומים, Zero Trust Architecture, Blockchain

**הנחיות כתיבה**:
- כתוב בעברית מקצועית וברורה
- השתמש בדוגמאות ממשיות של התקפות ידועות
- הסבר מושגים טכניים באופן מובן גם לקורא לא מומחה
- צור תחושת דחיפות ומודעות לחשיבות הנושא
```

---

### Document 3: Cloud Computing and Infrastructure

**Filename**: `data/raw/hebrew_documents/technology/cloud_computing.txt`
**Word Count**: 500-700 words
**Topic**: מחשוב ענן ותשתיות

**Prompt**:
```
כתוב מאמר מקיף בן 600-700 מילים בעברית על מחשוב ענן ותשתיות.

כלול את הנושאים הבאים:
1. **מהו מחשוב ענן**: הגדרה, עקרונות יסוד, מעבר מ-On-Premise לענן
2. **מודלי שירות**:
   - IaaS (Infrastructure as a Service) - תשתית כשירות
   - PaaS (Platform as a Service) - פלטפורמה כשירות
   - SaaS (Software as a Service) - תוכנה כשירות
3. **סוגי פריסה**:
   - ענן ציבורי (Public Cloud)
   - ענן פרטי (Private Cloud)
   - ענן היברידי (Hybrid Cloud)
4. **ספקי ענן מובילים**: AWS, Azure, Google Cloud - השוואה והבדלים
5. **יתרונות**: גמישות, חסכון, זמינות גבוהה, קנה מידה (Scalability)
6. **אתגרים**: אבטחה, תלות בספק, עלויות נסתרות, ציות רגולטורי
7. **מגמות עתידיות**: Serverless, Edge Computing, Multi-Cloud

**הנחיות כתיבה**:
- כתוב בצורה מאוזנת שמציגה גם יתרונות וגם אתגרים
- השתמש באנלוגיות להמחשת מושגים מורכבים
- הוסף דוגמאות שימוש ממשיות מתחומים שונים
```

---

### Document 4: Internet of Things (IoT)

**Filename**: `data/raw/hebrew_documents/technology/iot.txt`
**Word Count**: 500-700 words
**Topic**: אינטרנט של הדברים (IoT)

**Prompt**:
```
כתוב מאמר מקיף בן 600-700 מילים בעברית על אינטרנט הדברים (Internet of Things - IoT).

כלול את הנושאים הבאים:
1. **מהו IoT**: הגדרה, התפתחות היסטורית, חזון העתיד
2. **רכיבי מערכת IoT**:
   - חיישנים (Sensors)
   - קישוריות (Connectivity) - WiFi, Bluetooth, 5G
   - עיבוד נתונים (Data Processing)
   - ממשק משתמש (User Interface)
3. **תחומי יישום**:
   - בית חכם (Smart Home)
   - ערים חכמות (Smart Cities)
   - תעשייה 4.0 (Industrial IoT)
   - חקלאות חכמה
   - בריאות דיגיטלית (Healthcare IoT)
4. **אתגרים טכניים**: צריכת אנרגיה, רוחב פס, תאימות פרוטוקולים
5. **אתגרי אבטחה**: התקני IoT כנקודת חדירה, פרטיות, עדכוני אבטחה
6. **עתיד ה-IoT**: 5G, AI בקצה (Edge AI), סטנדרטיזציה

**הנחיות כתיבה**:
- התמקד בדוגמאות מעשיות שהקורא מכיר
- הסבר איך IoT משפיע על חיי היומיום
- שמור על איזון בין אופטימיות טכנולוגית לחששות אבטחה
```

---

### Document 5: Blockchain and Cryptocurrencies

**Filename**: `data/raw/hebrew_documents/technology/blockchain.txt`
**Word Count**: 500-700 words
**Topic**: בלוקצ'יין ומטבעות קריפטוגרפיים

**Prompt**:
```
כתוב מאמר מקיף בן 600-700 מילים בעברית על טכנולוגיית הבלוקצ'יין ומטבעות קריפטוגרפיים.

כלול את הנושאים הבאים:
1. **מהו בלוקצ'יין**: מבנה הבלוק, שרשרת, ביזור (Decentralization), שקיפות
2. **עקרונות טכניים**:
   - הצפנה קריפטוגרפית
   - הוכחת עבודה (Proof of Work)
   - קונצנזוס מבוזר
   - אי-הפיכות (Immutability)
3. **מטבעות קריפטוגרפיים**: ביטקוין, אתריום, הבדלים ביניהם
4. **יישומים מעבר למטבעות**:
   - חוזים חכמים (Smart Contracts)
   - ניהול שרשרת האספקה
   - זהות דיגיטלית
   - מערכות הצבעה
5. **יתרונות**: שקיפות, אבטחה, חוסר צורך בצד שלישי
6. **אתגרים וביקורת**: צריכת אנרגיה, מדרגיות, רגולציה, תנודתיות
7. **עתיד הבלוקצ'יין**: Web3, DeFi, NFTs, יישומים ארגוניים

**הנחיות כתיבה**:
- הסבר מושגים טכניים מורכבים בפשטות
- הצג תמונה מאוזנת של התקווה והביקורת
- הימנע מקידום או התנגדות נחרצת - שמור על אובייקטיביות
```

---

### Document 6: Software Development Methodologies

**Filename**: `data/raw/hebrew_documents/technology/software_dev.txt`
**Word Count**: 500-700 words
**Topic**: מתודולוגיות פיתוח תוכנה

**Prompt**:
```
כתוב מאמר מקיף בן 600-700 מילים בעברית על מתודולוגיות פיתוח תוכנה.

כלול את הנושאים הבאים:
1. **מבוא**: חשיבות המתודולוגיה בפיתוח תוכנה, התפתחות לאורך השנים
2. **מתודולוגיות מסורתיות**:
   - Waterfall (מפל): שלבים ברצף, תיעוד מפורט, מתאים לפרויקטים יציבים
   - Spiral: ניהול סיכונים, אב-טיפוס
3. **מתודולוגיות זריזות (Agile)**:
   - Scrum: ספרינטים, תפקידים (Product Owner, Scrum Master), טקסים יומיים
   - Kanban: לוח משימות, זרימה רציפה, WIP מוגבל
   - XP (Extreme Programming): Pair Programming, TDD, רפקטורינג
4. **DevOps**: אינטגרציה בין פיתוח ותפעול, CI/CD, אוטומציה
5. **בחירת מתודולוגיה**: גודל צוות, סוג פרויקט, דרישות לקוח, תרבות ארגונית
6. **מגמות עתידיות**: Remote-First, Platform Engineering, GitOps

**הנחיות כתיבה**:
- הסבר את היתרונות והחסרונות של כל מתודולוגיה
- השתמש בדוגמאות מעשיות מפרויקטים אמיתיים
- הדגש שאין פתרון אחד שמתאים לכולם
```

---

### Document 7: Mobile Applications and Development

**Filename**: `data/raw/hebrew_documents/technology/mobile_apps.txt`
**Word Count**: 500-700 words
**Topic**: אפליקציות ופיתוח מובייל

**Prompt**:
```
כתוב מאמר מקיף בן 600-700 מילים בעברית על פיתוח אפליקציות מובייל.

כלול את הנושאים הבאים:
1. **מבוא**: מהפכת הסמארטפון, חשיבות אפליקציות בחיינו
2. **פלטפורמות**:
   - iOS (Swift, SwiftUI)
   - Android (Kotlin, Jetpack Compose)
   - השוואה בין הפלטפורמות
3. **גישות פיתוח**:
   - Native: ביצועים מירביים, גישה מלאה ל-API
   - Cross-Platform: React Native, Flutter, Xamarin
   - Web Apps: Progressive Web Apps (PWA)
4. **אתגרים בפיתוח מובייל**:
   - גדלי מסך שונים
   - ביצועים וצריכת סוללה
   - קישוריות לא יציבה
   - אבטחת מידע במכשיר
5. **UX/UI במובייל**: עיצוב לנגיעה, ניווט פשוט, נגישות
6. **פרסום והפצה**: App Store, Google Play, תהליכי אישור, מודלים מוניטרים
7. **מגמות**: 5G, AR/VR במובייל, Super Apps, On-Device AI

**הנחיות כתיבה**:
- הסבר הבדלים טכניים בצורה מובנת
- הוסף דוגמאות של אפליקציות מצליחות
- דון בשיקולים עסקיים ולא רק טכניים
```

---

## Law Domain (7 Documents)

### Document 8: Contract Law Fundamentals

**Filename**: `data/raw/hebrew_documents/law/contract_law.txt`
**Word Count**: 500-700 words
**Topic**: יסודות דיני חוזים

**Prompt**:
```
כתוב מאמר משפטי מקיף בן 600-700 מילים בעברית על יסודות דיני חוזים.

כלול את הנושאים הבאים:
1. **הגדרת חוזה**: הסכם משפטי מחייב, יסודות החוזה בדין הישראלי
2. **רכיבי חוזה תקף**:
   - הצעה (Offer) - מפורטת וברורה
   - קבלה (Acceptance) - מלאה וללא תנאי
   - תמורה (Consideration) - ערך כלכלי
   - כוונה משפטית (Intention) - יצירת יחסים משפטיים
   - כשרות משפטית - גיל, שפיות
3. **סוגי חוזים**:
   - בכתב ובעל פה
   - חוזים אחידים וחוזים אישיים
   - חוזה מפורש וחוזה משתמע
4. **פרשנות חוזים**: כוונת הצדדים, תום לב, דרכי פרשנות
5. **הפרת חוזה**:
   - הפרה יסודית ורגילה
   - סעדים: פיצויים, ביטול, ביצוע בעין
   - נזיקין חוזיים
6. **חוזים בעידן הדיגיטלי**: חוזים אלקטרוניים, תנאי שימוש, חתימה דיגיטלית

**הנחיות כתיבה**:
- כתוב בעברית משפטית מקצועית אך מובנת
- השתמש במינוחים משפטיים מדויקים
- הוסף דוגמאות ממקרים אמיתיים (ללא פרטים מזהים)
- צור טקסט מובנה עם ממשקים ברורים בין הנושאים
```

---

### Document 9: Intellectual Property Rights

**Filename**: `data/raw/hebrew_documents/law/intellectual_property.txt`
**Word Count**: 500-700 words
**Topic**: קניין רוחני וזכויות יוצרים

**Prompt**:
```
כתוב מאמר משפטי מקיף בן 600-700 מילים בעברית על קניין רוחני וזכויות יוצרים.

כלול את הנושאים הבאים:
1. **מהו קניין רוחני**: הגדרה, חשיבות כלכלית, עקרונות יסוד
2. **סוגי הגנה על קניין רוחני**:
   - **זכויות יוצרים (Copyright)**: יצירות ספרותיות, אמנותיות, תוכנה
   - **פטנטים (Patents)**: המצאות טכנולוגיות, תהליך הרישום
   - **סימני מסחר (Trademarks)**: לוגו, שמות מותגים, הגנה
   - **סודות מסחריים (Trade Secrets)**: נוסחאות, תהליכים
3. **היקף ההגנה**: תקופת הגנה, זכויות בעל הקניין, שימוש הוגן
4. **הפרת קניין רוחני**: העתקה, שימוש לא מורשה, פיראטיות, אכיפה
5. **קניין רוחני בעידן הדיגיטלי**:
   - AI וזכויות יוצרים
   - NFTs וקניין דיגיטלי
   - Open Source ורישוי
6. **דין בינלאומי**: WIPO, אמנות בינלאומיות, אכיפה חוצת גבולות

**הנחיות כתיבה**:
- הסבר מושגים משפטיים במונחים נגישים
- הדגש את המתח בין חדשנות להגנה
- הוסף דוגמאות של מקרים מפורסמים (Apple vs Samsung, וכד')
```

---

### Document 10: Privacy and Data Protection Law

**Filename**: `data/raw/hebrew_documents/law/privacy_law.txt`
**Word Count**: 500-700 words
**Topic**: דיני פרטיות והגנת מידע

**Prompt**:
```
כתוב מאמר משפטי מקיף בן 600-700 מילים בעברית על דיני פרטיות והגנת מידע.

כלול את הנושאים הבאים:
1. **הזכות לפרטיות**: זכות יסוד, התפתחות היסטורית, היקף ההגנה
2. **חוק הגנת הפרטיות בישראל**:
   - עקרונות יסוד
   - מאגרי מידע ורישום
   - זכויות הפרט: עיון, תיקון, מחיקה
   - רשות הגנת הפרטיות
3. **GDPR (האיחוד האירופי)**:
   - תחולה על חברות ישראליות
   - עקרונות: הסכמה, מינימיזציה, שקיפות
   - Right to be Forgotten
   - קנסות והשלכות
4. **איסוף ושימוש במידע**:
   - הסכמה מדעת (Informed Consent)
   - מטרות לגיטימיות
   - אבטחת מידע
5. **אתגרים בעידן הדיגיטלי**:
   - Big Data וניתוח נתונים
   - פרופיילינג אלגוריתמי
   - מעקב מקוון
   - זיהוי ביומטרי
6. **אכיפה**: תלונות, חקירות, עונשים

**הנחיות כתיבה**:
- הדגש את האיזון בין פרטיות לבין אינטרסים לגיטימיים
- השתמש בדוגמאות מהחדשות (פייסבוק-קיימברידג' אנליטיקה, וכד')
- הסבר איך הדין משפיע על משתמשים וחברות
```

---

### Document 11: Employment Law

**Filename**: `data/raw/hebrew_documents/law/employment_law.txt`
**Word Count**: 500-700 words
**Topic**: דיני עבודה

**Prompt**:
```
כתוב מאמר משפטי מקיף בן 600-700 מילים בעברית על דיני עבודה בישראל.

כלול את הנושאים הבאים:
1. **יסודות דיני עבודה**: יחסי עובד-מעביד, חוזה עבודה, דין קוגנטי
2. **זכויות עובדים בסיסיות**:
   - שכר מינימום
   - שעות עבודה ושעות נוספות
   - ימי חופשה, מחלה, חגים
   - דמי הבראה ופנסיה
   - גמול שעת הודעה
3. **סיום יחסי עבודה**:
   - התפטרות מרצון
   - פיטורים - סיבות מוצדקות, הליך הוגן
   - פיצויי פיטורים
   - הודעה מוקדמת
4. **איסור אפליה**: מגדר, גזע, דת, גיל, נכות, נטייה מינית
5. **הגנת עובדים**:
   - התאגדות ואיגודים מקצועיים
   - הסכמים קיבוציים
   - ארגונים להגנה: משרד העבודה, בית דין לעבודה
6. **מגמות עכשוויות**:
   - עבודה מרחוק וזכויות
   - כלכלת ה-Gig (עובדים עצמאיים)
   - הטרדה מינית במקום העבודה

**הנחיות כתיבה**:
- כתוב בצורה מאוזנת המשקפת את זכויות שני הצדדים
- הוסף דוגמאות של מקרים נפוצים
- הדגש את המשמעויות המעשיות עבור עובדים ומעסיקים
```

---

### Document 12: Corporate Law and Governance

**Filename**: `data/raw/hebrew_documents/law/corporate_law.txt`
**Word Count**: 500-700 words
**Topic**: דיני חברות וממשל תאגידי

**Prompt**:
```
כתוב מאמר משפטי מקיף בן 600-700 מילים בעברית על דיני חברות וממשל תאגידי.

כלול את הנושאים הבאים:
1. **סוגי חברות בישראל**:
   - חברה בע"מ (בערבון מוגבל)
   - חברה פרטית וחברה ציבורית
   - עמותות וחל"צ (חברה לתועלת הציבור)
2. **הקמת חברה**:
   - רישום ותקנון
   - הון מניות
   - אורגנים: אסיפה כללית, דירקטוריון, מנכ"ל
3. **ממשל תאגידי (Corporate Governance)**:
   - חובות אמון של דירקטורים
   - ניגוד עניינים
   - שקיפות ודיווח
   - בקרה פנימית
4. **זכויות בעלי מניות**:
   - זכות הצבעה
   - זכות מידע
   - תביעות נגזרות
5. **עסקאות מיוחדות**:
   - עסקאות עם בעלי עניין
   - מיזוגים ורכישות (M&A)
   - הנפקה לציבור (IPO)
6. **חדלות פירעון**: פירוק חברה, כינוס נכסים, הגנה על נושים

**הנחיות כתיבה**:
- הסבר את המבנה התאגידי בצורה ברורה
- התמקד בעקרונות המרכזיים של ממשל תאגידי
- הדגש את החשיבות של אחריות תאגידית
```

---

### Document 13: Consumer Protection

**Filename**: `data/raw/hebrew_documents/law/consumer_protection.txt`
**Word Count**: 500-700 words
**Topic**: הגנת הצרכן

**Prompt**:
```
כתוב מאמר משפטי מקיף בן 600-700 מילים בעברית על חוק הגנת הצרכן בישראל.

כלול את הנושאים הבאים:
1. **מטרת החוק**: איזון כוחות בין צרכן לעוסק, הגנה על הצד החלש
2. **זכויות הצרכן**:
   - זכות לקבל מידע מלא ונכון
   - זכות לביטול עסקה (14 יום)
   - זכות לשירות הוגן
   - זכות לפיצוי בגין מוצר פגום
3. **חובות עוסק**:
   - מתן מידע מדויק
   - איסור פרסומת מטעה
   - איסור תניות גורפות
   - שירות לקוחות הולם
4. **אחריות למוצרים**:
   - תקופת אחריות
   - תיקון, החלפה, או החזר כספי
   - מוצרים פגומים ומסוכנים
5. **רכישות מקוונות**:
   - אתרי מסחר אלקטרוני
   - משלוחים והחזרות
   - תשלומים מאובטחים
6. **אכיפה וסעדים**:
   - רשות הגנת הצרכן
   - תביעות קטנות
   - פיצויים וסנקציות

**הנחיות כתיבה**:
- כתוב בצורה נגישה שמסבירה זכויות בפועל
- הוסף דוגמאות של מצבים יומיומיים
- הדגש מתי וכיצד ניתן לפעול
```

---

### Document 14: Digital Rights and Cyber Law

**Filename**: `data/raw/hebrew_documents/law/digital_rights.txt`
**Word Count**: 500-700 words
**Topic**: זכויות דיגיטליות ודיני סייבר

**Prompt**:
```
כתוב מאמר משפטי מקיף בן 600-700 מילים בעברית על זכויות דיגיטליות ודיני סייבר.

כלול את הנושאים הבאים:
1. **מבוא**: המרחב הדיגיטלי כזירה משפטית, אתגרים ייחודיים
2. **חופש הביטוי ברשת**:
   - זכויות וגבולות
   - תוכן פוגעני ולשון הרע
   - צנזורה ומחיקת תוכן
   - אחריות פלטפורמות
3. **פשעי סייבר**:
   - פריצה למחשבים
   - מעילה במידע
   - הונאות מקוונות
   - הטרדה ברשת
4. **זכות לשכחה (Right to be Forgotten)**:
   - מחיקת תוכן מנועי חיפוש
   - איזון בין פרטיות לבין חופש המידע
5. **חוזים דיגיטליים**:
   - תוקף משפטי של חתימה אלקטרונית
   - תנאי שימוש באתרים
   - רכישות מקוונות
6. **שיפוט בינלאומי**:
   - שיפוט חוצה גבולות
   - אכיפה בעולם הדיגיטלי
   - סמכות שיפוט

**הנחיות כתיבה**:
- הדגש את הדילמות המשפטיות הייחודיות לעידן הדיגיטלי
- הוסף דוגמאות של פסקי דין מנחים
- דון באתגרים של רגולציה במרחב גלובלי
```

---

## Medicine Domain (6 Documents)

### Document 15: Cardiology and Heart Disease

**Filename**: `data/raw/hebrew_documents/medicine/cardiology.txt`
**Word Count**: 500-700 words
**Topic**: קרדיולוגיה ומחלות לב

**Prompt**:
```
כתוב מאמר רפואי מקיף בן 600-700 מילים בעברית על קרדיולוגיה ומחלות לב.

כלול את הנושאים הבאים:
1. **מערכת הלב וכלי הדם**:
   - מבנה הלב: חדרים, עליות, מסתמים
   - מחזור הדם: מחזור ריאתי ומחזור גופי
   - תפקיד הלב כמשאבה
2. **מחלות לב נפוצות**:
   - **מחלת עורקים כליליים (CAD)**: היצרות, טרשת עורקים
   - **אוטם שריר הלב**: סימפטומים, טיפול דחוף
   - **יתר לחץ דם**: סיבות, סיבוכים, טיפול
   - **הפרעות קצב (Arrhythmias)**: פרפור פרוזדורים, טכיקרדיה
   - **אי ספיקת לב**: סוגים, תסמינים, טיפול
3. **גורמי סיכון**:
   - עישון
   - כולסטרול גבוה
   - סוכרת
   - השמנת יתר
   - חוסר פעילות גופנית
   - גנטיקה
4. **אבחון**:
   - בדיקת אק"ג (ECG)
   - אקו לב (Echocardiography)
   - מבחני מאמץ
   - צנתור לבבי
5. **טיפולים**:
   - תרופות: סטטינים, נוגדי קרישה, חוסמי בטא
   - ניתוחים: מעקפים, החלפת מסתמים
   - התערבויות: סטנטים, קוצב לב
6. **מניעה**: תזונה, פעילות גופנית, ניהול מתח

**הנחיות כתיבה**:
- כתוב בעברית רפואית מקצועית אך מובנת לקורא מדע-פופולרי
- השתמש במינוחים רפואיים נכונים (עם תרגום לעברית יומיומית בסוגריים)
- הדגש את החשיבות של מניעה וגילוי מוקדם
- צור טקסט אינפורמטיבי ועובדתי
```

---

### Document 16: Neurology and Brain Health

**Filename**: `data/raw/hebrew_documents/medicine/neurology.txt`
**Word Count**: 500-700 words
**Topic**: נוירולוגיה ובריאות המוח

**Prompt**:
```
כתוב מאמר רפואי מקיף בן 600-700 מילים בעברית על נוירולוגיה ובריאות המוח.

כלול את הנושאים הבאים:
1. **מערכת העצבים**:
   - מבנה המוח: חומר אפור, חומר לבן, אזורי המוח
   - תפקידי המוח: חשיבה, רגש, תנועה, חושים
   - מערכת העצבים ההיקפית
2. **מחלות נוירולוגיות נפוצות**:
   - **שבץ מוחי (Stroke)**: איסכמי והמורגי, זמן-מוח
   - **אפילפסיה**: התקפים, סוגים, טיפול
   - **מיגרנה**: מנגנון, טריגרים, טיפול
   - **טרשת נפוצה (MS)**: מחלה אוטואימונית, תסמינים
   - **פרקינסון**: ניוון, רעד, נוקשות
   - **אלצהיימר**: דמנציה, ירידה קוגניטיבית
3. **תסמינים נוירולוגיים**:
   - כאבי ראש
   - חולשה או חוסר תחושה
   - סחרחורת
   - בעיות זיכרון
4. **אבחון**:
   - MRI, CT מוחי
   - אלקטרואנצפלוגרם (EEG)
   - בדיקות נוירולוגיות
5. **טיפולים**:
   - תרופות
   - נוירוכירורגיה
   - שיקום נוירולוגי
   - טיפולים חדשניים
6. **שמירה על בריאות המוח**: אורח חיים, תזונה, תרגול קוגניטיבי

**הנחיות כתיבה**:
- הסבר את המורכבות של מערכת העצבים בצורה ברורה
- הדגש את הקשר בין אורח חיים לבריאות המוח
- צור תחושת אמפתיה כלפי חולים נוירולוגיים
```

---

### Document 17: Pharmacology and Drug Development

**Filename**: `data/raw/hebrew_documents/medicine/pharmacology.txt`
**Word Count**: 500-700 words
**Topic**: פרמקולוגיה ופיתוח תרופות

**Prompt**:
```
כתוב מאמר רפואי מקיף בן 600-700 מילים בעברית על פרמקולוגיה ופיתוח תרופות.

כלול את הנושאים הבאים:
1. **מהי פרמקולוגיה**: חקר תרופות, פרמקודינמיקה ופרמקוקינטיקה
2. **מנגנוני פעולה של תרופות**:
   - קולטנים (Receptors)
   - אגוניסטים ואנטגוניסטים
   - אנזימים ותעלות יונים
3. **תהליך פיתוח תרופה**:
   - מחקר בסיסי וזיהוי מטרות
   - מחקר קדם-קליני (in vitro, in vivo)
   - ניסויים קליניים:
     - Phase I: בטיחות
     - Phase II: יעילות ראשונית
     - Phase III: השוואה לטיפול קיים
     - Phase IV: מעקב לאחר אישור
   - רגולציה ואישור: FDA, EMA, משרד הבריאות
4. **סוגי תרופות**:
   - תרופות כימיות קלאסיות
   - ביולוגיות (Biologics)
   - תרופות מותאמות אישית (Personalized Medicine)
   - תרופות גנריות
5. **תופעות לוואי**:
   - מנגנונים
   - פרמקוויגילנס (מעקב אחר תופעות לוואי)
   - איזון תועלת-סיכון
6. **מגמות עתידיות**:
   - AI בגילוי תרופות
   - רפואה מדויקת
   - מודיפיקציות גנטיות

**הנחיות כתיבה**:
- הסבר תהליכים מדעיים מורכבים בפשטות
- הדגש את המורכבות והזמן הנדרש לפיתוח תרופה
- דון באתגרים כלכליים ואתיים
```

---

### Document 18: Diabetes and Metabolic Disorders

**Filename**: `data/raw/hebrew_documents/medicine/diabetes.txt`
**Word Count**: 500-700 words
**Topic**: סוכרת והפרעות מטבוליות

**Prompt**:
```
כתוב מאמר רפואי מקיף בן 600-700 מילים בעברית על סוכרת והפרעות מטבוליות.

כלול את הנושאים הבאים:
1. **מהי סוכרת**: הפרעה ברמות הגלוקוז בדם, תפקיד האינסולין
2. **סוגי סוכרת**:
   - **סוכרת סוג 1**: אוטואימונית, תלות באינסולין, גיל צעיר
   - **סוכרת סוג 2**: עמידות לאינסולין, קשר להשמנה, גיל מבוגר
   - **סוכרת הריון**: במהלך הריון, סיכונים לאם ולעובר
3. **תסמינים**:
   - צמא מוגבר
   - הטלת שתן מרובה
   - עייפות
   - ירידה במשקל (סוג 1)
   - טשטוש ראייה
4. **אבחון**:
   - בדיקת גלוקוז בצום
   - HbA1c (המוגלובין מסוכרר)
   - מבחן סבילות לגלוקוז
5. **סיבוכים**:
   - מחלות לב וכלי דם
   - נוירופתיה (נזק לעצבים)
   - נפרופתיה (נזק לכליות)
   - רטינופתיה (נזק לעיניים)
   - כף רגל סוכרתית
6. **טיפול**:
   - שינויי אורח חיים: תזונה, פעילות גופנית
   - תרופות: מטפורמין, סולפונילאוריאות
   - אינסולין: סוגים, אופן מתן
   - טכנולוגיות: משאבות אינסולין, חיישנים רציפים
7. **מניעה**: שמירה על משקל בריא, תזונה מאוזנת, פעילות גופנית

**הנחיות כתיבה**:
- הדגש את החשיבות של איזון גלוקוז ומניעת סיבוכים
- הסבר את ההבדלים בין סוגי הסוכרת
- צור תחושה של תקווה - ניתן לנהל את המחלה בהצלחה
```

---

### Document 19: Mental Health and Psychiatry

**Filename**: `data/raw/hebrew_documents/medicine/mental_health.txt`
**Word Count**: 500-700 words
**Topic**: בריאות הנפש ופסיכיאטריה

**Prompt**:
```
כתוב מאמר רפואי מקיף בן 600-700 מילים בעברית על בריאות הנפש ופסיכיאטריה.

כלול את הנושאים הבאים:
1. **מהי בריאות נפשית**: הגדרה, ספקטרום, חשיבות
2. **הפרעות נפשיות נפוצות**:
   - **דיכאון**: תסמינים, סוגים, שכיחות
   - **חרדה**: הפרעת חרדה כללית, פאניקה, פוביות
   - **הפרעה דו-קוטבית**: עליות ומורדות במצב הרוח
   - **סכיזופרניה**: פסיכוזה, הזיות, תחושות הזויות
   - **PTSD**: הפרעת דחק פוסט-טראומטית
   - **OCD**: הפרעה טורדנית-כפייתית
3. **גורמי סיכון**:
   - גנטיקה
   - טראומה וחוויות ילדות
   - מתח כרוני
   - חוסר תמיכה חברתית
   - שימוש בחומרים ממכרים
4. **סטיגמה ומודעות**: הסרת סטיגמה, חשיבות הטיפול, חינוך
5. **אבחון וטיפול**:
   - שיחה קלינית ואבחנה
   - טיפולים פסיכולוגיים: CBT, פסיכותרפיה
   - תרופות: נוגדי דיכאון, נוגדי חרדה, מייצבי מצב רוח
   - טיפול משולב
   - אשפוז פסיכיאטרי (במקרים חמורים)
6. **שמירה על בריאות נפשית**:
   - מיינדפולנס ומדיטציה
   - קשרים חברתיים
   - פעילות גופנית
   - שינה תקינה
   - חיפוש עזרה מקצועית

**הנחיות כתיבה**:
- כתוב בצורה אמפתית וללא שיפוטיות
- הסר סטיגמה על ידי הצגה של מחלות נפש כמחלות רפואיות לגיטימיות
- הדגש שיש טיפולים זמינים ויעילים
- עודד חיפוש עזרה מקצועית
```

---

### Document 20: Preventive Medicine and Public Health

**Filename**: `data/raw/hebrew_documents/medicine/preventive_medicine.txt`
**Word Count**: 500-700 words
**Topic**: רפואה מניעתית ובריאות הציבור

**Prompt**:
```
כתוב מאמר רפואי מקיף בן 600-700 מילים בעברית על רפואה מניעתית ובריאות הציבור.

כלול את הנושאים הבאים:
1. **מהי רפואה מניעתית**: מניעה על פני טיפול, רמות מניעה
2. **רמות מניעה**:
   - **מניעה ראשונית**: מניעת מחלה (חיסונים, תזונה, פעילות גופנית)
   - **מניעה משנית**: גילוי מוקדם (סקר, בדיקות שגרה)
   - **מניעה שלישית**: מניעת החמרה והשבה לתפקוד
3. **חיסונים**:
   - עקרון הפעולה
   - חיסוני ילדות: חצבת, אדמת, חזרת, פוליו
   - חיסוני מבוגרים: שפעת, COVID-19
   - חסינות עדר
4. **סקר וגילוי מוקדם**:
   - ממוגרפיה (סרטן שד)
   - קולונוסקופיה (סרטן מעי גס)
   - בדיקות דם שגרתיות
   - מדידת לחץ דם
5. **אורח חיים בריא**:
   - **תזונה**: דיאטה מאוזנת, ירקות ופירות
   - **פעילות גופנית**: 150 דקות שבועיות, חוזק שרירים
   - **הפסקת עישון**: הסיכונים והיתרונות
   - **הפחתת אלכוהול**: צריכה מתונה
   - **ניהול מתח**: טכניקות רגיעה
6. **בריאות הציבור**:
   - אפידמיולוגיה ומעקב אחר מחלות
   - תוכניות לאומיות: חיסונים, סקר
   - חינוך לבריאות
   - מדיניות בריאות: חוקי עישון, מיסוי סוכר
7. **מגמות עתידיות**: רפואה מותאמת אישית, Big Data, בינה מלאכותית

**הנחיות כתיבה**:
- הדגש את החסכון הכלכלי והאנושי של מניעה
- צור תחושת אחריות אישית לבריאות
- הסבר איך בריאות הציבור משפיעה על כולנו
- עודד גישה יזומה לבריאות
```

---

## Metadata Schema

Create `data/raw/hebrew_documents/metadata.json` with the following structure:

```json
{
  "collection_name": "Hebrew Documents for Context Windows Lab - Experiment 3",
  "language": "hebrew",
  "total_documents": 20,
  "created_date": "2025-12-10",
  "encoding": "UTF-8",
  "purpose": "RAG Impact experiment - comparing full context vs retrieval-based methods",
  "documents": [
    {
      "id": "tech_001",
      "filename": "ai_machine_learning.txt",
      "domain": "technology",
      "topic": "Artificial Intelligence and Machine Learning",
      "topic_hebrew": "בינה מלאכותית ולמידת מכונה",
      "language": "hebrew",
      "word_count": 650,
      "created": "2025-12-10",
      "key_terms": [
        "בינה מלאכותית",
        "למידת מכונה",
        "אלגוריתמים",
        "רכב אוטונומי",
        "עיבוד שפה טבעית"
      ],
      "summary": "Comprehensive overview of AI and ML concepts, applications, challenges, and future trends"
    },
    {
      "id": "tech_002",
      "filename": "cybersecurity.txt",
      "domain": "technology",
      "topic": "Cybersecurity and Data Protection",
      "topic_hebrew": "אבטחת סייבר והגנת מידע",
      "language": "hebrew",
      "word_count": 630,
      "created": "2025-12-10",
      "key_terms": [
        "אבטחת סייבר",
        "הצפנה",
        "פישינג",
        "חומות אש",
        "הגנת מידע"
      ],
      "summary": "Exploration of cybersecurity threats, defense layers, and modern protection strategies"
    }
    // ... Continue for all 20 documents
  ]
}
```

---

## How to Use These Prompts

### Method 1: Manual Generation (Using Claude or GPT)

1. **Select a prompt** from the sections above (e.g., Document 1: AI and Machine Learning)
2. **Copy the entire Hebrew prompt** (the text inside the code block)
3. **Paste into Claude or ChatGPT**
4. **Save the generated Hebrew text** to the appropriate file:
   - Create directory: `mkdir -p data/raw/hebrew_documents/technology`
   - Save output: `nano data/raw/hebrew_documents/technology/ai_machine_learning.txt`
   - Ensure UTF-8 encoding
5. **Repeat for all 20 documents**
6. **Create metadata.json** with information about each document

### Method 2: Automated Generation Script

Create `scripts/generate_hebrew_documents.py`:

```python
import anthropic
import json
from pathlib import Path

# Load prompts from this file or a JSON
prompts = [
    {
        "id": "tech_001",
        "filename": "ai_machine_learning.txt",
        "domain": "technology",
        "prompt": "כתוב מאמר מקיף בן 600-700 מילים..."
    },
    # ... all 20 prompts
]

# Initialize Claude API
client = anthropic.Anthropic(api_key="your-api-key")

for prompt_config in prompts:
    print(f"Generating {prompt_config['filename']}...")

    # Call Claude API
    response = client.messages.create(
        model="claude-sonnet-4",
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt_config["prompt"]}
        ]
    )

    # Save to file
    output_path = Path(f"data/raw/hebrew_documents/{prompt_config['domain']}/{prompt_config['filename']}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(response.content[0].text, encoding="utf-8")

    print(f"✓ Saved {prompt_config['filename']}")

print("All documents generated successfully!")
```

### Method 3: Using This Repository

Once documents are generated and committed to the repository:

1. **Clone the repository**
2. **Documents are in**: `data/raw/hebrew_documents/`
3. **Load in Experiment 3**:
   ```python
   from pathlib import Path

   def load_hebrew_documents():
       docs_path = Path("data/raw/hebrew_documents")
       documents = []

       for domain_dir in ["technology", "law", "medicine"]:
           domain_path = docs_path / domain_dir
           for txt_file in domain_path.glob("*.txt"):
               content = txt_file.read_text(encoding="utf-8")
               documents.append({
                   "domain": domain_dir,
                   "filename": txt_file.name,
                   "content": content
               })

       return documents
   ```

---

## Verification Checklist

After generating all documents, verify:

- [ ] All 20 documents created
- [ ] UTF-8 encoding (Hebrew displays correctly)
- [ ] Word count between 500-700 words for each document
- [ ] Documents organized in correct directories
- [ ] metadata.json created with all document info
- [ ] Hebrew text is natural (not machine translation)
- [ ] Technical terminology is accurate
- [ ] Documents are informative and well-structured

---

## Benefits of This Approach

1. **Transparency**: All 20 documents visible in codebase
2. **Reproducibility**: Anyone can regenerate using these exact prompts
3. **Version Control**: Documents tracked in git history
4. **Inspection**: Easy to review what data is fed to the LLM
5. **Testing**: Can manually verify RAG retrieval quality
6. **Assignment Compliance**: Meets Hebrew document requirement from PDF
7. **Reusability**: Can use these documents for future experiments

---

## Next Steps

1. **Generate all 20 documents** using prompts above
2. **Create directory structure** (`data/raw/hebrew_documents/...`)
3. **Save each document** as UTF-8 encoded .txt file
4. **Create metadata.json** with document information
5. **Update Experiment 3 code** to load from files instead of generating synthetic
6. **Test RAG retrieval** with real Hebrew documents
7. **Commit to repository** with descriptive commit message
8. **Document in CLAUDE.md** for project tracking

---

## Questions or Issues?

- **Encoding problems**: Ensure all files are UTF-8 encoded
- **Prompt improvements**: Adjust prompts for better quality
- **Additional documents**: Follow same pattern for new docs
- **API costs**: Consider caching generated documents to avoid regeneration

---

**Document Version**: 1.0
**Created**: 2025-12-10
**Author**: Context Windows Lab Team
**Purpose**: Generate comprehensive Hebrew document corpus for Experiment 3
