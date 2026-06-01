# HandWritten Digit Recognition - Simple Documentation (Roman Urdu)

## 1) Ye Project Kya Hai?
Ye ek web app hai jo user ki upload ki hui handwritten number image (0 se 9) ko read karke batata hai ke number kya hai.

## 2) Kis Language Aur Framework Mein Banaya?
- **Python**: backend logic aur machine learning ke liye
- **Django**: poori web app chalane ke liye (routes, views, forms, login system)
- **HTML/CSS/Bootstrap**: website ka design aur UI
- **JavaScript (Bootstrap bundle)**: frontend interactions ke liye

## 3) Machine Learning / OCR Mein Kya Use Hua?
- **TensorFlow/Keras**: trained model (`CNN_Model.h5`) se digit prediction
- **Tesseract OCR (`pytesseract`)**: image se numbers text ki form mein nikalne ki koshish
- **OpenCV + NumPy + SciPy + Pillow**: image preprocessing (grayscale, threshold, resize, clean)

## 4) Database Kya Use Hui?
- **SQLite** (Django ki default DB)
- Prediction ka record save hota hai (image, predicted digit, confidence waghera)

## 5) Main Features
- User signup/login
- Image upload
- Handwritten digit prediction
- Prediction confidence show hoti hai
- Profile aur dashboard pages

## 6) Project Ka Flow (Bohat Simple)
1. User login karta hai.
2. User handwritten digit image upload karta hai.
3. System pehle OCR se number read karta hai.
4. Agar OCR fail ho jaye to CNN model prediction karta hai.
5. Result screen par show hota hai aur database mein save hota hai.

## 7) Maine Ye Project Kaise Build Kiya? (Short Explain)
1. Django project setup kiya aur app banayi.
2. Templates aur static files se frontend pages banaye.
3. Model training se banay hue CNN model file ko project mein load kiya.
4. Image preprocessing aur prediction logic `views.py` mein add ki.
5. User authentication aur profile system add kiya.
6. Upload -> process -> predict -> save ka complete flow implement kiya.

## 8) Teacher Ko One-Line Mein Kaise Batana Hai?
"Mera project Django based web app hai jo Python, TensorFlow/Keras aur OCR ki madad se handwritten digits ko recognize karta hai, aur result database mein save karta hai."
