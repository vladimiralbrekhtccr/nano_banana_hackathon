from PIL import Image
import sys

def concat_images_horizontal(image1_path, image2_path, output_path):
    """
    Склеивает два изображения слева направо (горизонтально)
    
    Args:
        image1_path: путь к первому изображению (слева)
        image2_path: путь ко второму изображению (справа)
        output_path: путь для сохранения результата
    """
    # Открываем изображения
    img1 = Image.open(image1_path)
    img2 = Image.open(image2_path)
    
    # Получаем размеры
    width1, height1 = img1.size
    width2, height2 = img2.size
    
    # Выбираем максимальную высоту
    max_height = max(height1, height2)
    
    # Создаем новое изображение с суммарной шириной
    total_width = width1 + width2
    result_img = Image.new('RGB', (total_width, max_height), color='white')
    
    # Вставляем первое изображение слева
    result_img.paste(img1, (0, 0))
    
    # Вставляем второе изображение справа
    result_img.paste(img2, (width1, 0))
    
    # Сохраняем результат
    result_img.save(output_path)
    print(f"Изображения склеены и сохранены в: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python image_concat.py <путь_к_изображению1> <путь_к_изображению2> <путь_результата>")
        print("Пример: python image_concat.py img1.jpg img2.jpg result.jpg")
        # /home/vladimir_albrekht/projects/nano_banana_hack/src/demo_google_api/cute_girl.jpeg /home/vladimir_albrekht/projects/nano_banana_hack/src/demo_google_api/generated_image_6_th.png /home/vladimir_albrekht/projects/nano_banana_hack/src/demo_google_api/concat_1_2.png
        sys.exit(1)
    
    image1_path = sys.argv[1]
    image2_path = sys.argv[2] 
    output_path = sys.argv[3]
    
    try:
        concat_images_horizontal(image1_path, image2_path, output_path)
    except Exception as e:
        print(f"Ошибка: {e}")