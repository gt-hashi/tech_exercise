from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from .models import GeneratedImage
from .filters import sin_contrast, change_brightness, change_saturation # ← filters.py に定義
from PIL import Image
import random
from io import BytesIO

def home(request):
    # home.html を表示
    images = GeneratedImage.objects.order_by("-created_at")
    return render(request, "hello_world_app/home.html", {"images": images})



@csrf_exempt
def process_image(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        img = Image.open(uploaded_file).convert("RGB")
        raster = img.load()

        # アルゴリズム適用
        random.seed(0)
        random_ratio = 0.01
        brightness_factor = 1 # 明るさを変える, 0.0 <= factor <= 2.0（〜3.0）
        saturation_factor = 0.5 # 彩度を変える, 0.0 <= factor <= 2.0（〜3.0）
        sin_contrast_linearity = 1 # コントラストを上げる, 線形化指数linearity: 0〜5くらい
        for y in range(img.height):
            for x in range(img.width):
                
                if random.random() < random_ratio:
                    r,g,b = (0,0,0)
                    raster[x,y] = (r,g,b)
                else:
                    new_r, new_g, new_b = change_brightness(raster[x,y],brightness_factor) # 明るさを変える, 0.0 <= factor <= 2.0（〜3.0）
                    new_r, new_g, new_b = change_saturation((new_r, new_g, new_b),saturation_factor) # 彩度を変える, 0.0 <= factor <= 2.0（〜3.0）
                    new_r, new_g, new_b = sin_contrast((new_r, new_g, new_b),sin_contrast_linearity) # コントラストを上げる, linearity: 0〜5くらい
                    raster[x,y] = (new_r, new_g, new_b)  


        # 保存処理
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        image_file = ContentFile(buffer.getvalue())

        generated = GeneratedImage()
        generated.file.save(f"converted_{uploaded_file.name}", image_file)
        generated.save()

        return JsonResponse({
            "url": generated.file.url,
            "name": generated.file.name.split("/")[-1]
        })


    return JsonResponse({"error": "No file uploaded"}, status=400)


