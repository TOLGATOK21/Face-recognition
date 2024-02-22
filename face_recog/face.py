import cv2
import face_recognition
import webbrowser

video_capture = cv2.VideoCapture(0)

tolga_image = face_recognition.load_image_file("vesikalık.jpg")
tolga_face_encoding = face_recognition.face_encodings(tolga_image)[0]

# Tanımlı yüzleri ve isimleri listele
known_face_encodings = [tolga_face_encoding]
known_face_names = ["Tolga Tok" , ]
occur_name = []

cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Video', 800, 600)

while True:
    ret, frame = video_capture.read()

    # ALDIĞIMIZ KAREYİ KÜÇÜLTÜYORUZ Kİ HIZLI SONUÇ ALALIM
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # BGR DAN RGB YE ÇEVİRR
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # UYUMLU YÜZLERİN LOKASYONLARINI BULAN KOD KISMI
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # Tanımlı yüzlerle eşleşmeyi kontrol et
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Bilinmiyor"

        # Eşleşen bir yüz bulunduysa ismi al
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)
        
        occur_name.append(name)

    # Sonuçları ekrana yazdır
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Yüzü çerçeve içerisine al
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)

        # Yüzün altına etiket ekle
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 8, bottom - 8), font, 1.0, (255, 255, 255), 1)

    # Ekranda en üstte isimleri göstermek için metin kutusu ekle
    cv2.rectangle(frame, (0, 0), (800, 50), (0, 0, 0), cv2.FILLED)
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, ", ".join(set(occur_name)), (10, 30), font, 1.0, (255, 255, 255), 1)

    # Sonuçları görüntüle
    cv2.imshow('Video', frame)
   


    # Çıkış işlemi
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

# Video yakalama nesnesini serbest bırak ve pencereyi kapat
video_capture.release()
cv2.destroyAllWindows()
