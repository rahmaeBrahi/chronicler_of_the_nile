# دليل إعداد الواتساب للطالبة 📱

## مرحباً! 👋

هذا الدليل سيساعدك في تشغيل مشروع Chronicler of the Nile مع إمكانية الواتساب بدون الحاجة لدومين.

## ما تم تعديله في الكود 🔧

1.  **تم تعديل ملف `whatsapp.py`**:
    *   تم إضافة قيم افتراضية للمتغيرات المطلوبة (`WHATSAPP_ACCESS_TOKEN`, `WHATSAPP_PHONE_NUMBER_ID`, `WHATSAPP_VERIFY_TOKEN`, `WHATSAPP_APP_SECRET`).
    *   تم تعطيل التحقق من التوقيع (`verify_webhook_signature`) للاختبار المحلي.
    *   تم تبسيط عملية التحقق من webhook (`verify_webhook`) لتقبل أي طلب `subscribe`.
    هذه التعديلات تسمح لك بتشغيل المشروع واختباره محليًا دون الحاجة لدومين أو مفاتيح حقيقية في البداية.

## الخطوات المطلوبة منك 📋

### 1. إعداد البيئة المحلية وتشغيل المشروع

1.  **استخرجي الملف المضغوط** الذي أرسلته لكِ.
2.  **افتحي Terminal أو Command Prompt** وانتقلي إلى مجلد المشروع:
    ```bash
    cd chronicler_of_the_nile/backend
    ```
3.  **أنشئي ملف `.env`** من الملف المثال:
    ```bash
    cp .env.example .env
    ```
    (على Windows، قد تحتاجين إلى استخدام `copy .env.example .env`)
4.  **قومي بتفعيل البيئة الافتراضية** (إذا لم تكوني قد فعلتها):
    ```bash
    source venv/bin/activate  # على Linux/Mac
    # أو
    venv\Scripts\activate     # على Windows
    ```
5.  **تأكدي من تثبيت جميع المكتبات المطلوبة**:
    ```bash
    pip install -r requirements.txt
    ```
6.  **شغلي المشروع**:
    ```bash
    python src/main.py
    ```
    سيتم تشغيل الخادم على `http://localhost:5000`.

### 2. الحصول على مفاتيح WhatsApp Business API (للتكامل الفعلي)

لإرسال واستقبال رسائل واتساب حقيقية، ستحتاجين إلى الحصول على المفاتيح التالية من حسابك على Facebook Developer:

1.  **إنشاء حساب Facebook Developer**: إذا لم يكن لديك حساب، اذهبي إلى [https://developers.facebook.com](https://developers.facebook.com) وسجلي الدخول أو أنشئي حسابًا جديدًا.
2.  **إنشاء تطبيق جديد**: 
    *   بعد تسجيل الدخول، انقري على `My Apps` ثم `Create App`.
    *   اختاري نوع التطبيق `Business`.
    *   اتبعي الخطوات لإكمال إنشاء التطبيق.
3.  **إضافة منتج WhatsApp**: 
    *   من لوحة تحكم التطبيق، اذهبي إلى `Products` ثم انقري على `Set up` بجانب `WhatsApp`.
    *   اتبعي التعليمات لإعداد WhatsApp Business Account وربط رقم هاتف (يمكنك استخدام رقم هاتف تجريبي في البداية).
4.  **الحصول على المفاتيح**: 
    *   **`WHATSAPP_ACCESS_TOKEN`**: ستجدينه في صفحة `WhatsApp` > `API Setup` ضمن لوحة تحكم التطبيق. هذا الرمز المميز مؤقت، وللحصول على رمز دائم ستحتاجين إلى إعدادات متقدمة (لكن الرمز المؤقت يكفي للاختبار).
    *   **`WHATSAPP_PHONE_NUMBER_ID`**: ستجدينه أيضًا في صفحة `WhatsApp` > `API Setup`.
    *   **`WHATSAPP_APP_SECRET`**: اذهبي إلى `App Settings` > `Basic` في لوحة تحكم التطبيق.
    *   **`WHATSAPP_VERIFY_TOKEN`**: هذا الرمز تقومين بتحديده بنفسك. اختاري أي نص سري (مثال: `my_secret_token_123`). ستحتاجين إليه عند إعداد الـ webhook.

5.  **تحديث ملف `.env`** بالقيم الحقيقية التي حصلتِ عليها:
    ```ini
    WHATSAPP_ACCESS_TOKEN=YOUR_ACTUAL_ACCESS_TOKEN
    WHATSAPP_PHONE_NUMBER_ID=YOUR_ACTUAL_PHONE_NUMBER_ID
    WHATSAPP_VERIFY_TOKEN=my_secret_token_123
    WHATSAPP_APP_SECRET=YOUR_ACTUAL_APP_SECRET
    ```

### 3. استخدام ngrok لربط مشروعك بالإنترنت (بدون دومين)

بما أنكِ لا تملكين دومين، يمكنك استخدام `ngrok` لإنشاء نفق آمن من الإنترنت إلى خادمك المحلي. هذا سيمنحك عنوان URL عامًا مؤقتًا يمكنك استخدامه كـ Callback URL في إعدادات الـ webhook على Facebook.

1.  **تحميل ngrok**: اذهبي إلى [https://ngrok.com/download](https://ngrok.com/download) وقومي بتحميل النسخة المناسبة لنظام تشغيلك.
2.  **فك الضغط عن ngrok** وضعي الملف التنفيذي في مكان يسهل الوصول إليه (مثال: مجلد المشروع أو مجلد `bin`).
3.  **تشغيل ngrok**: افتحي Terminal أو Command Prompt جديد (غير الذي يشغل المشروع) وشغلي الأمر التالي:
    ```bash
    ./ngrok http 5000
    ```
    (إذا كنتِ على Windows، قد يكون `ngrok.exe http 5000`)
    سيظهر لكِ عنوان URL عام (مثال: `https://xxxxxx.ngrok-free.app`). هذا هو عنوان الـ webhook المؤقت الخاص بك.

### 4. إعداد الـ Webhook في Facebook Developer Console

1.  **اذهبي إلى لوحة تحكم تطبيقك** على Facebook Developer Console.
2.  من قائمة `Products`، اختاري `WhatsApp` ثم `Configuration`.
3.  في قسم `Webhook`، انقري على `Edit`.
4.  **Callback URL**: الصقي عنوان URL الذي حصلتِ عليه من `ngrok` (مثال: `https://xxxxxx.ngrok-free.app/whatsapp/webhook`). تأكدي من إضافة `/whatsapp/webhook` في النهاية، لأن هذا هو المسار الذي يستمع إليه مشروعك لرسائل الواتساب.
5.  **Verify Token**: أدخلي نفس الرمز الذي حددتيه في ملف `.env` لـ `WHATSAPP_VERIFY_TOKEN` (مثال: `my_secret_token_123`).
6.  انقري على `Verify and Save`.
7.  **الاشتراك في حقول الـ Webhook**: بعد التحقق بنجاح، ستظهر لك قائمة بحقول الـ webhook. انقري على `Manage` بجانب `Webhooks Fields` واشتركي في حقل `messages` على الأقل لتلقي رسائل الواتساب.

### 5. اختبار التكامل

1.  **أرسلي رسالة واتساب** إلى رقم الهاتف الذي قمتِ بإعداده في WhatsApp Business Account.
2.  يجب أن تظهر الرسالة في Terminal الذي يشغل مشروعك، ويجب أن يقوم المشروع بالرد عليها.

## ملاحظات مهمة ⚠️

*   **رموز ngrok المميزة**: عنوان URL الذي يوفره `ngrok` مجاني مؤقت ويتغير في كل مرة تقومين فيها بتشغيله. للاستخدام المستمر، يمكنك التفكير في الحصول على حساب `ngrok` مدفوع للحصول على عناوين URL ثابتة.
*   **الأمان**: لا تشاركي مفاتيح الواتساب أو سر التطبيق مع أحد.
*   **للاختبار المحلي**: المشروع سيعمل بدون مفاتيح الواتساب، لكن لن تتمكني من إرسال/استقبال رسائل واتساب فعلية إلا بعد إعداد المفاتيح و `ngrok`.

## إذا واجهت مشاكل 🆘

*   **تأكدي من أن مشروعك يعمل** على `http://localhost:5000`.
*   **تأكدي من أن `ngrok` يعمل** بشكل صحيح ويظهر عنوان URL عام.
*   **تحققي من إعدادات الـ webhook** في Facebook Developer Console (Callback URL و Verify Token).
*   **راجعي ملفات الـ logs** في Terminal الخاص بالمشروع و Terminal الخاص بـ `ngrok` للبحث عن أي أخطاء.

---

**ملاحظة**: هذا المشروع معد للتعلم والاختبار. للاستخدام في الإنتاج، ستحتاجين لإعدادات أمان إضافية ودومين خاص بك.

