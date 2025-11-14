import cv2
import os

def extract_screenshots(video_path):
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = f"{base_name}_screenshots"
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames == 0:
        print("Erro: não foi possível ler o vídeo.")
        return

    percentages = [i * 10 for i in range(10)]  # 0%, 10%, ..., 90%

    for i, percent in enumerate(percentages):
        target_frame = int((percent / 100) * (total_frames - 1))
        cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)
        ret, frame = cap.read()
        if not ret:
            continue

        img_name = f"{base_name}_{i+1:02d}.png"
        img_path = os.path.join(output_dir, img_name)
        cv2.imwrite(img_path, frame)

    cap.release()
    print(f"Imagens salvas em: {output_dir}")