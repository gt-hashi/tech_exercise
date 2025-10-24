import math

def sin_contrast(arr,linearity): #anplitudeのvariableを追加することで、コントラストの強さをlinearityで調整するのではなく、引き伸ばして調整できるようにする。amplitude = 0.5  # 0～1, 小さいほど中間を変えないnew_y = ((math.sin(pi_y - math.pi/2) * amplitude) + 0.5) * 255

    r,g,b = arr
    y = 0.299*r + 0.587*g + 0.114*b # グレースケール化にして、輝度を出す。
    pi_y = (y/255)*math.pi # 0~255 -> 0~π
    new_y = (math.sin(pi_y - math.pi/2) + 1)/2 * 255 # sinでコントラストを上げる。-1~1 ->0~2 -> 0~1 -> 0~255
    
    for i in range(linearity):
        new_y = (new_y + y)/2
        
    if new_y > 255:#255を超えたら255にする
        new_y = 255
        
    scale = new_y / y if y > 0 else 1 #輝度の変化率。もし、元の輝度が０にものすごく近い場合、急に明るくなる可能性があるので、１にする。
    
    new_r, new_g, new_b = [i*scale if i*scale <= 255 else 255 for i in arr]
    
    return (int(new_r), int(new_g), int(new_b))

def change_brightness(arr,factor):
    r,g,b = arr
    y = 0.299*r + 0.587*g + 0.114*b # グレースケール化にして、輝度を出す。
    new_y = y * factor#新しい輝度
    
    if new_y > 255:#255を超えたら255にする
        new_y = 255
        
    scale = new_y/ (y + 1e-6) #輝度の変化率
    
    new_r, new_g, new_b = [i*scale if i*scale <= 255 else 255 for i in arr]
    
    return (int(new_r), int(new_g), int(new_b))

def change_saturation(arr, factor):
    r, g, b = arr
    
    y = 0.299*r + 0.587*g + 0.114*b# 輝度（Y）
    
    new_r = y + (r - y) * factor# 彩度をfactor倍
    new_g = y + (g - y) * factor
    new_b = y + (b - y) * factor
    
    # 0〜255にクリップ
    new_r = max(0, min(255, int(new_r)))
    new_g = max(0, min(255, int(new_g)))
    new_b = max(0, min(255, int(new_b)))
    
    return (new_r, new_g, new_b)