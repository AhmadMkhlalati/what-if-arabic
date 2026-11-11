# ماذا لو — استوديو الرسوم المتحركة (نسخة عربية)

مشروع مستقل لاستوديو «What If» لصنع حلقات قصيرة متحركة بأسلوب الشخصيات العصا، كل الإطارات SVG
تُرسم بالكود وتُصيَّر بواسطة Remotion. هذه النسخة تضيف:

- **دعم العربية**: خط Cairo، اتجاه يمين-لليسار، حروف متصلة في بطاقة العنوان، ودعم الصوت العربي (`"lang": "ar"`).
- **شخصية جديدة «نور»** بحجاب، وقطعتان جديدتان للشخصيات: `hijab` و`bald`.
- **صورة واحدة بأمر واحد**: `Portrait` (شخصية واحدة) و`ArabicTitle`، و`npm run still`.
- **فحص المتطلبات**: `npm run preflight`.

## تجربة سريعة (بدون مفتاح API)

    cd studio
    npm install
    npx remotion still src/index.ts ArabicTitle out/title-ar.png --frame=60
    npx remotion still src/index.ts Portrait out/noor.png --props='{"character":"noor","caption":"نور"}'
    npm run cast        # ورقة كل الشخصيات

للحلقات الكاملة (فيديو بلا صوت) تحتاج ffmpeg وبايثون؛ التفاصيل في `README.md` و`references/arabic.md`.

## الترخيص والمصدر
ترخيص MIT. حقوق © 2026 Ahmad Mkhlalati. المشروع مبني على عمل سابق مرخّص بـMIT، ويبقى إشعار حقوقه الأصلي في `LICENSE` كما يشترط الترخيص.
